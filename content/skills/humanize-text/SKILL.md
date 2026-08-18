---
name: humanize-text
description: Use when polishing completed technical prose that sounds mechanically generated. Preserve technical meaning and the author's voice while removing artificial phrasing and cadence.
---

# Humanize Text

Use this as a final editorial pass on completed technical prose. Preserve the author's meaning, facts, caveats, numbers, and voice.

Do not draft new material, restructure the piece, add examples or opinions, or make the writing more literary, casual, corporate, or polished.

## Editing Focus

- Replace abstract summaries with concrete system behavior when the draft supports it.
- Prefer direct verbs over noun-heavy phrasing.
- Remove transitions and framing that add no meaning, such as "Additionally," "Moreover," "It is worth noting," "In order to," and "Overall."
- Rewrite formulaic contrasts such as "it is not X, it is Y" and "it is Y, not X" when a direct statement preserves the
  distinction. Keep the contrast when the opposition itself carries technical meaning.
- Remove reader-directed setup such as "imagine..." and vague comparison phrases such as "that feels like" or "it is
  like..." State the concrete behavior instead. Do not invent a replacement metaphor.
- Replace em dashes with punctuation that fits the sentence, such as a period, comma, colon, or parentheses.
- Break repetitive sentence patterns or balanced lists only when they make the prose sound mechanical.
- Keep slight unevenness when it reflects natural technical reasoning: a short sentence after a dense explanation, or a direct statement beside a longer one.
- Preserve useful bluntness, restraint, dry humor, and repetition when they already belong to the author's voice.
- Keep a precise sentence even when it is less smooth. Technical accuracy takes priority.

## Boundaries

- Do not add facts, benchmarks, claims, examples, metaphors, or personality.
- Do not remove technical detail or caveats.
- Do not make the text longer except for a small change needed to keep a revision natural.
- Do not rewrite whole paragraphs merely to vary rhythm.
- Do not make prose vague, casual, or theatrical in the name of sounding human.
- Do not replace simple wording with clever wording.

## Examples

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

Scan the revised prose for formulaic contrasts, reader-directed "imagine" framing, vague comparison phrases, and em
dashes. Remove or rewrite them under the rules above. The revised text should retain the same technical meaning and
authorial voice while sounding less mechanically even. If natural cadence conflicts with technical precision, keep the
precision.
