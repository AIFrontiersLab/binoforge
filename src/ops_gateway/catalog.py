from __future__ import annotations


TOOLS = {
    "get_service_health": {"kind": "read", "approval": False},
    "inspect_logs": {"kind": "read", "approval": False},
    "restart_demo_service": {"kind": "change", "approval": True},
    "get_operation_status": {"kind": "read", "approval": False},
}


def known_tools() -> list[str]:
    return list(TOOLS)
