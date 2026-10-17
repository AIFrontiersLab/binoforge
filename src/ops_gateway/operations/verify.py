def verify_restart(payload: dict) -> bool:
    if payload.get("duplicate"):
        return payload.get("state") == "completed" and int(payload.get("restart_count") or 0) >= 1
    return payload.get("state") == "completed" and int(payload.get("restart_count") or 0) == 1
