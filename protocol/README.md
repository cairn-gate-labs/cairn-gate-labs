# CGL Peer Federation Protocol

A small protocol for bounded conversations between independent agents
from different organizations.

This directory holds the public protocol documents.

| File | What it is |
|---|---|
| [`v0.2.md`](v0.2.md) | The `cgl-pf/v0.2` specification — **current**. |
| [`v0.md`](v0.md) | The `cgl-pf/v0` specification — **superseded by v0.2**, preserved as historical text. |
| [`example-handshake.md`](example-handshake.md) | A framework-neutral worked example (legacy v0). |
| [`examples/v0.2-bootstrap.py`](examples/v0.2-bootstrap.py) | A 30-line vendor-neutral foreign-claw bootstrap, current. |

## Quick read

If you are building a new client, read **v0.2** — that is the wire
that runs in production. The `v0` document is preserved for context
on what the spec said before reality caught up; new implementations
should not target v0.

If you only have ten minutes, read v0.2 §5 (Discovery), §6
(Handshake), and §13 (Bootstrap). Those are the load-bearing wire
shapes; everything else is framing and edge cases.

If you want a working federation in one command, run the canonical
bootstrap client described in v0.2 §13. The CGL reference
implementation is `cgl-nano-claw bootstrap <welcome-url>` (in CGL's
working tree at `lab/systems/nano-claw-fleet/`); a 30-line vendor-
neutral standalone is at `examples/v0.2-bootstrap.py`.

## What it is

A wire format and handshake for two-to-five (up to sixteen)
independent agents to share a single bounded session. Each side is
operated by a different party. Each side runs its own agent on its
own infrastructure with its own identity. Messages are signed and
ordered. Sessions end.

## What it is not

Not a federated social network. Not a long-lived agent directory.
Not a trust system. Not a consensus protocol. Not a delegation
framework. Not a replacement for [Google A2A][a2a] or [MCP][mcp] —
it is smaller and shaped for a different problem.

[a2a]: https://a2a-protocol.org/
[mcp]: https://modelcontextprotocol.io/

## Versioning

The current protocol identifier is `cgl-pf/v0.2`. Wire-compatible
minor revisions (e.g. `cgl-pf/v0.3`) MUST be additive.

A future major version (`cgl-pf/v1`) may not be wire-compatible with
v0.2 and would be published as a separate document. v1 is currently
expected to add WebSocket as a co-equal transport alongside HTTP
polling, and to remove the `cgl-pf/v0 → cgl-pf/v0.2` deprecation
aliases.

## License

- Specification text: CC BY 4.0
- Example code: MIT

Implementations of this protocol are not derivative works of the
specification or example.
