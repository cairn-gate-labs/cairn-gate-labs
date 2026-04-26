---
layer: strategy
status: evolving
last_reviewed: 2026-04-25
review_cadence: quarterly
---

# Cairn Gate Labs — IP Strategy

## The posture

IP is a portfolio, not a checkbox. We do not patent everything. We do not publish everything. The decision tree matters more than the default.

---

## Decision tree for any invention

```
New technical mechanism developed
        ↓
Is it novel and non-obvious?
    No → Document as internal know-how / trade secret
    Yes ↓
Is it close to Meta's business or R&D (AI, ads, infra, ranking, agents, data)?
    Yes → Get IP counsel review + Meta conflicts guidance BEFORE any filing or publication
    No ↓
Is it commercially central and hard to keep secret?
    Yes → Provisional patent application (12-month window, no formal claims)
    No → Trade secret (document, protect, don't publish)
        ↓
After provisional: file non-provisional or abandon?
    Commercially central + defensible claims → non-provisional
    Otherwise → let lapse, protect as trade secret
```

---

## Clean-room requirements (non-negotiable)

- Personal laptop only. No Meta devices.
- Personal accounts only. No Meta accounts, email, or cloud.
- No Meta code, snippets, internal tools, libraries, or documentation.
- No Meta data, logs, examples, benchmarks, or prompts.
- No work time. No employer-derived examples.
- Separate invention log and repository, date-stamped from day one.
- Document: what you conceived, what the AI tool suggested, what you selected/rejected, what you implemented, what experiments showed.

---

## Asset map

| Asset | Protection mode | Notes |
|---|---|---|
| Cairn Gate brand | Trademark | USPTO search before heavy investment |
| Memory architecture (cortical model) | Patent candidate + trade secret (implementation) | Provisional before any public write-up |
| Retrieval governance methods | Trade secret or patent | Depends on specificity and novelty |
| Evaluation harnesses | Trade secret | Operational know-how; unlikely to patent |
| Client workflow IP | Contract-defined | SOW/MSA defaults: client owns their data; Cairn retains method rights |
| Briefs / playbooks | Copyright | Automatic; register for enforcement leverage |
| Code / systems | Copyright + trade secret | Written assignment from any contractors |

---

## Contractor rule

All contractors must sign a written IP assignment before any work begins. The U.S. Copyright Office is clear: works made for hire require express written agreement for commissioned works outside regular employment. Assume nothing transfers without a signed document.

---

## Publication rule

Invention memo → IP decision → ONLY THEN publish anything enabling.

A "Cairn Gate Brief" on a technical topic is a public disclosure. We treat every technical write-up as a pre-patent risk until the IP posture is decided. Non-enabling descriptions (what the system does, not how it works) can publish earlier.

---

## Cortical memory architecture — current status

Status: in development. No filing yet. Invention log started.

Key zones with potential:
- Memory consolidation (episodic → semantic → procedural)
- Retrieval governance (policy-gated, provenance-aware)
- Temporal decay and contradiction resolution
- Context reconstruction for specific workflow types
- Privacy-aware memory promotion

Next step: prior-art search + IP counsel consultation before any public write-up.
