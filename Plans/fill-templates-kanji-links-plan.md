# Plan: fill-templates kanji trainer links

## Goal
After filling all conjugation/adjective fields for each template card, append one kanji-trainer.org link per unique CJK kanji found in that card's completed text.

## Scope
File: `.cowork/skills/fill-templates.md`

## Behaviour spec

### Trigger
Inline, during the fill pass for each template — not a separate post-pass.

### What counts as a kanji
Unicode range U+4E00–U+9FFF (CJK Unified Ideographs). No other character classes.

### Link format
```
<a href="https://kanji-trainer.org/Mnemonic_phrase/Mnemonic_X.html">X</a>
```
where `X` is the kanji character itself (e.g. `食` → `Mnemonic_食.html`).

### Placement
Immediately below the last conjugation/adjective row of the template, before the blank line that separates it from the next card. One link per line.

### Ordering
By first occurrence of the kanji in the completed template text (left-to-right, top-to-bottom).

### Deduplication scope
Per-template. The same kanji may appear in links for multiple cards — each card is standalone for Anki review, so no cross-card deduplication.

### HTTP calls
None required. Links are pure string construction.

## Implementation steps

1. Read the current `fill-templates.md` skill to locate the section that describes how Claude fills each template.
2. Add a rule (or extend the existing fill rule) that, after all fields of a template are written:
   a. Collect every character in the completed template text.
   b. Filter to those in U+4E00–U+9FFF.
   c. Deduplicate while preserving first-occurrence order.
   d. For each kanji, produce: `<a href="https://kanji-trainer.org/Mnemonic_phrase/Mnemonic_X.html">X</a>`
   e. Append those lines (one per kanji) immediately after the last row of that template.
3. Ensure the blank line separating cards is still present after the link block.
4. Update any example output in the skill to reflect the new link lines.

## Example (before / after)

### Before
```
#wc 食べる(たべ) - to eat
食べます / 食べません / 食べました / 食べませんでした
食べて / 食べない / 食べれば / 食べよう / 食べろ
食べられる / 食べさせる / 食べさせられる

```

### After
```
#wc 食べる(たべ) - to eat
食べます / 食べません / 食べました / 食べませんでした
食べて / 食べない / 食べれば / 食べよう / 食べろ
食べられる / 食べさせる / 食べさせられる
<a href="https://kanji-trainer.org/Mnemonic_phrase/Mnemonic_食.html">食</a>
<a href="https://kanji-trainer.org/Mnemonic_phrase/Mnemonic_べ.html">べ</a>

```
Note: `べ` is hiragana (not in U+4E00–U+9FFF), so it would NOT appear — only `食` would. The above "after" example correctly shows only `食`.

## Acceptance criteria
- Each filled template ends with exactly one `<a …>` line per unique kanji (U+4E00–U+9FFF) found in that template's text, ordered by first occurrence.
- No link appears for hiragana, katakana, romaji, or punctuation.
- The blank separator line between cards is preserved after the link block.
- No HTTP requests are made during the fill pass.
- Deduplication is per-template only.
