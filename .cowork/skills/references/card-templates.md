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
そう (looks): [value]
お〜になる/special verb (honorific): [value]
ない形: [value]
なかった形: [value]
あれる形 (passive/honorific):  [value]
使役形 (make/let): [value]
ば形 (if): [value]
可能形 (can): [value]
おう形 (let's): [value]
命令形 (imperative): [value]
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
そう (looks): [value]
お/ご (honorific): [value]  ← optional, only when a natural honorific form exists
<a href="https://kanji-trainer.org/Mnemonic_phrase/Mnemonic_X.html">X</a>
<!--ID: ...-->
```

Notes:
- The 4 form lines appear in the exact order above.
- `お/ご (honorific):` is an optional 5th/last form line, appended after そう (looks)
  only when eligible and a natural お/ご form exists. See
  `.cowork/skills/references/honorific-forms.md` for eligibility, exclusions, and
  value-format rules. Omitted entirely (not a dash) when no natural form exists.
- One `<a href>` line per unique CJK kanji in the `ほんやく:` value (furigana stripped).
- `<!--ID: ...-->` is the last non-blank line of the block, after all links.

---

## Canonical #w (noun/expression) template

```
[Polish translation] [#k] #card
[japanese expression with furigana]
お/ご (honorific): [value]  ← optional, only when a natural honorific form exists
<a href="https://kanji-trainer.org/Mnemonic_phrase/Mnemonic_X.html">X</a>
<!--ID: ...-->
```

Notes:
- No `ほんやく:` line — the second line is the Japanese field directly.
- `お/ご (honorific):` is an optional 3rd line, appended immediately after the Japanese
  field line only when eligible and a natural お/ご form exists. See
  `.cowork/skills/references/honorific-forms.md` for eligibility, exclusions, and
  value-format rules (including the `(する)`-dropping rule for suru-noun entries).
  Omitted entirely (not a dash) when no natural form exists.
- One `<a href>` line per unique CJK kanji in the Japanese field line.
- `<!--ID: ...-->` is the last non-blank line of the block, after all links.

---

## Label alias table

See `.cowork/skills/references/label-aliases.json`.
