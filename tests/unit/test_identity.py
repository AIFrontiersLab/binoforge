from ops_gateway.identity.operation_key import operation_id
from ops_gateway.operations.lifecycle import allows
from ops_gateway.operations.verify import verify_restart
from ops_gateway.recovery.terminal import is_terminal

def test_operation_id_is_stable() -> None:
    first = operation_id("operator", "restart_demo_service", "demo")
    second = operation_id("operator", "restart_demo_service", "demo")
    assert first == second
    assert first.startswith("op_")

def test_completed_does_not_return_to_running() -> None:
    assert allows("completed", "running") is False
    assert is_terminal("completed") is True

def test_verify_accepts_one_restart() -> None:
    assert verify_restart({"state": "completed", "restart_count": 1, "duplicate": False}) is True
    assert verify_restart({"state": "completed", "restart_count": 2, "duplicate": False}) is False
