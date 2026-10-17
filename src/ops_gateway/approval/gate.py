from ops_gateway.policy import evaluate, validate_arguments

def authorize(policy: dict, actor: str, tool: str, approved: bool, arguments: dict) -> tuple[bool, str, dict]:
    try:
        cleaned = validate_arguments(tool, arguments)
    except ValueError as exc:
        return False, str(exc), arguments
    permitted, why = evaluate(policy, actor, tool, approved)
    return permitted, why, cleaned
