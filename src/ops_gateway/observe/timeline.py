def classify(event: str) -> str:
    if event in {"denied"}:
        return "control"
    if event in {"timeout", "reconciled", "escalate"}:
        return "recovery"
    if event in {"executed", "duplicate_prevented", "approved"}:
        return "change"
    return "other"
