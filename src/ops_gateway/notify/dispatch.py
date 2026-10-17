from pathlib import Path

from ops_gateway.journal import note
from ops_gateway.outbox import enqueue

NOTICE = {"reconciled", "escalate", "denied"}

def fanout(journal_path: Path, outbox_path: Path, event: dict) -> None:
    note(journal_path, event)
    if event.get("event") in NOTICE:
        enqueue(outbox_path, event)
