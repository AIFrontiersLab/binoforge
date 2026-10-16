# Operations

## Local state

The process writes checkpoints under `.run/` or the path you pass on the command line. A checkpoint is replaced atomically. An audit line is appended only after a step commits.

## Attempts

Each unfinished step can be tried three times. A crash records the attempt and does not commit the side effect. The next run continues from the last commit.

## Demo

```bash
bash scripts/demo.sh
```

## Failure drill

```bash
bash scripts/failure_injection.sh
```

## What this service does not do

- Exactly-once execution on arbitrary external systems
- Restarting a real production service
- A custom JSON dispatcher labeled as MCP
