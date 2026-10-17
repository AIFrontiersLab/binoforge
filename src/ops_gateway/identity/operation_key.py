import hashlib

def operation_id(actor: str, tool: str, idempotency_key: str) -> str:
    digest = hashlib.sha256(f"{actor}|{tool}|{idempotency_key}".encode("utf-8")).hexdigest()[:16]
    return f"op_{digest}"
