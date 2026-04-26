# Cairn Gate Labs — Documentation Index

## Repository structure

```
foundation/     Bedrock identity docs — rarely edited, changes require a decision record
strategy/       Living strategy — reviewed quarterly
decisions/      Append-only ADR log — why key decisions were made
canon/          Reference material — glossary, defined terms
```

## Foundation docs

| Doc | What it defines |
|---|---|
| [`foundation/CHARTER.md`](foundation/CHARTER.md) | What Cairn Gate is, isn't, and is building toward — start here |
| [`foundation/THESIS.md`](foundation/THESIS.md) | The core bet: bottleneck is systems, not model capability |
| [`foundation/TECHNICAL_PHILOSOPHY.md`](foundation/TECHNICAL_PHILOSOPHY.md) | How we build: stances, trade-offs, what we refuse |
| [`foundation/PRINCIPLES.md`](foundation/PRINCIPLES.md) | 10 operating principles — concrete and testable |
| [`foundation/VOICE.md`](foundation/VOICE.md) | Brand voice: do/don't pairs, example rewrites, banned phrases |

## Strategy docs

| Doc | What it covers |
|---|---|
| [`strategy/ARMS.md`](strategy/ARMS.md) | The six internal arms and their sequencing |
| [`strategy/IP_STRATEGY.md`](strategy/IP_STRATEGY.md) | IP posture: patent vs. trade secret, decision tree, asset map |

## Decision records

| ADR | Decision |
|---|---|
| [`decisions/0001-founding-structure.md`](decisions/0001-founding-structure.md) | Wyoming LLC over Delaware C-Corp |
| [`decisions/0002-brand-first-stealth.md`](decisions/0002-brand-first-stealth.md) | Brand-first operating model |

## Canon

| Doc | What it is |
|---|---|
| [`canon/GLOSSARY.md`](canon/GLOSSARY.md) | Defined terms used across all documentation |

## Conventions

- **Foundation** docs change via a numbered ADR committed to `decisions/` — no silent edits
- **Strategy** docs are free diffs, reviewed quarterly
- Every doc carries frontmatter: `layer`, `status`, `last_reviewed`, `review_cadence`
