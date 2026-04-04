# Skill: fill-templates

## Purpose
Replace plugin-generated empty Polish-field verb and adjective templates
with filled Japanese-field templates including all conjugation forms.

## Trigger phrases
User says: "fill [file/lesson]", "process [file/lesson]", "templates [file/lesson]"

## What the plugin generates (input)

### Verb card (empty):
```
to talk / to speak  #card
Tłumaczenie: 話す（はなす）
Forma masu: 
Forma te: 
Forma ta: 
Forma nai: 
Forma katta: 
```

### Adjective card (empty):
```
dark  #card
Tłumaczenie: 暗い（くらい）
Forma przeszła: 
Przeczenie: 
Przysłówek: 
```

## What to produce (output)

### Regular verb card (filled):
```
to talk / to speak  #card
ほんやく: 話す（はなす）
ます形: 話します
て形: 話して
た形: 話した
ない形: 話さない
なかった形: 話さなかった
ば形: 話せば
られる形: 話される
出す形: 話し出す
尊敬語: 話される
お〜になる: お話しになる
```

### Suru verb card (filled) — no forms:
```
attendance / to attend  #card
ほんやく: 出席（しゅっせき）
```

### Adjective card (filled):
```
dark  #card
ほんやく: 暗い（くらい）
過去形: 暗かった
否定形: 暗くない
副詞形: 暗く
```

## Conjugation rules

### Identifying verb type
- Ends in する or is a kanji/katakana noun with no hiragana verb ending → suru
  Examples: 出席, 予約, 質問する, 電話する
- Ends in える/ける/げる/せる/てる/でる/ねる/べる/める/れる → ichidan (ru-verb)
- Ends in いる/きる/ぎる/じる/ちる/にる/びる/みる/りる → ichidan (ru-verb)
- Everything else ending in う/く/ぐ/す/つ/ぬ/ぶ/む/る → godan (u-verb)
- Irregular: くる/来る

### Suru verbs
Output only two lines: front #card and ほんやく.
No conjugation forms needed — user knows them well.

### Ichidan verbs (ru-verbs)
Drop る, then:
- ます形: stem + ます
- て形: stem + て
- た形: stem + た
- ない形: stem + ない
- なかった形: stem + なかった
- ば形: stem + れば
- られる形: stem + られる
- 出す形: stem + 出す
- 尊敬語: stem + られる
- お〜になる: お + stem + になる

Example — 答える（こたえる）, stem = 答え:
ます形: 答えます / て形: 答えて / た形: 答えた / ない形: 答えない
なかった形: 答えなかった / ば形: 答えれば / られる形: 答えられる
出す形: 答え出す / 尊敬語: 答えられる / お〜になる: お答えになる

### Godan verbs (u-verbs)
Apply the correct row transformation based on the final kana:

| Ending | ます stem | て形  | た形  | ない形 | なかった形 | ば形 | られる形 | 出す形 |
|--------|----------|------|------|------|----------|-----|--------|------|
| う     | い       | って  | った  | わない | わなかった | えば | われる  | い出す |
| く     | き       | いて  | いた  | かない | かなかった | けば | かれる  | き出す |
| ぐ     | ぎ       | いで  | いだ  | がない | がなかった | げば | がれる  | ぎ出す |
| す     | し       | して  | した  | さない | さなかった | せば | される  | し出す |
| つ     | ち       | って  | った  | たない | たなかった | てば | たれる  | ち出す |
| ぬ     | に       | んで  | んだ  | なない | ななかった | ねば | なれる  | に出す |
| ぶ     | び       | んで  | んだ  | ばない | ばなかった | べば | ばれる  | び出す |
| む     | み       | んで  | んだ  | まない | まなかった | めば | まれる  | み出す |
| る     | り       | って  | った  | らない | らなかった | れば | られる  | り出す |

尊敬語: same as られる形
お〜になる: お + ます stem + になる

Example — 話す（はなす）, ends in す, stem = 話:
ます形: 話します / て形: 話して / た形: 話した / ない形: 話さない
なかった形: 話さなかった / ば形: 話せば / られる形: 話される
出す形: 話し出す / 尊敬語: 話される / お〜になる: お話しになる

### Irregular verbs
くる / 来る:
ます形: 来ます / て形: 来て / た形: 来た / ない形: 来ない
なかった形: 来なかった / ば形: 来れば / られる形: 来られる
出す形: 来出す / 尊敬語: 来られる / お〜になる: お出でになる

### i-adjectives
Drop い, then:
- 過去形: stem + かった
- 否定形: stem + くない
- 副詞形: stem + く

Special case — いい/よい:
過去形: よかった / 否定形: よくない / 副詞形: よく

Non-adjectives (次, はじめて, adverbs, な-adjectives mistagged as #wp):
Output — for all three fields.

## Furigana handling
- Brackets contain partial reading hints only, e.g. 上げる（あ）means 上 reads あ
- Never expand, modify, or remove furigana
- Copy ほんやく: value exactly as written in Tłumaczenie: line

## What never to touch
- The front text of the card — copy exactly as written before #card
- <!--ID: --> lines — preserve exactly, position after the last form line
- Rzeczowniki: section — completely untouched
- Everything above Rzeczowniki: — completely untouched

## Workflow
1. Open the file
2. Locate Czasowniki: section — process all verb cards
3. Locate Przymiotniki: section — process all adjective cards
4. Show full preview of both sections
5. Ask: "Looks good? Should I save?"
6. On confirmation: save file (keep backup as filename.md.bak)
