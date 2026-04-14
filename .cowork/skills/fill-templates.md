# Skill: fill-templates

## Purpose
Generate Anki flashcard templates for all #w, #wc, #wp lines in a lesson file
and append them under a `# Summary` + `Rzeczowniki:` section.

## Trigger phrases
"fill [file/lesson]", "process [file/lesson]", "templates [file/lesson]"

## Workflow
1. Find the lesson file (search by lesson number if needed)
2. Create a `.bak` backup of the file before writing — no confirmation needed
3. Read all `#w`, `#wc`, `#wp` lines from the lesson file
4. For each `#wc` verb: determine its type (godan / ichidan / suru / kuru) using
   your Japanese knowledge. If uncertain, use web search to confirm.
5. Generate cards following the formats below
6. Check each Japanese word against `KanjiList.md` — add `#k` tag if matched
7. Append the `# Summary` block to the end of the file
8. Done — no confirmation needed

## Verb type heuristic (apply when unsure)
- Ends in `える` or `いる` → **ichidan** (e.g. 食べる, 起きる)
- Ends in any other kana + `る` (ある, おる, うる...) → **godan** (e.g. 渡る, 走る)
- Ends in `く`,`ぐ`,`す`,`つ`,`ぬ`,`ぶ`,`む`,`う` → always **godan**
- `来る` → **kuru**
- `する` or compound `〜する` → **suru**
- Common godan exceptions ending in `える/いる`: 帰る, 走る, 切る, 知る, 入る, 要る

When uncertain, search: `[verb] godan ichidan` to confirm.

## File structure produced
Append this block to the end of the file:

```
# Summary

 ---


 Rzeczowniki:

[cards separated by blank lines]


 ---


```

## Card formats

### #w — word / expression / sentence
```
translation [#k] #card
japanese expression
```

### #wc — godan / ichidan verb
```
translation [#k] #card
ほんやく: japanese expression
ます形: ...
て形: ...
た形: ...
ない形: ...
なかった形: ...
ば形: ...
られる形: ...
出す形: ...
尊敬語: ...
お〜になる: ...
そう: ...
```

### #wc — suru verb (no conjugation)
```
translation [#k] #card
ほんやく: japanese expression
```

### #wc — kuru (来る)
```
translation [#k] #card
ほんやく: 来る
ます形: 来ます
て形: 来て
た形: 来た
ない形: 来ない
なかった形: 来なかった
ば形: 来れば
られる形: 来られる
出す形: 来出す
尊敬語: 来られる
お〜になる: お出でになる
そう: 来そう
```

### #wp — い-adjective
```
translation [#k] #card
ほんやく: japanese expression
過去形: stem + かった
否定形: stem + くない
副詞形: stem + く
そう: stem + そう
```
Special: いい / よい → よかった / よくない / よく / よさそう

### #wp — な-adjective
```
translation [#k] #card
ほんやく: japanese expression
過去形: —
否定形: —
副詞形: —
そう: base + そう
```

### #wp — non-adjective (次, はじめて, adverbs)
```
translation [#k] #card
ほんやく: japanese expression
過去形: —
否定形: —
副詞形: —
そう: —
```

## そう form rules
- **Godan verb**: ます stem + そう (渡る → 渡りそう, 降る → 降りそう)
- **Ichidan verb**: drop る + そう (食べる → 食べそう)
- **来る**: 来そう
- **い-adj**: drop い + そう (美味しい → 美味しそう)
- **Special**: いい / よい → よさそう
- **な-adj**: base + そう (静か → 静かそう)

## Conjugation rules

### Godan (u-verbs) — by ending kana
| Ending | ます stem | て形 | た形 | ない形 | なかった形 | ば形 | られる形 | 出す形 |
|--------|----------|------|------|--------|-----------|------|---------|--------|
| う | い | って | った | わない | わなかった | えば | われる | い出す |
| く | き | いて | いた | かない | かなかった | けば | かれる | き出す |
| ぐ | ぎ | いで | いだ | がない | がなかった | げば | がれる | ぎ出す |
| す | し | して | した | さない | さなかった | せば | される | し出す |
| つ | ち | って | った | たない | たなかった | てば | たれる | ち出す |
| ぬ | に | んで | んだ | なない | ななかった | ねば | なれる | に出す |
| ぶ | び | んで | んだ | ばない | ばなかった | べば | ばれる | び出す |
| む | み | んで | んだ | まない | まなかった | めば | まれる | み出す |
| る | り | って | った | らない | らなかった | れば | られる | り出す |
尊敬語 = られる形. お〜になる = お + ます stem + になる.

### Ichidan (ru-verbs) — drop る
stem + ます/て/た/ない/なかった/れば/られる/出す; 尊敬語=られる form; お〜になる = お + stem + になる.

## #k tag
Add `#k` before `#card` if the Japanese expression contains any kanji listed in `KanjiList.md`.

## Parsing rules

### Separator format
Japanese and translation are separated by ` - `:
- `日本語（よみ）- translation`
- `日本語 (よみ) - translation`
- `日本語 - translation`

### Special cases
- **Double-Japanese entry** (`#wc 伝える（つた）- 伝える（つたえる）- Polish`):
  Use the second Japanese form as both card front and ほんやく.
- **`ほんやく:` in translation**: strip the prefix, use only the Polish/English text.
- **Bold `**` markers**: strip from both Japanese and translation.
- **Empty translation**: skip the line.

## What never to touch
- TARGET DECK line at top of file
- <!--ID: --> lines (preserve exactly if present)
- Existing Rzeczowniki: section (if already present — do not re-run on filled files)
