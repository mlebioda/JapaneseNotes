---
name: honorific-forms
description: >
  Authoritative reference for the #w / #wp お/ご (honorific) row: eligibility,
  already-prefixed exclusions, prefix choice, value format, and placement.
  Used by fill-templates and templates-update skills.
---

# Honorific (お/ご) Forms Reference — #w and #wp

This file is the single source of truth for the optional `お/ご (honorific):` row on
`#w` (noun/expression/sentence) and `#wp` (adjective) cards. Both
`.cowork/skills/fill-templates.md` and `.cowork/skills/templates-update.md` defer here.

**`#wc` (verb) cards are never eligible for this row.** Verbs have their own distinct
`お〜になる/special verb (honorific)` field — a different mechanism (verb-stem + になる
derivation, not a noun/adjective prefix), governed entirely by
`references/verb-conjugation.md` and the separate `Plans/wc-honorific-special-verb-plan.md`.
This file does not apply to `#wc` in any way.

---

## Eligibility

### `#w` (noun/expression/sentence)

Eligible only if the Japanese field (furigana stripped) is a **bare noun**:
- No particles (は, が, を, に, で, と, の, へ, も, etc.).
- Not a conjugated verb or adjective ending.
- Suru-noun entries (e.g. `入院(にゅういん)(する)`) still count as bare nouns — the
  trailing `(する)` does not disqualify them.

This is a judgment call, not a rigid word-count or character check. Phrases and
sentences are never eligible.

### `#wp` (adjective)

Eligible only if the entry is a genuine single adjective in plain dictionary form —
い-adjective or な-adjective — per the type determination already used in
`references/adj-forms.md`.

`#wp` entries classified as **non-adjective/other** (the "all fields dash" case in
`adj-forms.md`) are **never eligible** — there is nothing to honorific-prefix.

Because `#wp` cards are, by the vault's tagging convention, already single words (not
phrases/sentences), there is no separate "no particles" check needed the way there is
for `#w` — the type-determination step itself is the eligibility gate.

### `#wc` (verb)

**Never eligible.** See the note at the top of this file.

---

## Already-prefixed exclusion

The mechanical check is the same for both types: does the furigana-stripped base
already begin with お or ご? If yes, the row is excluded. **The underlying reason
differs by card type — do not assume one explanation covers both.**

### `#w`

If the base word already begins with お or ご — e.g. お願い, お金, お弁当, お邪魔, all
real vault entries that would otherwise pass the "bare noun, no particle" test — it is
ineligible for a second prefix. Stacking a prefix (おお願い) is invalid Japanese. This
is a genuine **double-prefixing conflict**.

### `#wp`

The same "starts with お/ご → exclude" outcome applies, but for a **different
underlying reason**: many い-adjectives have お lexicalized into the word root itself —
おいしい, おかしい, おしゃれ, おもい — where お is not a separable, stackable honorific
prefix at all, it is simply part of the word. This is catching **lexically-fused お**,
not an already-honorific-prefixed word. A future implementer should not assume the
`#w` double-prefixing rationale carries over unchanged — for `#wp` there is no
"un-prefixed" base form to prefix in the first place.

---

## Prefix choice (お vs ご vs none)

Same wago/kango rule-of-thumb approach for both types:
- Native Japanese-origin (**wago**) words tend toward **お**.
- Sino-Japanese (**kango**) words tend toward **ご**.
- Well-known exceptions exist for both directions.
- Loanwords generally take **no prefix** at all.

### Noun exception list (`#w`)

お電話, お食事, お時間, お店, お願い(already-prefixed, excluded above), お金
(already-prefixed, excluded above), お弁当 (already-prefixed, excluded above)

(Note: some of the above are excluded by the already-prefixed rule and listed here only
to illustrate that they are wago words that would otherwise take お.)

### Adjective exception list (`#wp`)

お忙しい, お若い, ご立派, お元気, ご親切

### Loanword guidance (both types)

Loanwords (katakana-origin words) generally take no honorific prefix at all. Treat as
"no natural form" (omit) unless a prefixed form is well-established and commonly used.

### Uncertainty rule (both types)

If Claude is not confident a natural お/ご form exists, treat it as "no natural form" —
omit the row. Do not guess. Forcing a placeholder onto every eligible word risks
normalizing incorrect or invented お/ご forms.

---

## Value / furigana format

Label (same for both types, one canonical label — not two):
```
お/ご (honorific): [word with furigana]
```

Examples:
- `#w`: `お/ご (honorific): お電話(でんわ)`
- `#wp`: `お/ご (honorific): お忙(いそが)しい`

No extra annotation of which prefix was used — it is visible in the value itself.

### `(する)`-dropping rule — `#w`-only, confirmed N/A for `#wp`

For `#w` suru-noun entries, the honorific row value **drops** the trailing `(する)`:
```
担当(たんとう)(する)  →  ご担当(たんとう)
```
NOT `ご担当(たんとう)(する)`.

**Confirmed not applicable to `#wp`:** `adj-forms.md` and the canonical `#wp` template
in `card-templates.md` confirm that `#wp` values never carry a `(する)` suffix — that
formatting only exists for `#w` suru-noun entries. This is a verified fact, not a
silent omission: there is no `(する)`-dropping step needed for `#wp` because there is
never a `(する)` to drop in the first place.

---

## Placement

### `#w`

Immediately after the Japanese field line, before the kanji-trainer `<a href>` links,
before `<!--ID:-->`. Unchanged from the original design — there is nothing else between
the Japanese line and kanji links in the `#w` template.

### `#wp`

Inserted as the **new final form row** — immediately after そう (looks), which is
already the last of `#wp`'s 4 existing form lines (過去形, 否定形, 副詞形, そう
(looks)) — before kanji links, before `<!--ID:-->`.

This is structurally different from `#wc`'s `お〜になる` placement (which sits mid-list,
between そう (looks) and ない形, because `#wc` has 9 more form lines after そう) even
though both could loosely be described as "after そう" — for `#wp` it is simply an
append to the end of the form list, not a mid-list insert. Do not reuse `#wc`'s
positioning rule for `#wp`.

---

## No natural form exists

Omit the row entirely — no placeholder/N/A value (no `—`). Applies to both `#w` and
`#wp`, in both `fill-templates` (never add the row) and `templates-update` (never force
the row; remove it if incorrectly present from a prior run or manual edit).

---

## Relationship to `#wc`'s `お〜になる/special verb (honorific)` field

This row (`お/ご (honorific):`) and `#wc`'s `お〜になる/special verb (honorific):` field are
**two entirely different mechanisms**:
- `お/ご (honorific):` (`#w`/`#wp`, this file) — a lexical prefix applied to a noun or
  adjective (お + word, or ご + word).
- `お〜になる/special verb (honorific):` (`#wc` only, `references/verb-conjugation.md`) — a
  tiered mechanism (special-verb table, or verb-stem derivation お + ます stem + になる).

`#wc` is never eligible for the row documented in this file. Do not conflate the two
fields or their governing logic.
