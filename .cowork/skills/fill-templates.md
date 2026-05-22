# Skill: fill-templates

## Purpose
Generate Anki flashcard templates for all #w, #wc, #wp lines in a lesson file
and append them under a `# Summary` + `Rzeczowniki:` section.

## Trigger phrases
"fill [file/lesson]", "process [file/lesson]", "templates [file/lesson]"

## Workflow
1. Find the lesson file (search by lesson number if needed)
2. Run `fill_extract.py` to extract vocab lines, apply #k tags, and write skeleton cards
3. Read the updated lesson file to see the generated skeletons
4. For each `#wc` verb skeleton: determine verb type (godan / ichidan / suru / kuru)
   and fill in all blank conjugation fields
5. For each `#wp` adjective skeleton: determine type (い / な / non-adj)
   and fill in blank form fields
6. Write the completed cards back with Edit — replacing the skeleton block
7. Done — no confirmation needed

## Step 2 — running the script

Translate the lesson file path and KanjiList path to bash mount paths, then run:

```bash
python3 /sessions/stoic-serene-brahmagupta/mnt/ObsidianJP/.cowork/skills/fill_extract.py \
  "<lesson_bash_path>" \
  "/sessions/stoic-serene-brahmagupta/mnt/ObsidianJP/KanjiList.md"
```

The script handles automatically:
- Extracting all `#w`, `#wc`, `#wp` lines
- Deduplication (same Japanese field = skip)
- `#k` tagging (grep against KanjiList.md)
- Writing skeleton template structure with blank fields
- Suru verb detection (no conjugation rows if `する` in Japanese)
- Removing empty existing `# Summary` and re-appending

## Step 4 — filling verb skeletons

For each `#wc` skeleton, fill all blank fields. Use the verb type heuristic below.
If uncertain, web-search `[verb] godan ichidan`.

### Verb type heuristic
- Ends in `える` or `いる` → **ichidan** (e.g. 食べる, 起きる)
- Ends in any other kana + `る` → **godan** (e.g. 渡る, 走る)
- Ends in `く`,`ぐ`,`す`,`つ`,`ぬ`,`ぶ`,`む`,`う` → always **godan**
- `来る` → **kuru** (use fixed forms below)
- `する` or compound `〜する` → **suru** (script already produces no-conjugation skeleton)
- Common godan exceptions ending in `える/いる`: 帰る, 走る, 切る, 知る, 入る, 要る

### Godan (u-verbs) — by ending kana
| Ending | ます stem | て形 | た形 | ない形 | なかった形 | ば形 | 可能形 | られる形 | 出す形 | 意志形 |
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
尊敬語 = られる形. お〜になる = お + ます stem + になる.

### Ichidan (ru-verbs) — drop る
stem + ます/て/た/ない/なかった/れば/られる/出す; 可能形 = stem + られる; 意志形 = stem + よう (食べる → 食べよう); 尊敬語 = られる form; お〜になる = お + stem + になる.

### 可能形 — special cases
- **Godan**: change final kana from う-row to え-row + る (書く → 書ける, 渡る → 渡れる, 買う → 買える)
- **Ichidan**: drop る + られる (食べる → 食べられる)
- **来る** → 来られる
- **する** → できる

### そう form rules
- **Godan**: ます stem + そう (渡る → 渡りそう)
- **Ichidan**: drop る + そう (食べる → 食べそう)
- **来る**: 来そう
- **い-adj**: drop い + そう (美味しい → 美味しそう); いい/よい → よさそう
- **な-adj**: base + そう (静か → 静かそう)

### 来る — fixed forms
```
ます形: 来ます
て形: 来て
た形: 来た
ない形: 来ない
なかった形: 来なかった
ば形 (if): 来れば
可能形 (can): 来られる
られる形 (is done by): 来られる
出す形 (start): 来出す
尊敬語 (honorific): 来られる
お〜になる (honorific): お出でになる
そう (looks like): 来そう
おう (let's): 来よう
```

## Step 5 — filling adjective skeletons

For each `#wp` skeleton, determine adj type then fill fields:

### い-adjective — fill actual forms
```
過去形: stem + かった
否定形: stem + くない
副詞形: stem + く
そう: stem + そう
```
Special: いい / よい → よかった / よくない / よく / よさそう

### な-adjective or non-adjective — fill dashes
```
過去形: —
否定形: —
副詞形: —
そう: base + そう   ← (な-adj) or —  ← (non-adj / adverb)
```

## Card format reference (for manual fixes if needed)

### #w — word / expression / sentence
```
translation [#k] #card
japanese expression (furigana)
```
Copy the Japanese portion as-is (everything before ` - `), including furigana `(よみ)`.

### #wc — godan / ichidan verb (fully filled)
```
translation [#k] #card
ほんやく: japanese expression (furigana)
ます形: ...
て形: ...
た形: ...
ない形: ...
なかった形: ...
ば形 (if): ...
可能形 (can): ...
られる形 (is done by): ...
出す形 (start): ...
尊敬語 (honorific): ...
お〜になる (honorific): ...
そう (looks like): ...
おう (let's): ...
```

### #wc — suru verb (script generates this automatically)
```
translation [#k] #card
ほんやく: japanese expression (furigana)
```

## Parsing rules (reference — handled by script, Claude applies for manual fixes)

- Furigana `（よみ）` / `(よみ)`: keep inline, do NOT strip
- Double-Japanese entry (`#wc 伝える（つた）- 伝える（つたえる）- Polish`): use second Japanese form
- Bold `**` markers: strip from both fields
- Empty translation: skip the line

## Post-execution prompt

After filling all skeletons, ask the user:

> Summary written. Run **summarize-grammar** on this lesson now? (adds grammar points to the index)

- If **yes** → immediately load and execute the `summarize-grammar` skill for the same lesson, no further confirmation needed.
- If **no** → done.

## What never to touch
- TARGET DECK line at top of file
- <!--ID: --> lines (preserve exactly if present)
- Existing <!--ID: --> (if already found in file — script aborts automatically)
