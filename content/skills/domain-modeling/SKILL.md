---
name: domain-modeling
description: Clarify domain terminology, boundaries, scenarios, and durable design decisions when the user is changing the domain model.
---

# Domain Modeling

Use this skill when the task changes the project's language or domain boundaries. Reading existing vocabulary for context
alone does not activate it.

## Model work

- Treat the glossary and code as evidence, not unquestionable authority. Surface contradictions and distinguish current
  behavior from intended behavior.
- Turn vague or overloaded terms into precise concepts. Test relationships with concrete scenarios, especially edge
  cases that expose boundary decisions.
- Keep the glossary free of implementation detail. Create or update `GLOSSARY.md` only when a term is settled, using
  [GLOSSARY-FORMAT.md](GLOSSARY-FORMAT.md). Create ADRs only for decisions that are hard to reverse, surprising
  without rationale, and based on a real trade-off; use [ADR-FORMAT.md](ADR-FORMAT.md).
- Write decisions when they become stable unless another active skill, such as `grill-me`, requires a read-only
  interview first. In that case, keep a visible record and persist settled updates when the interview closes.

Read the format file only when creating or updating that artifact. Keep domain language separate from implementation
specification.

<!--
Provenance only: Adapted from Matt Pocock's domain-modeling skill:
https://github.com/mattpocock/skills/tree/main/skills/engineering/domain-modeling
Do not open or consult the upstream skill when applying this local skill; this version is authoritative.
-->
