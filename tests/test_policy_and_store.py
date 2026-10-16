from pathlib import Path

import pytest

from ops_gateway.policy import evaluate, load_policy, validate_arguments
from ops_gateway.reconcile import reconcile_after_timeout
from ops_gateway.store import restart

ROOT = Path(__file__).resolve().parents[1]


def test_reader_cannot_restart() -> None:
    policy = load_policy(ROOT / "examples" / "policy.yaml")
    allowed, reason = evaluate(policy, "reader", "restart_demo_service", approved=True)
    assert not allowed
    assert reason == "role denied"


def test_restart_requires_approval() -> None:
    policy = load_policy(ROOT / "examples" / "policy.yaml")
    allowed, reason = evaluate(policy, "operator", "restart_demo_service", approved=False)
    assert not allowed
    assert reason == "approval required"


def test_limit_is_bounded() -> None:
    with pytest.raises(ValueError):
        validate_arguments("inspect_logs", {"limit": 100})


def test_duplicate_restart_does_not_increment(tmp_path: Path) -> None:
    path = tmp_path / "state.json"
    first = restart(path, "op_demo1234", "clear the stuck demo", "normal")
    second = restart(path, "op_demo1234", "clear the stuck demo", "normal")
    assert first["duplicate"] is False
    assert first["restart_count"] == 1
    assert second["duplicate"] is True
    assert second["restart_count"] == 1
    assert second["generation"] == first["generation"]


def test_reconcile_escalates_when_status_stays_running() -> None:
    def fetch(_operation_id: str) -> dict:
        return {"state": "running"}

    decision = reconcile_after_timeout(fetch, "op_demo1234", attempts=3)
    assert decision["outcome"] == "escalate"


def test_reconcile_returns_completed_without_another_restart() -> None:
    calls = {"count": 0}

    def fetch(_operation_id: str) -> dict:
        calls["count"] += 1
        return {"state": "completed", "restart_count": 1}

    decision = reconcile_after_timeout(fetch, "op_demo1234", attempts=3)
    assert decision["outcome"] == "reconciled"
    assert calls["count"] == 1
