import pytest

from reconcile import StarterGap, reconcile_after_timeout


def test_starter_does_not_reconcile() -> None:
    with pytest.raises(StarterGap):
        reconcile_after_timeout(lambda _operation_id: {"state": "completed"}, "op_demo")
