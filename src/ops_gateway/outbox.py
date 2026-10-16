from __future__ import annotations

import json
from pathlib import Path


def enqueue(path: Path, notice: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(notice) + "\n")
