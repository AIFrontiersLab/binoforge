from __future__ import annotations

import argparse
import logging
import os
from pathlib import Path

from ops_gateway.client import Gateway


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ops-gateway")
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run", help="Discover, authorize and execute one simulated tool")
    run.add_argument("--actor", default=os.environ.get("OPS_ACTOR", "operator"))
    run.add_argument("--tool", required=True)
    run.add_argument("--reason", default="inspect the demo service")
    run.add_argument("--approve", action="store_true")
    run.add_argument("--timeout", type=float, default=5.0)
    run.add_argument("--idempotency-key", default="demo")
    run.add_argument("--limit", type=int, default=10)
    run.add_argument("--policy", default="examples/policy.yaml")
    run.add_argument("--state", default=os.environ.get("OPS_STATE_PATH", ".run/service-state.json"))
    run.add_argument("--audit", default=os.environ.get("OPS_AUDIT_PATH", ".run/audit.jsonl"))
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    if args.command == "run":
        gateway = Gateway(
            policy_path=Path(args.policy),
            state_path=Path(args.state),
            audit_path=Path(args.audit),
        )
        return gateway.run(
            actor=args.actor,
            tool=args.tool,
            reason=args.reason,
            approved=args.approve,
            timeout=args.timeout,
            idempotency_key=args.idempotency_key,
            limit=args.limit,
        )
    return 2
