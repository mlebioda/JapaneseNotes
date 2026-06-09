---
name: kanji-links
description: >
  Authoritative reference for the kanji trainer link generation procedure used by
  fill-templates and templates-update skills.
---

# Kanji Trainer Links Reference

This file is the single source of truth for the kanji trainer link procedure.
Both `.cowork/skills/fill-templates.md` and `.cowork/skills/templates-update.md` defer here.

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

---

## Script usage

A helper script is provided at `.cowork/scripts/kanji-links.py` to generate the link lines mechanically.

The caller must strip furigana from the source text before passing it (the script does not strip furigana itself).

```bash
python3 .cowork/scripts/kanji-links.py "<source_text>"
```

Using the vault-root-relative path from any working directory:

```bash
python3 "/Users/michallebioda/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianJP/.cowork/scripts/kanji-links.py" "<source_text>"
```

The script prints one `<a href>` line per unique kanji (U+4E00–U+9FFF only, first-occurrence order) to stdout, ready to paste as the link block in a card. If no kanji are found, output is empty (exit code 0).
