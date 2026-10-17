from ops_gateway.reconcile import reconcile_after_timeout

def after_timeout(fetch_status, operation_id: str, attempts: int = 3) -> dict:
    return reconcile_after_timeout(fetch_status, operation_id, attempts=attempts)
