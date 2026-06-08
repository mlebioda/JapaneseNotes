---
name: adj-forms
description: >
  Authoritative reference for Japanese adjective form derivations used by
  fill-templates and update-templates skills.
---

# Adjective Forms Reference

This file is the single source of truth for adjective conjugation rules.
Both `.cowork/skills/fill-templates.md` and `.cowork/skills/update-templates.md` defer here.

---

## い-adjective — fill actual forms

Stem = adjective minus final い.

```
過去形:  stem + かった
否定形:  stem + くない
副詞形:  stem + く
そう:    stem + そう
```

### Special case: いい / よい

```
過去形:  よかった
否定形:  よくない
副詞形:  よく
そう:    よさそう
```

Both `いい` and `よい` use the `よ-` stem for all derived forms.

---

## な-adjective — fill dashes (except そう)

な-adjectives do not inflect in the same way as い-adjectives.
All conjugation fields that do not apply receive a dash.

```
過去形:  —
否定形:  —
副詞形:  —
そう:    base + そう   (e.g. 静か → 静かそう)
```

The base for `そう` is the plain な-adjective stem (without な or だ).

---

## Non-adjective / adverb — all fields dash

When a `#wp` line turns out to be an adverb or other non-adjective word:

```
過去形:  —
否定形:  —
副詞形:  —
そう:    —
```

---

## Determining adjective type

1. If the Japanese word ends in `い` (and is not a な-adjective ending in `ない`, e.g. 嫌い) → **い-adjective**.
2. If marked with な or typically used with だ → **な-adjective**.
3. If it is an adverb, noun, or other non-inflecting word → **non-adjective** (all dashes).

When uncertain, default to **な-adjective** rules (safer: produces dashes rather than wrong forms).
