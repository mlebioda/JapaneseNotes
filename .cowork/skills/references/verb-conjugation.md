---
name: verb-conjugation
description: >
  Authoritative reference for Japanese verb type detection and all 15 conjugation
  forms used by fill-templates and templates-update skills.
---

# Verb Conjugation Reference

This file is the single source of truth for verb conjugation rules.
Both `.cowork/skills/fill-templates.md` and `.cowork/skills/templates-update.md` defer here.

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
`て形`, `た形`, `ます形`, `出す形 (start)`, `そう (looks like)`, `お〜になる (honorific)`, `ない形`, `なかった形`, `受身形 (passive)`, `使役形 (make/let)`, `尊敬語 (honorific)`, `ば形 (if)`, `可能形 (can)`, `おう形 (let's)`, `命令形 (imperative)`

| Ending | ます stem | て形 | た形 | ない形 | なかった形 | ば形 | 可能形 | 受身形 | 使役形 | 出す形 | 意志形 | 命令形 |
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
- `尊敬語 (honorific)` = same as `受身形 (passive)` value
- `お〜になる (honorific)` = お + ます stem + になる (e.g. お渡りになる)
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
| 受身形 (passive) | stem + られる | 食べられる |
| 使役形 (make/let) | stem + させる | 食べさせる |
| 出す形 (start) | stem + 出す | 食べ出す |
| 尊敬語 (honorific) | = 受身形 | 食べられる |
| お〜になる (honorific) | お + stem + になる | お食べになる |
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
あれる形 (passive):  来られる
使役形 (make/let): 来させる（こさせる）
出す形 (start): 来出す
尊敬語 (honorific): 来られる
お〜になる (honorific): お出でになる
そう (looks): 来そう
おう形 (let's): 来よう
命令形 (imperative): 来い（こい）
```

---

## 尊敬語 and お〜になる derivation rules

- `尊敬語 (honorific)` is always the same value as `受身形 (passive)` — plain form, **never add ます** (e.g. 履かれる, not 履かれます).
- `お〜になる (honorific)` = お + ます stem + になる.  
  Example: 渡る → ます stem り → お渡りになる.  
  Exception: 来る → お出でになる (fixed).
