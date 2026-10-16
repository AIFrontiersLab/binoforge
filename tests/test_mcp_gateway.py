import json
from pathlib import Path

from ops_gateway.audit import read_events
from ops_gateway.client import Gateway

ROOT = Path(__file__).resolve().parents[1]


def _gateway(tmp_path: Path) -> Gateway:
    return Gateway(
        policy_path=ROOT / "examples" / "policy.yaml",
        state_path=tmp_path / "state.json",
        audit_path=tmp_path / "audit.jsonl",
    )


def test_discovery_lists_simulated_tools(tmp_path: Path) -> None:
    import asyncio

    gateway = _gateway(tmp_path)
    names = asyncio.run(gateway._discover())
    assert {
        "get_service_health",
        "inspect_logs",
        "restart_demo_service",
        "get_operation_status",
    } <= set(names)


def test_health_uses_mcp(tmp_path: Path) -> None:
    code = _gateway(tmp_path).run(
        actor="reader",
        tool="get_service_health",
        reason="read health",
        approved=False,
        timeout=5,
        idempotency_key="health-1",
    )
    assert code == 0


def test_timeout_reconciles_one_restart(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("OPS_MODE", "delay")
    monkeypatch.setenv("OPS_RESTART_DELAY_SECONDS", "1.2")
    gateway = _gateway(tmp_path)
    code = gateway.run(
        actor="operator",
        tool="restart_demo_service",
        reason="recover the demo service",
        approved=True,
        timeout=0.4,
        idempotency_key="timeout-1",
    )
    assert code == 0
    events = [item["event"] for item in read_events(gateway.audit_path)]
    assert "timeout" in events
    assert "reconciled" in events
    state = json.loads(gateway.state_path.read_text(encoding="utf-8"))
    assert state["restart_count"] == 1
    again = gateway.run(
        actor="operator",
        tool="restart_demo_service",
        reason="recover the demo service",
        approved=True,
        timeout=5,
        idempotency_key="timeout-1",
    )
    assert again == 0
    state = json.loads(gateway.state_path.read_text(encoding="utf-8"))
    assert state["restart_count"] == 1


def test_stall_escalates(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("OPS_MODE", "stall")
    monkeypatch.setenv("OPS_RESTART_DELAY_SECONDS", "1.2")
    gateway = _gateway(tmp_path)
    code = gateway.run(
        actor="operator",
        tool="restart_demo_service",
        reason="recover the demo service",
        approved=True,
        timeout=0.4,
        idempotency_key="stall-1",
    )
    assert code == 2
    events = [item["event"] for item in read_events(gateway.audit_path)]
    assert "escalate" in events
    state = json.loads(gateway.state_path.read_text(encoding="utf-8"))
    assert state["restart_count"] == 0
