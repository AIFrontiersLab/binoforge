from __future__ import annotations

import fcntl
import json
import os
from pathlib import Path


def initial_state() -> dict:
    return {
        "generation": 1,
        "status": "healthy",
        "restart_count": 0,
        "operations": {},
        "logs": ["service started"],
    }


def load_state(path: Path) -> dict:
    if not path.exists():
        return initial_state()
    return json.loads(path.read_text(encoding="utf-8"))


def restart(path: Path, operation_id: str, reason: str, mode: str) -> dict:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        handle.seek(0)
        raw = handle.read()
        data = json.loads(raw) if raw.strip() else initial_state()
        existing = data["operations"].get(operation_id)
        if existing:
            result = {"duplicate": True, "restart_count": data["restart_count"], **existing}
        else:
            if mode == "stall":
                record = {"state": "running", "reason": reason, "generation": data["generation"]}
                data["logs"].append(f"restart started {operation_id}")
                data["operations"][operation_id] = record
                result = {"duplicate": False, "restart_count": data["restart_count"], **record}
            else:
                data["generation"] += 1
                data["restart_count"] += 1
                data["status"] = "healthy"
                record = {"state": "completed", "reason": reason, "generation": data["generation"]}
                data["operations"][operation_id] = record
                data["logs"].append(f"restart completed {operation_id} generation {data['generation']}")
                result = {"duplicate": False, "restart_count": data["restart_count"], **record}
        _write_locked(handle, data)
        return result


def operation_status(path: Path, operation_id: str) -> dict:
    data = load_state(path)
    record = data["operations"].get(operation_id)
    if record is None:
        return {"state": "missing", "operation_id": operation_id, "generation": data["generation"]}
    return {
        "operation_id": operation_id,
        "restart_count": data["restart_count"],
        "service_generation": data["generation"],
        **record,
    }


def service_health(path: Path) -> dict:
    data = load_state(path)
    return {"status": data["status"], "generation": data["generation"], "service": "demo"}


def service_logs(path: Path, limit: int) -> dict:
    data = load_state(path)
    return {"lines": data["logs"][-limit:]}


def _write_locked(handle, data: dict) -> None:
    handle.seek(0)
    handle.truncate()
    handle.write(json.dumps(data, indent=2))
    handle.flush()
    os.fsync(handle.fileno())
