# References and provenance

## Dependencies

- mcp: local MCP client and server. License MIT.
- pyyaml: policy file. License MIT.
- pytest: tests. License MIT.

## Documented facts

- The installed mcp 2.3.0 package exposes MCPServer and a stdio ClientSession.call_tool timeout.

## Proposed decisions

- The simulated service writes the operation result before the delayed reply.
- The operation id is a hash of the actor, tool and idempotency key.
- MOCK design note. This is not live research.

## Sources

- Installed MCP SDK interface (MIT) hash 176f2b4e68e901557b74fd9f35da03ead91679db649300e38992eb79c25ad782
- Untrusted instruction fixture (unknown) hash a8e0010de6f26bf54d8ca7774cf3af590986b2042c5e290a8ce3e9025b046b43

Private sources are not copied into this project.
External repositories were not copied.
