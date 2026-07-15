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
   and fill in blank form fields, then evaluate honorific eligibility and append the
   `お/ご (honorific):` row as the new last form line if a natural form exists (see Step 5 below)
6. After all fields of a template are filled, append kanji trainer links (see ## Kanji trainer links below)
7. Write the completed cards back with Edit — replacing the skeleton block
8a. For all `#w` cards in the Summary section: evaluate honorific eligibility and insert the
   `お/ご (honorific):` row after the Japanese field line if a natural form exists (see Step 8a below)
8b. For all `#w` cards: append kanji trainer links after the Japanese field line, or after the
   honorific row if one was inserted in Step 8a — whichever is last (same rule — one `<a>` line
   per unique CJK kanji in that card's text)
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
可能形 special cases, そう form rules, 来る fixed forms, お〜になる/special-verb derivation rules.

**お〜になる/special verb (honorific) first-time-fill fallback:** apply the tiered logic in
`verb-conjugation.md`'s derivation-rules section. If tier 3b requires a web search and the
search result is genuinely inconclusive, there is no confirmation gate in this fill workflow
to fall back on (unlike `templates-update.md`'s Repair 3e). In that case, do NOT silently
write `-` and do NOT silently write an unflagged tier-2 guess. Instead, default to a
best-effort tier-2 お+ます形+になる value and append an inline flag so the user can double
check it, e.g. `お〜になる/special verb (honorific): お見せになる (unconfirmed — verify)`.

## Step 5 — filling adjective skeletons

For each `#wp` skeleton, determine adj type then fill fields.

See `.cowork/skills/references/adj-forms.md` for い/な/non-adj rules,
including the special case for いい/よい and how to determine adjective type.

After the 4 standard adjective forms (過去形, 否定形, 副詞形, そう (looks)) are filled,
evaluate honorific eligibility per `.cowork/skills/references/honorific-forms.md`. If the
entry is a genuine single adjective (not a non-adjective/all-dash entry) and a natural
お/ご honorific form exists, append `お/ご (honorific): [word with furigana]` as the new
5th/last form line, immediately after そう (looks). If not eligible, or Claude is not
confident a natural form exists, omit the row entirely — no placeholder value. This
sub-instruction runs before Step 6 appends kanji links, so the honorific row (when
present) is already the last adjective row by the time Step 6 executes.

## Step 8a — evaluating #w honorific eligibility

For each `#w` card, evaluate honorific eligibility per
`.cowork/skills/references/honorific-forms.md`. If the Japanese field (furigana stripped)
is a bare noun (no particles, not a conjugated ending; suru-nouns count) and is not
already prefixed with お/ご, and a natural お/ご honorific form exists, insert
`お/ご (honorific): [word with furigana]` as a new line immediately after the Japanese
field line (before any kanji trainer links). Suru-noun entries drop the trailing `(する)`
in the honorific value (e.g. `担当(たんとう)(する)` → `ご担当(たんとう)`). If not
eligible, or Claude is not confident a natural form exists, omit the row entirely — no
placeholder value.

## Step 8b — #w kanji trainer links

Append kanji trainer links after the Japanese field line, or after the honorific row
inserted in Step 8a if one exists — whichever line is last in the block at this point.

## Kanji trainer links

Applies to **all card types**: `#w`, `#wc`, and `#wp`.

- For `#wc` and `#wp`: append links after the last conjugation/adjective row (Step 6).
  This wording stays correct for `#wp` only because the honorific sub-instruction added
  to Step 5 runs *before* Step 6 — so when a `#wp` honorific row is present, it is
  already the "last adjective row" by the time Step 6 executes. This ordering dependency
  is intentional and must not be reversed.
- For `#w`: append links after the Japanese field line, or after the honorific row if one
  was inserted (Step 8b; see Step 8a for the honorific row itself).

See `.cowork/skills/references/kanji-links.md` for the full kanji link procedure:
CJK range definition, source text rules (including furigana stripping for #wc/#wp),
link format, deduplication scope, and placement rules.

---

## Card format reference (for manual fixes if needed)

### #w — word / expression / sentence
```
translation [#k] #card
japanese expression (furigana)
お/ご (honorific): honorific word (furigana)  ← optional, only when a natural form exists
<a href="https://kanji-trainer.org/Mnemonic_phrase/Mnemonic_X.html">X</a>
```
Copy the Japanese portion as-is (everything before ` - `), including furigana `(よみ)`.
The `お/ご (honorific):` line is inserted per Step 8a — omitted entirely (no placeholder)
when the word is not eligible or no natural form exists. See
`.cowork/skills/references/honorific-forms.md`.

### #wc — godan / ichidan verb (fully filled)
```
translation [#k] #card
ほんやく: japanese expression (furigana)
て形: ...
た形: ...
ます形: ...
出す形 (start): ...
そう (looks): ...
お〜になる/special verb (honorific): ...
ない形: ...
なかった形: ...
あれる形 (passive/honorific):  ...
使役形 (make/let): ...
ば形 (if): ...
可能形 (can): ...
おう形 (let's): ...
命令形 (imperative): ...
<a href="https://kanji-trainer.org/Mnemonic_phrase/Mnemonic_X.html">X</a>
```
(one `<a …>` line per unique CJK kanji in the `ほんやく:` value, furigana stripped, ordered by first occurrence)

### #wc — suru verb (script generates this automatically)
```
translation [#k] #card
ほんやく: japanese expression (furigana)
```

### #wp — adjective (fully filled)
```
translation [#k] #card
ほんやく: japanese expression (furigana)
過去形: ...
否定形: ...
副詞形: ...
そう (looks): ...
お/ご (honorific): honorific word (furigana)  ← optional, only when a natural form exists
<a href="https://kanji-trainer.org/Mnemonic_phrase/Mnemonic_X.html">X</a>
```
The `お/ご (honorific):` line is appended per Step 5's honorific sub-instruction — omitted
entirely (no placeholder) when the entry is not a genuine single adjective or no natural
form exists. See `.cowork/skills/references/honorific-forms.md`.

## Parsing rules (reference — handled by script, Claude applies for manual fixes)

- Furigana `（よみ）` / `(よみ)`: keep inline, do NOT strip
- Double-Japanese entry (`#wc 伝える（つた）- 伝える（つたえる）- Polish`): use second Japanese form
- Bold `**` markers: strip from both fields
- Empty translation: skip the line

## What never to touch
- TARGET DECK line at top of file
- <!--ID: --> lines (preserve exactly if present)
- Existing <!--ID: --> (if already found in file — script aborts automatically)
