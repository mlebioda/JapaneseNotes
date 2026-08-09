---
name: verb-conjugation
description: >
  Authoritative reference for Japanese verb type detection and all 15 conjugation
  forms used by fill-templates, templates-update, and add-word-to-deck skills.
---

# Verb Conjugation Reference

This file is the single source of truth for verb conjugation rules.
`.cowork/skills/fill-templates.md`, `.cowork/skills/templates-update.md`, and
`.cowork/skills/add-word-to-deck.md` all defer here.

---

## Verb type heuristic

- Ends in `える` or `いる` → **ichidan** (e.g. 食べる, 起きる, あげる, 調べる)  
  E-row kana (char before る): え け げ せ ぜ て で ね へ べ ぺ め れ  
  I-row kana (char before る): い き ぎ し じ ち ぢ に ひ び ぴ み り
- Ends in any other kana + `る` → **godan** (e.g. 渡る, 走る)
- Ends in `く`,`ぐ`,`す`,`つ`,`ぬ`,`ぶ`,`む`,`う` → always **godan**
- `来る` → **kuru** (use fixed forms table below)
- `する` or compound `〜する` → **suru** (no conjugation rows — skeleton only)
- Common godan exceptions ending in `える/いる`: 帰る, 走る, 切る, 知る, 入る, 要る

If still uncertain after applying the heuristic, web-search `[verb] godan ichidan` before filling.

---

## Godan (u-verbs) — conjugation table by ending kana

The 15 form labels, in canonical order:
`て形`, `た形`, `ます形`, `出す形 (start)`, `そう (looks like)`, `お〜になる/special verb (honorific)`, `謙譲語 (humble)`, `ない形`, `なかった形`, `あれる形 (passive/honorific)`, `使役形 (make/let)`, `ば形 (if)`, `可能形 (can)`, `おう形 (let's)`, `命令形 (imperative)`

| Ending | ます stem | て形 | た形 | ない形 | なかった形 | ば形 | 可能形 | あれる形 | 使役形 | 出す形 | 意志形 | 命令形 |
|--------|----------|------|------|--------|-----------|------|--------|---------|--------|--------|--------|--------|
| う | い | って | った | わない | わなかった | えば | える | われる | わせる | い出す | おう | え |
| く | き | いて | いた | かない | かなかった | けば | ける | かれる | かせる | き出す | こう | け |
| ぐ | ぎ | いで | いだ | がない | がなかった | げば | げる | がれる | がせる | ぎ出す | ごう | げ |
| す | し | して | した | さない | さなかった | せば | せる | される | させる | し出す | そう | せ |
| つ | ち | って | った | たない | たなかった | てば | てる | たれる | たせる | ち出す | とう | て |
| ぬ | に | んで | んだ | なない | ななかった | ねば | ねる | なれる | なせる | に出す | のう | ね |
| ぶ | び | んで | んだ | ばない | ばなかった | べば | べる | ばれる | ばせる | び出す | ぼう | べ |
| む | み | んで | んだ | まない | まなかった | めば | める | まれる | ませる | み出す | もう | め |
| る | り | って | った | らない | らなかった | れば | れる | られる | らせる | り出す | ろう | れ |

Notes for godan:
- `お〜になる/special verb (honorific)` — see ## お〜になる/special-verb derivation rules below.
- `謙譲語 (humble)` — see ## 謙譲語 (humble) derivation rules below.
- `そう (looks like)` = ます stem + そう (e.g. 渡りそう)
- `おう形 (let's)` = 意志形 column above
- `使役形 (make/let)` = ない形 stem (あ/わ row) + せる
- `命令形 (imperative)` = e-row kana alone (same row as 可能形/ば形, no る/ば suffix)

---

## Ichidan (ru-verbs) — drop る

Stem = verb minus final る.

| Form | Rule | Example (食べる → stem 食べ) |
|------|------|------|
| ます形 | stem + ます | 食べます |
| て形 | stem + て | 食べて |
| た形 | stem + た | 食べた |
| ない形 | stem + ない | 食べない |
| なかった形 | stem + なかった | 食べなかった |
| ば形 (if) | stem + れば | 食べれば |
| 可能形 (can) | stem + られる | 食べられる |
| あれる形 (passive/honorific) | stem + られる | 食べられる |
| 使役形 (make/let) | stem + させる | 食べさせる |
| 出す形 (start) | stem + 出す | 食べ出す |
| お〜になる/special verb (honorific) | お + stem + になる (tier 2 only) | お見せになる (見せる) |
| 謙譲語 (humble) | お/ご + stem + いたす／します (tier 2 only) | お教えいたす／お教えします (教える) |
| そう (looks like) | stem + そう | 食べそう |
| おう形 (let's) | stem + よう | 食べよう |
| 命令形 (imperative) | stem + ろ | 食べろ |

---

## 可能形 — special cases

- **Godan**: change final kana from う-row to え-row + る  
  Examples: 書く → 書ける, 渡る → 渡れる, 買う → 買える
- **Ichidan**: drop る + られる (食べる → 食べられる)
- **来る** → 来られる
- **する** → できる

---

## 使役形 — special cases

- **Godan**: ない形 stem (あ-row) + せる, with the う-ending exception using わ instead of あ  
  Examples: 書く → 書かせる, 飲む → 飲ませる, 話す → 話させる, 買う → 買わせる
- **Ichidan**: drop る + させる  
  Examples: 食べる → 食べさせる, 見る → 見させる
- **する** → させる
- **来る** → 来させる（こさせる）

---

## 命令形 — special cases

- **Godan**: change final kana from う-row to え-row, no suffix added
  Examples: 書く → 書け, 飲む → 飲め, 話す → 話せ, 買う → 買え
- **Ichidan**: drop る + ろ (canonical colloquial form; よ not used)
  Examples: 食べる → 食べろ, 見る → 見ろ
- **する** → しろ
- **来る** → 来い（こい）

---

## そう form rules

- **Godan**: ます stem + そう (渡る → 渡りそう)
- **Ichidan**: drop る + そう (食べる → 食べそう)
- **来る**: 来そう
- **い-adj**: drop い + そう (美味しい → 美味しそう); いい/よい → よさそう
- **な-adj**: base + そう (静か → 静かそう)

---

## 来る — fixed forms

```
ます形: 来ます
て形: 来て
た形: 来た
ない形: 来ない
なかった形: 来なかった
ば形 (if): 来れば
可能形 (can): 来られる
あれる形 (passive/honorific):  来られる
使役形 (make/let): 来させる（こさせる）
出す形 (start): 来出す
お〜になる/special verb (honorific): いらっしゃる
謙譲語 (humble): 参る
そう (looks): 来そう
おう形 (let's): 来よう
命令形 (imperative): 来い（こい）
```

---

## お〜になる/special-verb derivation rules

This field resolves via a three-tier priority order. It never resolves to the
られる/passive-honorific form itself — that is the separate `あれる形 (passive/honorific)`
field, unaffected by this rule.

### Tier 1 — special verb table

If the verb's meaning matches an entry below, always use the special verb — this tier wins
regardless of tier 2 eligibility.

| Verb meaning | Special verb (honorific) |
|---|---|
| 行く／来る／いる | いらっしゃる (default; おいでになる／お越しになる are valid, more formal alternates — いらっしゃる is the default pick) |
| 食べる／飲む | 召し上がる |
| 寝る／休む | お休みになる |
| 死ぬ | お亡くなりになる |
| 言う | おっしゃる |
| 見る | ご覧になる |
| 着る | お召しになる |
| する | なさる |
| 知っている（ている形） | ご存じ(です) |
| くれる | くださる |

する and 来る always use their tier-1 special verb (なさる／いらっしゃる) — they never take tier 2.

### Tier 2 — お + ます形(stem) + になる

Used only when (a) no special verb applies, (b) the verb is not する/来る, and (c) the ます-stem
is 2+ morae.  
Example: 見せる → ます stem 見せ → お見せになる.

### Tier 3a — deterministic exclusion (1-mora stem, no search)

If no special verb applies and the ます-stem is exactly 1 mora (e.g. 見る, 着る — both already
covered by the tier-1 table in practice, so this rarely surfaces as its own case),
お+ます形+になる is grammatically impossible. This is a computable fact (mora count), not a
judgment call — resolve directly to `-` without any web search.

### Tier 3b — search-confirmed exclusion (ambiguous idiomatic usage)

If the ます-stem is 2+ morae, no special verb applies, but it's genuinely unclear whether
お+ます形+になる is idiomatically natural for that specific verb, web-search e.g.
`[verb] 尊敬語 おになる` before deciding — mirroring the existing web-search escalation pattern
already used for the verb-type heuristic above and in `templates-update.md`. Only write `-`
once the search confirms the verb customarily relies solely on the plain られる/
passive-honorific form (`あれる形 (passive/honorific)`) with no idiomatic お+ます形+になる or
special-verb form in active use.

Tier 3a and 3b both produce `-` but are distinguishable and must not be conflated: 3a is a
deterministic mora-count check requiring no search; 3b requires search-confirmed ambiguous
usage.

---

## 謙譲語 (humble) derivation rules

This field resolves via a four-tier priority order. It never resolves to the
`あれる形 (passive/honorific)` field or to the `お〜になる/special verb (honorific)` field —
both are separate, unrelated fields on the same card and are unaffected by this rule.

### Tier 1 — special verb table

If the verb's meaning matches an entry below, always use the special verb — this tier wins
regardless of tier 2 eligibility. Tier-1 entries are single-valued — there is no いたす／します
dual form here, since there is nothing left to derive; the special verb itself is already
fully humble.

| Verb meaning | Special verb (humble) |
|---|---|
| 行く／来る | 参る |
| する | いたす |
| 言う | 申す (default; 申し上げる is a valid, more-formal alternate) |
| 見る | 拝見する |
| 聞く／尋ねる／訪問する | 伺う |
| 食べる／飲む | いただく |
| もらう | いただく |
| あげる | さしあげる |
| いる | おる |
| 知っている | 存じておる (存じ上げる — for people) |
| 会う | お目にかかる |
| 見せる | お目にかける |
| 借りる | 拝借する |

する and 来る always use their tier-1 special verb (いたす／参る) — they never take tier 2.

### Tier 2 — お/ご + ます形(stem) + いたす／します

Used only when (a) no special verb applies and (b) the ます-stem is 2+ morae. Prefix choice (お
for wago-origin verbs, ご for kango/verbal-noun verbs) reuses the wago/kango prefix-choice
heuristic in `.cowork/skills/references/honorific-forms.md`'s "## Prefix choice (お vs ご vs
none)" section (cross-reference only — see that file's scope-note for the exact carve-out).

**This tier's value is dual-valued and slash-separated** — both the いたす form and the
する／します form, in that order: `[お-stem]いたす／[お-stem]します` for wago verbs, or
`ご[noun]いたす／ご[noun]します` for kango/suru-compound verbs. This is a deliberate,
explicit deviation from every other single-valued form field on this card — tier 2 is the only
tier where the auxiliary itself (いたす vs する／します) is the thing varying.

Note: suru-compound (`〜する`) verbs never reach this tier in practice, since suru verbs have
zero conjugation rows entirely (an existing, unrelated rule — `#wc` suru verbs skip all form
fields). This makes the ご-branch of this rule real in principle but rarely-if-ever exercised
on an actual filled card. Document it for correctness — it is a near-dead branch in practice,
not a branch to remove.

Example: 手伝う → ます stem 手伝い (4 morae) → お手伝いいたす／お手伝いします.

### Tier 3a — deterministic exclusion (1-mora stem, no search)

If no special verb applies and the ます-stem is exactly 1 mora (e.g. 寝る, 着る, 出る — real
`#wc` entries in the vault, none tier-1-covered for 謙譲語), お/ご+ます形+いたす is
grammatically impossible. This is a computable fact (mora count), not a judgment call —
resolve directly to `-` without any web search.

### Tier 3b — search-confirmed exclusion (ambiguous idiomatic usage)

If the ます-stem is 2+ morae, no special verb applies, but it's genuinely unclear whether
お/ご+stem+いたす is idiomatically natural for that specific verb, web-search e.g.
`[verb] 謙譲語 いたす` before deciding — mirroring the same escalation pattern already used for
お〜になる's tier 3b and the verb-type heuristic above. Only write `-` once the search confirms
the verb has no idiomatic humble form in active use.

Tier 3a and 3b both produce `-` but are distinguishable and must not be conflated: 3a is a
deterministic mora-count check requiring no search; 3b requires search-confirmed ambiguous
usage.

する and 来る always use their tier-1 special verb (いたす／参る) — they never take tier 2, 3a,
or 3b.

This field never resolves to `あれる形 (passive/honorific)` or to
`お〜になる/special verb (honorific)` — both are separate fields, unaffected by this rule.
