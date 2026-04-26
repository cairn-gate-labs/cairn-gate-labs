---
id: 0001
date: 2026-04-24
status: decided
---

# ADR 0001 — Founding Structure: Wyoming Single-Member LLC

## Context

Needed a legal entity to hold contracts, revenue, expenses, IP, and a bank account. Considered Wyoming LLC, Delaware LLC, Delaware C-Corp, Washington LLC.

## Decision

Wyoming single-member LLC (Cairn Gate Labs LLC), registered 2026-04-24 via Northwest Registered Agent.

## Consequences

- Pass-through taxation (federal income treated as owner's, not separate entity)
- WA B&O tax applies on gross receipts regardless of profit
- No liability separation between internal arms (Advisory, Systems, etc.) — they are accounting divisions, not legal entities
- Spin-out to separate entities triggered only by: outside capital, co-founder economics, major liability exposure, product with clean cap table need

## Alternatives considered

- **Delaware C-Corp** — only makes sense for institutional fundraising; adds board requirements and double taxation. Revisit if venture-scale ambition develops.
- **Washington LLC** — less privacy than Wyoming; personal address harder to keep off record.
- **Delaware LLC** — reasonable alternative; Wyoming cheaper, stronger privacy, no state income tax.

## Why Wyoming over Delaware

- Privacy: Northwest's address on public filings, not owner's
- Cost: ~$200/yr vs. ~$300+/yr for Delaware
- No state income tax
- Can domesticate to Delaware later (~$200-300, same EIN) if fundraising intent changes
