from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import os
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.shared.exceptions import MCPError

from ops_gateway.audit import append
from ops_gateway.policy import evaluate, load_policy, validate_arguments
from ops_gateway.reconcile import reconcile_after_timeout

LOGGER = logging.getLogger("ops_gateway")
READ_TOOLS = {"get_service_health", "inspect_logs", "get_operation_status"}


def operation_id(actor: str, tool: str, idempotency_key: str) -> str:
    digest = hashlib.sha256(f"{actor}|{tool}|{idempotency_key}".encode("utf-8")).hexdigest()[:16]
    return f"op_{digest}"


class Gateway:
    def __init__(self, *, policy_path: Path, state_path: Path, audit_path: Path) -> None:
        self.policy = load_policy(policy_path)
        self.state_path = state_path
        self.audit_path = audit_path

    def run(
        self,
        *,
        actor: str,
        tool: str,
        reason: str,
        approved: bool,
        timeout: float,
        idempotency_key: str,
        limit: int = 10,
    ) -> int:
        op_id = operation_id(actor, tool, idempotency_key)
        arguments = {"operation_id": op_id, "reason": reason, "limit": limit}
        try:
            arguments = validate_arguments(tool, arguments)
        except ValueError as exc:
            self._audit({"event": "denied", "actor": actor, "tool": tool, "reason": str(exc)})
            print(json.dumps({"status": "denied", "reason": str(exc)}))
            return 1
        permitted, why = evaluate(self.policy, actor, tool, approved)
        if not permitted:
            self._audit({"event": "denied", "actor": actor, "tool": tool, "reason": why})
            print(json.dumps({"status": "denied", "reason": why}))
            return 1
        self._audit({"event": "approved", "actor": actor, "tool": tool, "operation_id": op_id})
        names = asyncio.run(self._discover())
        if tool not in names:
            self._audit({"event": "denied", "actor": actor, "tool": tool, "reason": "tool not discovered"})
            print(json.dumps({"status": "denied", "reason": "tool not discovered"}))
            return 1
        timed_out = False
        payload: dict = {}
        try:
            payload = asyncio.run(self._call(tool, _tool_arguments(tool, arguments), timeout))
        except Exception as exc:
            if not _is_timeout(exc):
                raise
            timed_out = True
            self._audit({"event": "timeout", "operation_id": op_id, "tool": tool})
        if timed_out or payload.get("state") == "running":
            decision = reconcile_after_timeout(self._status_sync, op_id, attempts=3)
            record = decision.get("record") or {}
            if decision["outcome"] == "reconciled" and record.get("state") == "completed":
                self._audit({"event": "reconciled", "operation_id": op_id, "state": "completed"})
                verified = self._verify(record)
                print(json.dumps({"status": "reconciled", "operation_id": op_id, "verified": verified, **record}))
                return 0 if verified else 1
            self._audit({"event": "escalate", "operation_id": op_id, "state": record.get("state")})
            print(json.dumps({"status": "escalate", "operation_id": op_id, "record": record}))
            return 2
        if payload.get("duplicate"):
            self._audit({"event": "duplicate_prevented", "operation_id": op_id})
        else:
            self._audit({"event": "executed", "operation_id": op_id, "tool": tool})
        if tool == "restart_demo_service":
            verified = self._verify(payload)
            print(json.dumps({"status": "executed", "operation_id": op_id, "verified": verified, **payload}))
            return 0 if verified else 1
        print(json.dumps({"status": "executed", "operation_id": op_id, **payload}))
        return 0

    def _verify(self, payload: dict) -> bool:
        if payload.get("duplicate"):
            return payload.get("state") == "completed" and int(payload.get("restart_count") or 0) >= 1
        return payload.get("state") == "completed" and int(payload.get("restart_count") or 0) == 1

    def _status_sync(self, op_id: str) -> dict:
        return asyncio.run(self._call("get_operation_status", {"operation_id": op_id}, 5))

    async def _discover(self) -> list[str]:
        async with stdio_client(self._params()) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                listed = await session.list_tools()
        return [tool.name for tool in listed.tools]

    async def _call(self, tool: str, arguments: dict, timeout: float) -> dict:
        async with stdio_client(self._params()) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(tool, arguments, read_timeout_seconds=timeout)
        return _payload(result)

    def _params(self) -> StdioServerParameters:
        env = {
            "OPS_STATE_PATH": str(self.state_path),
            "OPS_MODE": os.environ.get("OPS_MODE", "normal"),
            "OPS_RESTART_DELAY_SECONDS": os.environ.get("OPS_RESTART_DELAY_SECONDS", "0"),
        }
        if os.environ.get("PYTHONPATH"):
            env["PYTHONPATH"] = os.environ["PYTHONPATH"]
        return StdioServerParameters(
            command=os.environ.get("OPS_PYTHON", sys.executable),
            args=["-m", "ops_gateway.mcp_server"],
            env=env,
        )

    def _audit(self, event: dict) -> None:
        append(self.audit_path, event)
        LOGGER.info("%s", event["event"])


def _is_timeout(exc: BaseException) -> bool:
    if isinstance(exc, TimeoutError):
        return True
    if isinstance(exc, MCPError) and "timed out" in str(exc).lower():
        return True
    if isinstance(exc, BaseExceptionGroup):
        return bool(exc.exceptions) and all(_is_timeout(item) for item in exc.exceptions)
    return False


def _tool_arguments(tool: str, arguments: dict) -> dict:
    if tool == "restart_demo_service":
        return {"operation_id": arguments["operation_id"], "reason": arguments["reason"]}
    if tool == "get_operation_status":
        return {"operation_id": arguments["operation_id"]}
    if tool == "inspect_logs":
        return {"limit": arguments["limit"]}
    return {}


def _payload(result) -> dict:
    if getattr(result, "isError", False) or getattr(result, "is_error", False):
        raise RuntimeError(_text(result) or "tool error")
    text = _text(result)
    if not text:
        structured = getattr(result, "structured_content", None) or getattr(result, "structuredContent", None)
        if isinstance(structured, dict):
            return structured
        return {}
    return json.loads(text)


def _text(result) -> str:
    parts = []
    for block in getattr(result, "content", None) or []:
        text = getattr(block, "text", None)
        if text:
            parts.append(text)
    return "\n".join(parts)
