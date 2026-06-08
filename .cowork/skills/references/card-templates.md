---
name: card-templates
description: >
  Canonical card block definitions and label alias table used by update-templates
  to detect and repair field name variants in existing lesson files.
---

# Card Templates Reference

This file is the single source of truth for:
1. The canonical block structure for each card type (`#wc`, `#wp`, `#w`)
2. The label alias table mapping known variant spellings to canonical labels

Both `.cowork/skills/fill-templates.md` and `.cowork/skills/update-templates.md` defer here.

---

## Canonical #wc (verb) template

```
[Polish translation] [#k] #card
ほんやく: [japanese expression with furigana]
ます形: [value]
て形: [value]
た形: [value]
ない形: [value]
なかった形: [value]
ば形 (if): [value]
可能形 (can): [value]
られる形 (is done by): [value]
出す形 (start): [value]
尊敬語 (honorific): [value]
お〜になる (honorific): [value]
そう (looks like): [value]
おう (let's): [value]
<a href="https://kanji-trainer.org/Mnemonic_phrase/Mnemonic_X.html">X</a>
<!--ID: ...-->
```

Notes:
- The 13 form lines appear in the exact order above.
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
そう: [value]
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

This table maps known variant label spellings to their canonical form.
Used by **Repair 1** in update-templates.

| Variant | Canonical |
|---------|-----------|
| `Tłumaczenie:` | `ほんやく:` |
| `translation:` | `ほんやく:` |
| `ほんやく：` (full-width colon) | `ほんやく:` |
| `te-form:` | `て形:` |
| `て-form:` | `て形:` |
| `ta-form:` | `た形:` |
| `た-form:` | `た形:` |
| `negative:` | `ない形:` |
| `nai-form:` | `ない形:` |
| `past negative:` | `なかった形:` |
| `past-negative:` | `なかった形:` |
| `conditional:` | `ば形 (if):` |
| `ba-form:` | `ば形 (if):` |
| `potential:` | `可能形 (can):` |
| `passive:` | `られる形 (is done by):` |
| `inceptive:` | `出す形 (start):` |
| `honorific:` | `尊敬語 (honorific):` |
| `volitional:` | `おう (let's):` |
| `ou-form:` | `おう (let's):` |
| `looks like:` | `そう (looks like):` |
| `sou:` | `そう (looks like):` |
| `past:` | `過去形:` |
| `past form:` | `過去形:` |
| `negative form:` | `否定形:` |
| `adverb:` | `副詞形:` |
| `adverbial:` | `副詞形:` |

### Usage rules for the alias table

1. Match is case-sensitive for Japanese labels; case-insensitive for romaji/Latin variants.
2. Strip leading/trailing whitespace from the label before matching.
3. If a variant matches an alias entry, replace only the label; preserve the value after the colon verbatim (including leading space).
4. If a label does not appear in the alias table, attempt positional matching (see Repair 1 in update-templates.md). If positional matching is also inconclusive, do not rename — flag for user review.
5. This table is not exhaustive. When a new variant is discovered in a real lesson file, add it here and apply the rename.
