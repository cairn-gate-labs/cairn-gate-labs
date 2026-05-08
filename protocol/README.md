# CGL Peer Federation Protocol

A small protocol for bounded conversations between independent agents
from different organizations.

This directory holds the public protocol documents.

| File | What it is |
|---|---|
| [`v0.md`](v0.md) | The `cgl-pf/v0` specification (RFC-style, ~600 lines). |
| [`example-handshake.md`](example-handshake.md) | A framework-neutral worked example showing the minimum compliant peer (pure HTTP + WebSocket + Ed25519). |

## Quick read

If you only have ten minutes, read the spec's table of contents and
§5 (Discovery) and §6 (Handshake). Those are the load-bearing wire
shapes; everything else is framing and edge cases.

If you are wiring an existing agent up to this protocol, read the
spec to know what your code must do, then mirror the worked example
in your language. The example is ~200 lines of pseudocode and uses
no framework or SDK.

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

The protocol identifier is `cgl-pf/v0`. v0 is published as-is and
is wire-frozen — minor revisions (e.g. `cgl-pf/v0.1`) MUST be
wire-compatible additions.

A future major version (`cgl-pf/v1`) is not wire-compatible with
v0 and would be published as a separate document.

## License

- Specification text: CC BY 4.0
- Example code: MIT

Implementations of this protocol are not derivative works of the
specification or example.
