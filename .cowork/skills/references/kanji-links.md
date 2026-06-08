---
name: kanji-links
description: >
  Authoritative reference for the kanji trainer link generation procedure used by
  fill-templates and update-templates skills.
---

# Kanji Trainer Links Reference

This file is the single source of truth for the kanji trainer link procedure.
Both `.cowork/skills/fill-templates.md` and `.cowork/skills/update-templates.md` defer here.

---

## What counts as a kanji

Only characters in Unicode range **U+4E00–U+9FFF** (CJK Unified Ideographs).

Hiragana, katakana, romaji, punctuation, and numbers do NOT produce links.

---

## Source text rule (per card type)

| Card type | Source text for kanji collection |
|-----------|----------------------------------|
| `#wc` (verb) | Value of the `ほんやく:` line only — strip furigana before collecting |
| `#wp` (adjective) | Value of the `ほんやく:` line only — strip furigana before collecting |
| `#w` (noun/expression) | The Japanese field line (second line of the block) — used as-is |

### Furigana stripping (for #wc and #wp)

Remove all furigana annotations before collecting kanji.
Two supported formats:
- `〇（〇）` — full-width parentheses: strip the `（reading）` part
- `〇(〇)` — ASCII parentheses: strip the `(reading)` part

After stripping, collect all U+4E00–U+9FFF characters from the remaining text.

---

## Link format

```
<a href="https://kanji-trainer.org/Mnemonic_phrase/Mnemonic_X.html">X</a>
```

Where `X` is the kanji character itself.

Example: 食 → `<a href="https://kanji-trainer.org/Mnemonic_phrase/Mnemonic_食.html">食</a>`

One `<a ...>` line per unique kanji.

---

## Deduplication

Per-template. First-occurrence order (left-to-right through the source text).
The same kanji appearing in multiple cards each gets its own link in each card — no cross-card deduplication.

---

## Placement

Link lines are placed:
- **After** the last conjugation/adjective form row (for `#wc` and `#wp`)
- **After** the Japanese field line (for `#w`)
- **Before** the `<!--ID: ...-->` line
- **Before** the blank separator line that follows the block

---

## No HTTP calls

Links are pure string construction. No web requests are needed or permitted.
