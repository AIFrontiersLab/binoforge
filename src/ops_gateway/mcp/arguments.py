def for_tool(tool: str, arguments: dict) -> dict:
    if tool == "restart_demo_service":
        return {"operation_id": arguments["operation_id"], "reason": arguments["reason"]}
    if tool == "get_operation_status":
        return {"operation_id": arguments["operation_id"]}
    if tool == "inspect_logs":
        return {"limit": arguments["limit"]}
    return {}
