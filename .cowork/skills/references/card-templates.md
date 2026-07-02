---
name: card-templates
description: >
  Canonical card block definitions and label alias table used by templates-update
  to detect and repair field name variants in existing lesson files.
---

# Card Templates Reference

This file is the single source of truth for:
1. The canonical block structure for each card type (`#wc`, `#wp`, `#w`)
2. The label alias table mapping known variant spellings to canonical labels

Both `.cowork/skills/fill-templates.md` and `.cowork/skills/templates-update.md` defer here.

---

## Canonical #wc (verb) template

```
[Polish translation] [#k] #card
ほんやく: [japanese expression with furigana]
て形: [value]
た形: [value]
ます形: [value]
出す形 (start): [value]
そう (looks like): [value]
お〜になる (honorific): [value]
ない形: [value]
なかった形: [value]
あれる形 (passive):  [value]
使役形 (make/let): [value]
尊敬語 (honorific): [value]
ば形 (if): [value]
可能形 (can): [value]
おう形 (let's): [value]
<a href="https://kanji-trainer.org/Mnemonic_phrase/Mnemonic_X.html">X</a>
<!--ID: ...-->
```

Notes:
- The 14 form lines appear in the exact order above.
- One `<a href>` line per unique CJK kanji in the `ほんやく:` value (furigana stripped).
- `<!--ID: ...-->` is the last non-blank line of the block, after all links.
- Suru verbs (`する` in ほんやく: value) have no form lines — block ends at ほんやく: line.

---

## Canonical #wp (adjective) template

```
[Polish translation] [#k] #card
ほんやく: [japanese expression with furigana]
過去形: [value]
否定形: [value]
副詞形: [value]
そう (looks like): [value]
<a href="https://kanji-trainer.org/Mnemonic_phrase/Mnemonic_X.html">X</a>
<!--ID: ...-->
```

Notes:
- The 4 form lines appear in the exact order above.
- One `<a href>` line per unique CJK kanji in the `ほんやく:` value (furigana stripped).
- `<!--ID: ...-->` is the last non-blank line of the block, after all links.

---

## Canonical #w (noun/expression) template

```
[Polish translation] [#k] #card
[japanese expression with furigana]
<a href="https://kanji-trainer.org/Mnemonic_phrase/Mnemonic_X.html">X</a>
<!--ID: ...-->
```

Notes:
- No `ほんやく:` line — the second line is the Japanese field directly.
- One `<a href>` line per unique CJK kanji in the Japanese field line.
- `<!--ID: ...-->` is the last non-blank line of the block, after all links.

---

## Label alias table

See `.cowork/skills/references/label-aliases.json`.
