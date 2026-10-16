# Engineering challenge

The restart succeeds, but the client times out before receiving confirmation. Decide how to reconcile durable state without issuing a second restart.

## Prerequisites

Python 3.12; The mcp package.

## Setup

Install the reference package, then read `starter/`.

## Starter mode

starter/ops_gateway/reconcile.py raises StarterGap.

## Reference solution

src/ops_gateway/reconcile.py polls status and escalates inside a bound.

## Failure injection

OPS_MODE=stall

```bash
bash scripts/failure_injection.sh
```

## Expected outcome

One restart, a reconciled audit event and no second generation bump.

## Acceptance

- Tool discovery uses the MCP client and lists the four simulated tools.
- Restart without approval is denied.
- A timeout still observes one completed restart.
- A second call with the same operation id does not restart again.
- An unresolved running operation escalates.

## Extensions

- Add a second approver role for restart.
