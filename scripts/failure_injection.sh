#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
rm -rf .run
mkdir -p .run
export OPS_STATE_PATH="$PWD/.run/service-state.json"
export OPS_AUDIT_PATH="$PWD/.run/audit.jsonl"
export OPS_MODE=stall
export OPS_RESTART_DELAY_SECONDS=1.2
set +e
python -m ops_gateway run \
  --actor operator \
  --tool restart_demo_service \
  --reason "recover the demo service" \
  --approve \
  --timeout 0.4 \
  --idempotency-key stall-demo \
  --state "$OPS_STATE_PATH" \
  --audit "$OPS_AUDIT_PATH"
code=$?
set -e
test "$code" -eq 2
python - << 'PY'
import json
import os
from pathlib import Path
state = json.loads(Path(os.environ["OPS_STATE_PATH"]).read_text())
audit = Path(os.environ["OPS_AUDIT_PATH"]).read_text()
assert state["restart_count"] == 0
assert "escalate" in audit
print("failure-injection-ok")
PY
