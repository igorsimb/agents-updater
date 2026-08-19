---
name: humanize-text
description: User-invoked only. Polish completed technical prose that sounds mechanically generated while preserving
  technical meaning and the author's voice.
---

# Humanize Text

Use this only when the user explicitly invokes it. Apply it as a final linguistic pass on completed technical prose.
Preserve the author's meaning, facts, caveats, numbers, terminology, degree of certainty, and voice.

Do not draft new material, broadly restructure the piece, add examples or opinions, or make the writing more literary,
casual, corporate, or polished.

## Workflow

1. Read the complete source before editing. Identify its intended tone and the technical terms that must remain stable.
2. Scan for the patterns below. Treat them as diagnostic signals, not automatic errors or banned words.
3. Make the smallest revisions that improve clarity and cadence.
4. Compare the revision with the source. Restore anything that changes a fact, qualification, number, attribution,
   technical term, or degree of certainty.
5. Read the revision once for natural rhythm. Fix remaining mechanical patterns without smoothing away the author's
   voice.

## Editing Focus

- Replace abstract summaries with concrete system behavior when the draft supports it.
- Prefer direct verbs over noun-heavy phrasing.
- Remove transitions and framing that add no meaning, such as "Additionally," "Moreover," "It is worth noting," "In order to," and "Overall."
- Remove puffery, promotional wording, and unsupported intensifiers. Keep an adjective or adverb when it has a precise
  technical meaning or the draft supports it with evidence.
- Rewrite superficial participial tails such as "ensuring," "highlighting," or "showcasing" when they imply a result
  without explaining one. Delete the tail if it adds no meaning.
- Prefer plain verbs over inflated substitutes such as "serves as," "stands as," "utilizes," and metaphorical
  "leverages." Do not replace established domain terminology merely because it sounds formal.
- Rewrite formulaic contrasts such as "it is not X, it is Y" and "it is Y, not X" when a direct statement preserves the
  distinction. Keep the contrast when the opposition itself carries technical meaning.
- Remove reader-directed setup such as "imagine..." and vague comparison phrases such as "that feels like" or "it is
  like..." State the concrete behavior instead. Do not invent a replacement metaphor.
- Replace em dashes with punctuation that fits the sentence, such as a period, comma, colon, or parentheses.
- Break repetitive sentence patterns, forced groups of three, or balanced lists only when they make the prose sound
  mechanical. Use the number of points the content actually requires.
- Keep one term for one concept. Do not cycle through synonyms merely to avoid repetition.
- Rewrite "from X to Y" when the endpoints do not describe a meaningful range.
- Collapse stacked hedges to one calibrated term when it preserves the same uncertainty. Never strengthen a claim by
  removing meaningful caution.
- Prefer active voice when the actor is known and naming it improves the sentence. Keep passive voice when the actor is
  unknown, irrelevant, or intentionally deemphasized.
- Split a dense sentence when a reader must backtrack to parse it. Do not enforce one idea per sentence or turn the
  passage into a sequence of clipped statements.
- Remove generic conclusions that add sentiment but no result, decision, limitation, or next step.
- Use the project-swap test as a diagnostic: if a sentence could appear unchanged in unrelated project documentation,
  check whether it says anything specific here. Tighten it only with facts already present in the source.
- Keep slight unevenness when it reflects natural technical reasoning: a short sentence after a dense explanation, or a direct statement beside a longer one.
- Preserve useful bluntness, restraint, dry humor, and repetition when they already belong to the author's voice.
- Keep a precise sentence even when it is less smooth. Technical accuracy takes priority.

## Boundaries

- Do not add facts, benchmarks, claims, examples, metaphors, or personality.
- Do not remove technical detail or caveats.
- Do not remove or invent attribution. If an attribution is vague, preserve the claim unless the source supports a more
  precise version.
- Do not make the text longer except for a small change needed to keep a revision natural.
- Do not rewrite whole paragraphs merely to vary rhythm.
- Do not make prose vague, casual, or theatrical in the name of sounding human.
- Do not replace simple wording with clever wording.
- Do not treat individual words, punctuation, passive voice, or sentence length as proof that prose is mechanical.

## Examples

These examples isolate linguistic transformations. Assume every concrete detail in a revision is supported elsewhere
in the source. Copy the transformation pattern, not the facts. Never infer a mechanism, metric, or event from an
abstract sentence or metaphor alone.

Abstract:

> The change improved efficiency and reduced complexity.

Concrete:

> The change removed an extra model hop and sent less prompt context on simple turns.

Noun-heavy:

> The implementation of routing logic enabled optimization of lightweight requests.

Direct:

> The routing logic made lightweight requests cheaper.

Overly balanced:

> The app kept one shared runtime, preserved conversation history, and maintained the existing safety checks.

More natural:

> The app still used one shared runtime and kept the same conversation history. The safety checks stayed where they were.

Formulaic contrast:

> This is not a routing problem, it is a prompt-selection problem.

Direct:

> The router works. The prompt selector chooses the wrong prompt.

Decorative comparison:

> That felt like securing the front door and leaving the window open.

Concrete:

> The endpoint required authentication, but the debug route remained public.

## Final Check

Scan the revised prose for empty framing, formulaic contrasts, unsupported intensifiers, superficial participial tails,
synonym cycling, false ranges, stacked hedges, vague comparisons, generic conclusions, repetitive cadence, and em
dashes. Remove or rewrite them under the rules above.

Then compare the source and revision once more. The result must retain the same technical meaning, evidence,
uncertainty, and authorial voice. If natural cadence conflicts with technical precision, keep the precision.
