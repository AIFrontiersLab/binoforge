# Binoforge

An operations agent can discover powerful tools, but discovery alone does not grant permission to execute them.

A local MCP restart either returns a verified result, reconciles after a timeout or escalates when the outcome stays uncertain.

The service keeps its own checkpoint, audit trail and attempt budget. A repeat of a finished step does not apply that step again. Untrusted instruction text is denied before any side effect. The demo runs from local fixtures.

## Install

```bash
python -m pip install -e .
```

Copy the example environment if you want local paths:

```bash
cp .env.example .env
```

## Demo

```bash
bash scripts/demo.sh
```

The demo uses local fixtures. Network access is not required.

## Layout

- `policy` checks the actor, the role and the approval flag.
- `store` keeps the operation id and the service generation.
- `audit` records permit, timeout, reconcile and escalation.
- `reconcile` polls status inside a fixed bound.
- `mcp_server` exposes the local service tools.
- `limits` loads the local attempt and score bounds.
- `store` writes the checkpoint with an atomic replace.
- `audit` appends one line after a commit.
- `policy` denies empty input and instruction text.
- `budget` stops a step after the configured attempts.

- `docs/architecture.md` has the Mermaid diagrams for the overview, the components and the recovery flow.
- `docs/operations.md` covers local state, retries and the failure drill.
- `docs/challenge.md` describes the open engineering decision in `starter/`.
- `docs/troubleshooting.md` lists common failures.
- `docs/security.md` lists the trust assumptions.

## Architecture

```mermaid
flowchart LR
  intake[Request intake]
  policy[Policy and approval]
  intake --> policy
  execution[Execution and recovery]
  policy --> execution
```

The component diagram and the recovery flow are in `docs/architecture.md`.

## Tests

```bash
pytest -q
```

The starter workspace is separate and stays incomplete until that decision is implemented:

```bash
pytest -q starter/tests
```
