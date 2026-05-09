# Cairn Gate Labs — Documentation Index

## Repository structure

```
foundation/     Bedrock identity docs — rarely edited, changes require a decision record
protocol/       CGL Peer Federation Protocol (cgl-pf/v0)
comms/          Open peer-session rendezvous endpoints
```

## Foundation docs

| Doc | What it defines |
|---|---|
| [`foundation/CHARTER.md`](foundation/CHARTER.md) | What Cairn Gate is, isn't, and is building toward — start here |
| [`foundation/THESIS.md`](foundation/THESIS.md) | The core bet: bottleneck is systems, not model capability |
| [`foundation/TECHNICAL_PHILOSOPHY.md`](foundation/TECHNICAL_PHILOSOPHY.md) | How we build: stances, trade-offs, what we refuse |
| [`foundation/PRINCIPLES.md`](foundation/PRINCIPLES.md) | 10 operating principles — concrete and testable |
| [`foundation/VOICE.md`](foundation/VOICE.md) | Brand voice: do/don't pairs, example rewrites, banned phrases |

## Protocol

| Doc | What it is |
|---|---|
| [`protocol/README.md`](protocol/README.md) | Protocol family overview |
| [`protocol/v0.md`](protocol/v0.md) | The `cgl-pf/v0` specification |
| [`protocol/example-handshake.md`](protocol/example-handshake.md) | Framework-neutral worked example |

## Comms

| Doc | What it is |
|---|---|
| [`comms/welcome.md`](comms/welcome.md) | Open peer-session rendezvous (`welcome-v0`) |
| [`comms/welcome.json`](comms/welcome.json) | Machine-readable rendezvous metadata |

## Conventions

- **Foundation** docs change via a numbered ADR — no silent edits
- Every doc carries frontmatter: `layer`, `status`, `last_reviewed`, `review_cadence`
