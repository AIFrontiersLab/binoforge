from __future__ import annotations

import json
import os
import time
from pathlib import Path

from mcp.server.mcpserver import MCPServer

from ops_gateway.store import operation_status, restart, service_health, service_logs

server = MCPServer("ops-demo-service")


def _state_path() -> Path:
    return Path(os.environ["OPS_STATE_PATH"])


@server.tool(structured_output=False)
def get_service_health() -> str:
    """Return the simulated service health and generation."""
    return json.dumps(service_health(_state_path()))


@server.tool(structured_output=False)
def inspect_logs(limit: int = 10) -> str:
    """Return recent simulated service log lines."""
    bounded = max(1, min(int(limit), 20))
    return json.dumps(service_logs(_state_path(), bounded))


@server.tool(structured_output=False)
def restart_demo_service(operation_id: str, reason: str) -> str:
    """Restart the simulated service once for this operation id."""
    mode = os.environ.get("OPS_MODE", "normal")
    result = restart(_state_path(), operation_id, reason, mode)
    delay = float(os.environ.get("OPS_RESTART_DELAY_SECONDS", "0") or 0)
    if delay > 0 and not result["duplicate"]:
        time.sleep(delay)
    return json.dumps(result)


@server.tool(structured_output=False)
def get_operation_status(operation_id: str) -> str:
    """Read durable status for an operation without starting a new restart."""
    return json.dumps(operation_status(_state_path(), operation_id))


def main() -> None:
    server.run(transport="stdio")


if __name__ == "__main__":
    main()
