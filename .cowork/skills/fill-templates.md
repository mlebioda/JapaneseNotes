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
6. After all fields of a template are filled, append kanji trainer links (see ## Kanji trainer links below)
7. Write the completed cards back with Edit — replacing the skeleton block
8. For all `#w` cards in the Summary section: append kanji trainer links after the Japanese field line (same rule — one `<a>` line per unique CJK kanji in that card's text)
9. Done — no confirmation needed

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

For each `#wc` skeleton, fill all blank fields. Use the verb type heuristic in the reference file.
If uncertain, web-search `[verb] godan ichidan`.

See `.cowork/skills/references/verb-conjugation.md` for all conjugation tables and rules:
verb type heuristic, godan table (all endings × all 14 forms), ichidan rules,
可能形 special cases, そう form rules, 来る fixed forms, 尊敬語 and お〜になる derivation rules.

## Step 5 — filling adjective skeletons

For each `#wp` skeleton, determine adj type then fill fields.

See `.cowork/skills/references/adj-forms.md` for い/な/non-adj rules,
including the special case for いい/よい and how to determine adjective type.

## Kanji trainer links

Applies to **all card types**: `#w`, `#wc`, and `#wp`.

- For `#wc` and `#wp`: append links after the last conjugation/adjective row (Step 6).
- For `#w`: append links after the Japanese field line (Step 8).

See `.cowork/skills/references/kanji-links.md` for the full kanji link procedure:
CJK range definition, source text rules (including furigana stripping for #wc/#wp),
link format, deduplication scope, and placement rules.

---

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
て形: ...
た形: ...
ます形: ...
出す形 (start): ...
そう (looks like): ...
お〜になる (honorific): ...
ない形: ...
なかった形: ...
あれる形 (passive):  ...
使役形 (make/let): ...
尊敬語 (honorific): ...
ば形 (if): ...
可能形 (can): ...
おう形 (let's): ...
<a href="https://kanji-trainer.org/Mnemonic_phrase/Mnemonic_X.html">X</a>
```
(one `<a …>` line per unique CJK kanji in the `ほんやく:` value, furigana stripped, ordered by first occurrence)

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

## What never to touch
- TARGET DECK line at top of file
- <!--ID: --> lines (preserve exactly if present)
- Existing <!--ID: --> (if already found in file — script aborts automatically)
