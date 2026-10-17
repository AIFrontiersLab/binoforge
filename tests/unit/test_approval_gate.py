from pathlib import Path

from ops_gateway.approval.gate import authorize
from ops_gateway.approval.reasons import explain
from ops_gateway.policy import load_policy

ROOT = Path(__file__).resolve().parents[2]

def test_reader_restart_is_denied() -> None:
    policy = load_policy(ROOT / "examples" / "policy.yaml")
    permitted, why, _cleaned = authorize(
        policy,
        "reader",
        "restart_demo_service",
        True,
        {"operation_id": "op_demo1234", "reason": "clear the stuck demo", "limit": 10},
    )
    assert permitted is False
    assert why == "role denied"
    assert "role" in explain(why)
