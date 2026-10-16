from ops_gateway.budget import CallBudget
from ops_gateway.catalog import known_tools


def test_catalog_lists_the_service_tools() -> None:
    assert "restart_demo_service" in known_tools()


def test_budget_rejects_the_call_past_the_limit() -> None:
    budget = CallBudget(limit=1)
    assert budget.take("get_service_health") == 1
    try:
        budget.take("inspect_logs")
    except RuntimeError as exc:
        assert "budget" in str(exc)
    else:
        raise AssertionError("budget should stop the second call")
