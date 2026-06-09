---
name: verb-conjugation
description: >
  Authoritative reference for Japanese verb type detection and all 13 conjugation
  forms used by fill-templates and templates-update skills.
---

# Verb Conjugation Reference

This file is the single source of truth for verb conjugation rules.
Both `.cowork/skills/fill-templates.md` and `.cowork/skills/templates-update.md` defer here.

---

## Verb type heuristic

- Ends in `える` or `いる` → **ichidan** (e.g. 食べる, 起きる)
- Ends in any other kana + `る` → **godan** (e.g. 渡る, 走る)
- Ends in `く`,`ぐ`,`す`,`つ`,`ぬ`,`ぶ`,`む`,`う` → always **godan**
- `来る` → **kuru** (use fixed forms table below)
- `する` or compound `〜する` → **suru** (no conjugation rows — skeleton only)
- Common godan exceptions ending in `える/いる`: 帰る, 走る, 切る, 知る, 入る, 要る

If still uncertain after applying the heuristic, web-search `[verb] godan ichidan` before filling.

---

## Godan (u-verbs) — conjugation table by ending kana

The 13 form labels, in canonical order:
`て形`, `た形`, `ます形`, `出す形 (start)`, `そう (looks like)`, `お〜になる (honorific)`, `ない形`, `なかった形`, `受身形 (passive)`, `尊敬語 (honorific)`, `ば形 (if)`, `可能形 (can)`, `おう形 (let's)`

| Ending | ます stem | て形 | た形 | ない形 | なかった形 | ば形 | 可能形 | 受身形 | 出す形 | 意志形 |
|--------|----------|------|------|--------|-----------|------|--------|---------|--------|--------|
| う | い | って | った | わない | わなかった | えば | える | われる | い出す | おう |
| く | き | いて | いた | かない | かなかった | けば | ける | かれる | き出す | こう |
| ぐ | ぎ | いで | いだ | がない | がなかった | げば | げる | がれる | ぎ出す | ごう |
| す | し | して | した | さない | さなかった | せば | せる | される | し出す | そう |
| つ | ち | って | った | たない | たなかった | てば | てる | たれる | ち出す | とう |
| ぬ | に | んで | んだ | なない | ななかった | ねば | ねる | なれる | に出す | のう |
| ぶ | び | んで | んだ | ばない | ばなかった | べば | べる | ばれる | び出す | ぼう |
| む | み | んで | んだ | まない | まなかった | めば | める | まれる | み出す | もう |
| る | り | って | った | らない | らなかった | れば | れる | られる | り出す | ろう |

Notes for godan:
- `尊敬語 (honorific)` = same as `受身形 (passive)` value
- `お〜になる (honorific)` = お + ます stem + になる (e.g. お渡りになる)
- `そう (looks like)` = ます stem + そう (e.g. 渡りそう)
- `おう形 (let's)` = 意志形 column above

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
| 受身形 (passive) | stem + られる | 食べられる |
| 出す形 (start) | stem + 出す | 食べ出す |
| 尊敬語 (honorific) | = 受身形 | 食べられる |
| お〜になる (honorific) | お + stem + になる | お食べになる |
| そう (looks like) | stem + そう | 食べそう |
| おう形 (let's) | stem + よう | 食べよう |

---

## 可能形 — special cases

- **Godan**: change final kana from う-row to え-row + る  
  Examples: 書く → 書ける, 渡る → 渡れる, 買う → 買える
- **Ichidan**: drop る + られる (食べる → 食べられる)
- **来る** → 来られる
- **する** → できる

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
あれる形 (passive):  来られる
出す形 (start): 来出す
尊敬語 (honorific): 来られる
お〜になる (honorific): お出でになる
そう (looks like): 来そう
おう形 (let's): 来よう
```

---

## 尊敬語 and お〜になる derivation rules

- `尊敬語 (honorific)` is always the same value as `受身形 (passive)`.
- `お〜になる (honorific)` = お + ます stem + になる.  
  Example: 渡る → ます stem り → お渡りになる.  
  Exception: 来る → お出でになる (fixed).
