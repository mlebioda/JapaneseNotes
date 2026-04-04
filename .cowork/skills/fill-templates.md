# Skill: fill-templates

## Purpose
Generate Anki flashcard templates for all #w, #wc, #wp lines in a lesson file
and append them under a `# Summary` + `Rzeczowniki:` section.

## Trigger phrases
"fill [file/lesson]", "process [file/lesson]", "templates [file/lesson]"

## Fastest workflow (use this)
Run the saved script directly — no manual card writing needed:

```bash
python3 /path/to/ObsidianJP/.cowork/fill_cards.py <lesson_file.md>
```

Steps:
1. Find the lesson file (search by lesson number if needed)
2. Run fill_cards.py on it — script handles backup + output automatically
3. Done. No confirmation needed (backup is always created as .md.bak)

## File structure produced
The script appends this block to the end of the file:

```
# Summary

 ---


 Rzeczowniki:

translation [#k] #card
japanese expression


translation [#k] #card
ほんやく: japanese expression
ます形: ...
...
```

**No `Tłumaczenie:` keyword** — just the japanese expression directly.
**`# Summary`** heading must be present so it's visible in Obsidian.

## Card formats

### #w — word / expression / sentence
```
translation [#k] #card
japanese expression
```

### #wc — verb (non-suru)
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
```

### #wc — suru verb (no conjugation needed)
```
translation [#k] #card
ほんやく: japanese expression
```

### #wp — i-adjective
```
translation [#k] #card
ほんやく: japanese expression
過去形: stem + かった
否定形: stem + くない
副詞形: stem + く
```

### #wp — non-adjective (次, はじめて, adverbs mistagged as #wp)
```
translation [#k] #card
ほんやく: japanese expression
過去形: —
否定形: —
副詞形: —
```

## #k tag
Add `#k` before `#card` if the Japanese expression contains any kanji
listed in `ObsidianJP/KanjiList.md`.

## Special cases
- **Double-Japanese entry** (`#wc 伝える（つた）- 伝える（つたえる）- Polish`):
  Use the second Japanese form as both card front and ほんやく.
- **`ほんやく:` in translation**: strip the prefix, use only the Polish/English text.
- **Bold `**` markers**: strip from both Japanese and translation.
- **Empty translation**: skip the line.

## Separator format
Japanese and translation are separated by `- ` (with optional space before dash):
- Full-width paren: `日本語（よみ）- translation`
- ASCII paren: `日本語 (よみ) - translation`
- No paren: `日本語 - translation`

## Verb type table (maintained in fill_cards.py)
The script `fill_cards.py` has a `VTYPES` dict. Add new verbs there as
lessons introduce them. If a verb is missing, the card is still generated
but without conjugation forms.

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
stem + ます/て/た/ない/なかった/れば/られる/出す; 尊敬語=られる form.

### Irregular — 来る
来ます / 来て / 来た / 来ない / 来なかった / 来れば / 来られる / 来出す / お出でになる

## What never to touch
- TARGET DECK line at top of file
- <!--ID: --> lines (preserve exactly if present)
- Existing Rzeczowniki: section (if already present — do not re-run on filled files)
