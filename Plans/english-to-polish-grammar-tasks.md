# english-to-polish-grammar — Tasks

- [x] Create `.cowork/skills/english-to-polish-grammar.md` with:
  - [x] Standard YAML frontmatter (`name`/`description`, per `manage-holidays.md` convention)
  - [x] Trigger definition: `english gap <topic>`
  - [x] Hard rule: zero Japanese content anywhere in the output
  - [x] Concrete detection procedure (gloss → candidate forms → narrow to confusable subset) plus the single ていた worked example
  - [x] Fallback rule: stop and tell the user if detection can't confidently reach ≥2 constructs — never write a single-construct file
  - [x] Primary-construct rule (most direct/literal correspondence to the topic's gloss; listed first in H1 title; source of the slug)
  - [x] Slug derivation rule (kebab-case of primary construct's key phrase)
  - [x] Duplicate check: exact slug match + near-match scan of existing H1 titles/`##` headings across `English-gaps/*.md`; show existing title + covered constructs; ask skip / append delta / separate file
  - [x] Delta logic: parse existing `##` headings, compute newly-detected cluster minus already-covered set; handle empty-delta (nothing to add) vs non-empty-delta cases
  - [x] Full output structure spec: TARGET DECK line, H1 title, Polish intro, per-construct `##` sections (Polish explanation + Structure: line + 2-3 row example table), Szybkie porównanie table, Częste błędy section, `# Summary`, flashcards
  - [x] Append-mode behavior: update H1 title to include delta constructs, add only delta `##` sections/rows/cards, never touch existing content
  - [x] Scope boundary note: writes only inside `English-gaps/`
- [x] Create `.claude/commands/english-to-polish-grammar.md` slash command stub
- [x] Ask user for permission, then update `.cowork/instructions.md`:
  - [x] Add `English-gaps/` to the Directory map section
  - [x] Add one line documenting the new skill under "Available skills"
