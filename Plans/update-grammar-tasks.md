# update-grammar Skill — Implementation Tasks

Reference plan: [[update-grammar-plan]]

---

## Task 1 — Write the skill file

Create `.cowork/skills/lesson-to-web/update-grammar.md`.

Content must cover (in order):
- Frontmatter: name, description, trigger phrases
- Trigger section
- Workflow steps 1–9 as defined in the plan
- Completion report format
- "Never touch" section (frontmatter fields other than `proofread`, Japanese text, ID lines, files outside `grammar-index/grammar/`)

Key details to capture:
- Tag removal precedes furigana conversion on the same line
- Furigana algorithm: kanji-word detection (CJK U+4E00–U+9FFF), in-order matching, warning on mismatch
- Structure inference rules (single unified pattern → Structure 1; distinct use cases → Structure 2)
- Structure templates (word-type sections, tense rows, example required per row)
- See also algorithm: search grammar-index/*.md non-recursively, collect co-entries, format as absolute URLs
- User interaction points: substantive issues (step 5), missing info (step 6), structure confirmation (step 7)

---

## Task 2 — Update extract-grammar reference

In `.cowork/skills/lesson-to-web/extract-grammar.md`, step 10 references:
```
.cowork/skills/update-grammar.md
```
Update to:
```
.cowork/skills/lesson-to-web/update-grammar.md
```

There are two occurrences in step 10 — update both.

---

## Task 3 — Update instructions.md

In `.cowork/instructions.md`, add `update-grammar` under the `**lesson-to-web/**` group in `## Available skills`:

```
- lesson-to-web/update-grammar — post-process grammar files: furigana, language, structure, See also. Sets proofread: true. Trigger: "update grammar <file>"
```

---

## Task 4 — Self-review

After implementing tasks 1–3, verify:
- [ ] Skill file exists at `.cowork/skills/lesson-to-web/update-grammar.md`
- [ ] All 7 rules from the plan are covered in the skill file
- [ ] Both structure templates are written out in full
- [ ] See also algorithm is unambiguous (non-recursive search, co-entry collection, dedup, absolute URL format)
- [ ] User interaction points are clearly marked (which steps require user approval)
- [ ] extract-grammar.md step 10 reference updated (both occurrences)
- [ ] instructions.md Available skills section updated
- [ ] "Never touch" rules are complete
