DENIALS = {
    "unknown actor": "The actor is not in the local policy.",
    "unknown tool": "The tool is not in the local policy.",
    "role denied": "This role cannot call the tool.",
    "approval required": "The tool changes the service and needs an approval flag.",
}

def explain(reason: str) -> str:
    return DENIALS.get(reason, reason)
