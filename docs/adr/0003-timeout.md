# Timeout

The client timeout does not mean the restart failed. The gateway polls durable status a fixed number of times. A completed record is reconciled. A record that is still running is escalated.
