# Architecture

Scenario: An operations agent can discover a restart tool. The restart must still pass identity, policy and approval and a timed out client must reconcile durable state.

## Overview

- Request intake: in CLI request, out validated tool call.
- Policy and approval: in validated tool call, out permit or denial.
- Execution and recovery: in permitted tool call, out verified result or escalation.

## Components

- CLI intake (design): Accept the actor, tool, reason and idempotency key.
- MCP discovery (documented): List tools from a local MCP server over stdio.
- Argument check (design): Reject missing or oversized arguments.
- Identity policy (design): Allow the tool only for a matching role.
- Approval gate (design): Hold restart until an explicit approval flag is set.
- MCP executor (documented): Call the selected tool with a timeout.
- Operation store (design): Persist operation state before a delayed reply.
- Result check (design): Confirm service generation and duplicate status.
- Recovery (design): Poll status inside a bound and escalate if it stays running.
- Audit log (design): Append permit, timeout, reconcile and escalation events.

## Flows

Success: discover tools; validate arguments; approve restart; write completed operation; verify generation.

Failure and recovery: client times out; new session reads durable status; escalate when status stays running.

## Diagrams

```mermaid
flowchart LR
  intake[Request intake]
  policy[Policy and approval]
  intake --> policy
  execution[Execution and recovery]
  policy --> execution
```

```mermaid
flowchart TB
  subgraph intake [Request intake]
    cli_intake[CLI intake]
    mcp_discovery[MCP discovery]
    argument_validator[Argument check]
  end
  subgraph policy [Policy and approval]
    identity_policy[Identity policy]
    approval_gate[Approval gate]
  end
  subgraph execution [Execution and recovery]
    mcp_executor[MCP executor]
    operation_store[Operation store]
    result_verifier[Result check]
    recovery[Recovery]
    audit_log[Audit log]
  end
  cli_intake -->|request| argument_validator
  argument_validator -->|tool name| mcp_discovery
  mcp_discovery -->|tool list| identity_policy
  identity_policy -->|role decision| approval_gate
  approval_gate -->|permit| mcp_executor
  mcp_executor -->|operation id| operation_store
  mcp_executor -->|tool result| result_verifier
  result_verifier -->|timeout or result| recovery
  recovery -->|audit event| audit_log
```

```mermaid
flowchart TD
  receive_request[Receive request]
  discover_tools[Discover MCP tools]
  validate_args[Validate arguments]
  policy_decision{Policy and approval}
  execute_tool[Execute with timeout]
  timeout_decision{Client timed out}
  reconcile_status[Read durable status]
  verify_result[Verify generation]
  write_audit[Append audit]
  escalate[Escalate to a person]
  deny_request[Deny request]
  operation_store[Operation state file]
  receive_request -->|request control| discover_tools
  discover_tools -->|tool list data| validate_args
  validate_args -->|arguments control| policy_decision
  policy_decision -->|permit control| execute_tool
  policy_decision -->|deny control| deny_request
  execute_tool -->|operation state| operation_store
  execute_tool -->|reply control| timeout_decision
  timeout_decision -->|timeout control| reconcile_status
  timeout_decision -->|reply control| verify_result
  reconcile_status -->|completed data| verify_result
  reconcile_status -->|still running control| escalate
  verify_result -->|event state| write_audit
  escalate -->|escalation state| write_audit
  deny_request -->|denial state| write_audit
```

- `docs/diagrams/level1.png` is the three-block overview.
- `docs/diagrams/level2.png` is the component architecture.
- `docs/diagrams/level3.png` is the execution and recovery flow.
- Each level also has Mermaid, SVG and a text description.

Gold marks the local design. Blue marks behavior checked against a source.
