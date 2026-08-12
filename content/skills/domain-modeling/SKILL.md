---
name: domain-modeling
description: Build and sharpen a project's domain model. Use when the user wants to pin down domain terminology or a ubiquitous language, record an architectural decision, or when another skill needs to maintain the domain model.
---

# Domain Modeling

Actively build and sharpen the project's domain model as you design. This is the *active* discipline — challenging 
terms, inventing edge-case scenarios, and writing the glossary and decisions down the moment they crystallize. 
(Merely *reading* `GLOSSARY.md` for vocabulary is not this skill — that's a one-line habit any skill can do. This skill 
is for when you're changing the model, not just consuming it.)

## File structure

Most repos have a single glossary:

```
/
├── GLOSSARY.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
```

If a `GLOSSARY-MAP.md` exists at the root, the repo has multiple glossaries. The map points to where each one lives:

```
/
├── GLOSSARY-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
│── ordering/
│   ├── GLOSSARY.md
│   └── docs/adr/                 ← glossary-specific decisions
│── billing/
│   ├── GLOSSARY.md
│   └── docs/adr/
```

Create files lazily — only when you have something to write. If no `GLOSSARY.md` exists, create one when the first 
term is 
resolved. If no `docs/adr/` exists, create it when the first ADR is needed.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `GLOSSARY.md`, call it out immediately. "Your 
glossary defines 'cancellation' as X, but you seem to mean Y — which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account' — do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible — which is right?"

### Update GLOSSARY.md inline

When a term is resolved, update `GLOSSARY.md` right there. Don't batch these up — capture them as they happen. Use the 
format in [GLOSSARY-FORMAT.md](GLOSSARY-FORMAT.md).

When this skill is active with `grill-me`, its interview boundary takes precedence over the timing of file writes, not
over domain-modeling work. Continue challenging terms, testing scenarios, checking code, and recording every settled
term or decision in `grill-me`'s visible locked-decision record. Queue the corresponding glossary or ADR update while
questions remain. As soon as `grill-me` reaches its stop condition and explicitly closes the interview, persist all
settled queued updates before the final handoff. Do not persist unresolved candidates, and do not treat the deferred
write as permission to defer domain clarification.

`GLOSSARY.md` should be totally devoid of implementation details. Do not treat `GLOSSARY.md` as a spec, a scratch pad, 
or a 
repository for implementation decisions. It is a glossary and nothing else.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without rationale** — a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Use the format in [ADR-FORMAT.md](ADR-FORMAT.md).

<!--
Provenance only: Adapted from Matt Pocock's domain-modeling skill:
https://github.com/mattpocock/skills/tree/main/skills/engineering/domain-modeling
Do not open or consult the upstream skill when applying this local skill; this version is authoritative.
-->
