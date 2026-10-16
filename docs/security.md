# Security assumptions

Sensitive actions in this demo: restart_demo_service.

The demo does not receive production credentials.
Task files, documents and tool results are untrusted data.
The project does not execute instructions found inside those inputs.

Trust boundaries:

- A discovered tool is not executable until policy and approval pass.

Unknowns:

- Exactly-once execution across arbitrary external systems is TBD
- Behavior on arbitrary external systems is TBD

This project does not claim exactly-once execution on arbitrary external systems.
