from ops_gateway.budget import CallBudget

def meter(limit: int = 12) -> CallBudget:
    return CallBudget(limit=limit)
