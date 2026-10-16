# Starter

The reference restart path is already able to time out.
`reconcile.py` is the open decision.

Read durable operation status after a timeout.
Do not call restart again for the same operation id.
Escalate when the status is still running after the bounded polls.
