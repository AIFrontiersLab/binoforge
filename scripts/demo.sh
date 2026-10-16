#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
rm -rf .demo
mkdir -p .demo
export OPS_STATE_PATH="$PWD/.demo/service-state.json"
export OPS_AUDIT_PATH="$PWD/.demo/audit.jsonl"
export OPS_MODE=delay
export OPS_RESTART_DELAY_SECONDS=1.2
python -m ops_gateway run \
  --actor operator \
  --tool restart_demo_service \
  --reason "recover the demo service" \
  --approve \
  --timeout 0.4 \
  --idempotency-key demo-timeout \
  --state "$OPS_STATE_PATH" \
  --audit "$OPS_AUDIT_PATH"
python - << 'PY'
import json
import os
from pathlib import Path
state = json.loads(Path(os.environ["OPS_STATE_PATH"]).read_text())
audit = Path(os.environ["OPS_AUDIT_PATH"]).read_text()
assert state["restart_count"] == 1
assert "reconciled" in audit
print("demo-ok")
PY
