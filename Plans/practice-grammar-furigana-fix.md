# practice-grammar furigana rule strengthening

## Goal
Strengthen the furigana rule in `.cowork/skills/practice-grammar.md` so Claude reliably adds furigana to every kanji in every part of every exercise output — including compound words that were being skipped in practice (e.g. 来年, 日本語).

## Approach
Replace only line 113 with a rewritten version that keeps all existing mandatory/no-exceptions language, adds an explicit negative example showing the real failure mode (compound words without furigana), adds a paired positive example showing the correct form, and explicitly lists every output location the rule covers. No other lines or files change.

## Steps
1. Open `.cowork/skills/practice-grammar.md`.
2. Replace line 113 exactly. The current text is:

```
**Furigana rule — mandatory.** Every kanji character that appears in an exercise (sentence, prompt, choices, fragments, hint text) **must** have furigana. Use vault inline style: kanji immediately followed by the reading in full-width parentheses, e.g. `名刺（めいし）`, `病院（びょういん）`, `食（た）べる`. Before outputting each exercise, scan every kanji in it and verify furigana is present — no exceptions, including words from the vocab pool, example sentences, and grammar point context.
```

   Replace it with:

```
**Furigana rule — mandatory.** Every kanji character that appears anywhere in the exercise output **must** have furigana — no exceptions. This applies to every location: question text, answer options, feedback lines, hint text, example sentences, grammar-point context, and vocabulary pool words. Use vault inline style: kanji immediately followed by the reading in full-width parentheses, e.g. `名刺（めいし）`, `病院（びょういん）`, `食（た）べる`. Compound words are the most common failure point — every kanji in the compound needs its own reading. ✗ `来年、日本語の試験（しけん）を…` — 来年 and 日本語 are missing furigana. ✓ `来年（らいねん）、日本語（にほんご）の試験（しけん）を…` — every kanji covered. Before outputting each exercise, scan every kanji in every line and verify furigana is present.
```

3. Save the file.

## Risks
- This is a single-line text replacement in the skill's instruction block. No ID lines, no Summary section, and no plugin-generated content are involved — risk of data loss is zero.
- The change tightens an existing rule; it does not alter exercise types, SM-2 logic, or state format, so no existing progress data is affected.
