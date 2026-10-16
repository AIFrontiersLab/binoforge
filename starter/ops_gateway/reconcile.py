class StarterGap(RuntimeError):
    """The starter leaves timeout reconciliation unimplemented."""


def reconcile_after_timeout(fetch_status, operation_id: str, *, attempts: int = 3) -> dict:
    raise StarterGap(
        "The restart may already be durable. Read operation status before you decide to retry "
        "and escalate when the state stays running."
    )
