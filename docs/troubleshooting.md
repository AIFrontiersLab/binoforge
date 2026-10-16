# Troubleshooting

## Demo cannot find the package

Install it in the same environment you use to run the demo:

```bash
python -m pip install -e .
```

## Tests fail in starter/

Starter tests are supposed to fail until the challenge is implemented.
Run `pytest -q` for the reference solution.

## Timeout looks immediate

The MCP demo, when this is the operations gateway, uses a short client timeout on purpose.
Increase `--timeout` only when you are not reproducing the lost-response case.

## State from an older run

Delete the local `.run` or `.demo` directory and run the demo again.
