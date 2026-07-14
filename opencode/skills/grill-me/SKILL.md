---
name: grill-me
description: Conduct a user-invoked, decision-by-decision interview that turns an incomplete plan into an
  implementation-ready design without implementing it.
disable-model-invocation: true
---

# Grill Me

## Goal

Turn the user's plan into a coherent, implementation-ready design by resolving one decision at a time. Finish only when
the design is internally consistent, its material dependencies are resolved, and the remaining assumptions or open
questions are explicit. Do not implement anything during the interview.

## Prepare the Decision Tree

Before asking the first question:

1. Inspect relevant code, configuration, documentation, and tests when they can establish facts about the current system.
   Use read-only inspection and do not edit files or run mutating commands.
2. Separate facts discoverable from the repository from choices that require the user. Do not ask the user to choose
   something the available evidence already answers unless the plan proposes changing it.
3. Map the unresolved decisions in dependency order. Ask the earliest decision whose answer constrains later decisions.
4. Estimate the number of questions and use it as `y` in `Question x/y`. Treat `y` as a current estimate. If an answer
   reveals or removes material decisions, update `y` and briefly explain why.

## Ask One Decision at a Time

Ask exactly one unresolved decision per response. Do not skip ahead or combine independent decisions. You may explain
downstream consequences, but do not ask the user to decide them yet.

Use this structure for every question:

```markdown
## Question x/y: <decision>

### Concept
<Explain what is being decided and why it matters.>

### Example
<Show the smallest concrete example that clarifies the choice. Use a snippet, JSON, flow, or UI behavior when useful.>

### Options

- A. <option and practical effect>
- B. <option and practical effect>
- C. <option and practical effect>

### Recommendation
<Recommend one option and explain why it best fits the known goals and constraints.>

### Tradeoffs
<Compare the meaningful costs, risks, flexibility, and operational consequences.>

Which option do you choose, or what alternative should we consider?
```

Teach enough implementation mechanics for the user to make an informed choice, but keep the explanation focused on the
current decision. Make A, B, and C materially distinct. Accept a custom answer when none fits.

## Lock and Reconcile Decisions

After each answer:

1. Determine whether the current decision is resolved. If the answer is ambiguous, ask a clarification for the same
   decision and keep its question number.
2. Restate the resolved choice, its rationale, and its main implications as a locked decision.
3. Maintain and show a compact numbered list of all locked decisions before asking the next question.
4. Recalculate the remaining decision tree from the locked decisions and repository evidence.
5. If the answer suggests a better design, adapt the tree. Explicitly identify every affected locked decision, explain
   why it changed, and restate its replacement. Never revise a locked decision silently.
6. If a later answer conflicts with an earlier decision, revisit the earliest conflicting decision before proceeding.

Distinguish user choices from discovered constraints in the running record. Treat code as evidence of current behavior,
not as authority over the user's intended behavior.

## Stop Condition

End the interview when no material design decision remains unresolved. Provide a final design brief containing:

- the goal, success criteria, and non-goals;
- the complete locked-decision list;
- relevant components, interfaces, data flows, or UI behavior;
- failure behavior, edge cases, and validation expectations;
- explicit assumptions and any non-blocking open questions.

Do not create or modify implementation artifacts. If the user asks to implement during the interview, first confirm that
the interview is complete or that they want to end it early, then hand off the locked design as the implementation input.
