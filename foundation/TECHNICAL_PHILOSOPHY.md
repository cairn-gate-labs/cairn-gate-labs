---
layer: foundation
status: stable
last_reviewed: 2026-04-25
review_cadence: annual
---

# Cairn Gate Labs — Technical Philosophy

## Stance, not stack

These are positions, not preferences. A reasonable engineer could disagree with each one. That is the point.

**Correctness is a first-class deliverable.**
A system that works 80% of the time and fails silently the other 20% is not a system. It is a liability wearing a demo. We do not ship unless we can characterize the failure envelope.

**Legibility beats cleverness.**
The person who reads this code in 18 months is a stranger — possibly us. We write for that stranger. Abstractions earn their place by reducing total cognitive load, not by being elegant.

**Provenance is not optional in AI systems.**
Every output that matters should trace back to its source. Memory that cannot be audited is a guess dressed as knowledge. This shapes every architecture decision we make.

**Evaluation precedes deployment.**
We do not trust a system we cannot measure. Before something touches real data or a real user, we know what "working" means, what "broken" means, and how to tell the difference without human inspection of every case.

**The interface is part of the system.**
How a tool is invoked, what it surfaces, what it hides — these are architectural decisions, not UX polish. A powerful system with a bad interface produces bad decisions.

---

## The trade-off table

When two things conflict, here is where we stand:

| Axis | We favor | Why |
|---|---|---|
| Speed vs. rigor | Rigor, unless prototyping | Shortcuts in production compound; shortcuts in experiments are the point |
| Generality vs. specificity | Specificity first | We build for real problems. Generalize only when three cases demand it. |
| Novelty vs. boringness | Boringness in infrastructure | Boring infra frees up invention budget for the things that matter |
| Abstraction vs. directness | Directness until the abstraction earns it | Three concrete uses before any layer of indirection |
| Publish vs. protect | Protect first, publish selectively | IP is an asset. We do not give away architectures before we have filed or decided not to. |

---

## What we optimize for (ranked)

When these conflict, higher wins:

1. **Auditability** — can we explain what happened and why?
2. **Reliability** — does it work the same way every time under the same conditions?
3. **Utility** — does it actually solve the problem for the person using it?
4. **Efficiency** — does it do so without unnecessary cost, latency, or complexity?
5. **Elegance** — is it a pleasure to work with?

Elegance is last. It matters, but it never overrides the four above it.

---

## What we refuse

- **Shipping abstractions before we have three concrete uses.** One use case is a prototype. Two is a pattern. Three is a library.
- **Treating AI outputs as ground truth in evaluation pipelines.** LLM-as-judge is a tool; it is not a standard. We calibrate it against human judgment before we trust it.
- **Building on unstable dependencies for core functionality.** Wrapper-on-wrapper architectures collapse when one layer changes its API. Core logic owns its primitives.
- **Conflating velocity with progress.** Moving fast on the wrong problem is not a virtue. We stop and reframe before sprinting in a confirmed-wrong direction.
- **Publishing enabling details before IP protection is decided.** A public notebook is a public disclosure. We treat every technical write-up as a pre-patent risk until cleared.

---

## Worked example: memory architecture design

When we designed the cortical memory architecture, we had a choice: use an existing vector store pattern (fast, well-documented, standard), or build a multi-scale episodic/semantic/procedural layering that mirrors how human memory consolidates.

The trade-off table said: specificity first (the real problem is context reconstruction, not vector search), boring infrastructure (standard embedding models, standard storage), novel architecture (the consolidation and decay logic is the invention). The refusal list said: don't abstract until we have three uses. So the first version had no abstraction layer — just three concrete implementations against three different workflow types.

This is how we made the decision. Not by instinct. By applying the table.

---

## Open questions

Things this philosophy doesn't yet resolve:

- **When is an LLM the right interface vs. a deterministic system?** We have a bias toward determinism in infrastructure, but some problems are genuinely better served by probabilistic outputs. The line is not yet crisp.
- **How do we evaluate systems that improve with use?** Our evaluation-precedes-deployment principle is straightforward for static systems. For memory systems that learn, we need a richer evaluation framework that we are still developing.
- **What does "provenance-preserving" mean for generated content?** Tracing retrieved content back to a source is solved. Tracing synthesized content back to the reasoning chain that produced it is harder. We don't have a clean answer yet.

These are live research questions, not gaps in the philosophy. The philosophy tells us they matter. The work tells us how to resolve them.
