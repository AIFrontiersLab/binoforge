from __future__ import annotations

from pathlib import Path

import yaml


def load_policy(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def evaluate(policy: dict, actor: str, tool: str, approved: bool) -> tuple[bool, str]:
    actors = policy.get("actors") or {}
    tools = policy.get("tools") or {}
    if actor not in actors:
        return False, "unknown actor"
    role = actors[actor].get("role")
    spec = tools.get(tool)
    if spec is None:
        return False, "unknown tool"
    if role not in (spec.get("roles") or []):
        return False, "role denied"
    if spec.get("approval") and not approved:
        return False, "approval required"
    return True, "permit"


def validate_arguments(tool: str, arguments: dict) -> dict:
    cleaned = dict(arguments)
    if tool == "restart_demo_service":
        reason = str(cleaned.get("reason") or "")
        if not 8 <= len(reason) <= 200:
            raise ValueError("reason must be 8 to 200 characters")
        operation_id = str(cleaned.get("operation_id") or "")
        if not operation_id.startswith("op_") or len(operation_id) < 8:
            raise ValueError("operation_id must be a stable op_ identifier")
    if tool == "inspect_logs":
        limit = int(cleaned.get("limit") or 10)
        if not 1 <= limit <= 20:
            raise ValueError("limit must be 1 to 20")
        cleaned["limit"] = limit
    if tool == "get_operation_status":
        operation_id = str(cleaned.get("operation_id") or "")
        if not operation_id.startswith("op_"):
            raise ValueError("operation_id is required")
    return cleaned
