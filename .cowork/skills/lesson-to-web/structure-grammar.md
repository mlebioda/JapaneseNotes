---
name: structure-grammar
description: >
  Enforce file structure on grammar files under grammar-index/grammar/. Detects
  container files (skips them), normalises sections, infers Structure 1 vs Structure 2,
  and reformats with user confirmation. Trigger: "structure grammar <file>" or called
  from review-grammar.
---

# Structure Grammar Skill

## Trigger

- "structure grammar `<slug>`" — filename without `.md`
- "structure grammar grammar-index/grammar/`<slug>`.md" — full relative path
- (called automatically from review-grammar with a list of file paths)

---

## Workflow

Process each file in order. Apply all steps to one file before moving to the next.

If called with **all** mode (from review-grammar "all" answer): skip the handoff prompt at the end and automatically continue to register-confusability-grammar.

---

## Shared files

Load `.cowork/skills/lesson-to-web/_conventions.md` before starting.

---

Check the proofread: true guard (see _conventions.md) before processing each file.

---

### Step 7 — File structure enforcement

#### Container file detection

Files matching `grammar-index/vocabulary-*.md` are vocabulary consolidation files, not
containers — never processed by this skill at all (not even the container-skip log line); this
guard is checked before the `## Sub-topics` check.

Before applying any normalisation, check whether the file is a container file:
- A `## Sub-topics` section is present.

If the file is a container file:
- Skip all normalisation and structure inference.
- Log: `Structure: container file — Step 7 skipped`.
- Continue to handoff.

#### Section normalisation (silent, before proposing structure)

- `## Examples` absent → add an empty `## Examples` section between `## Structure` and `## Notes`.
- `## Notes` present but empty → remove the section entirely.
- **Re-run preservation:** when reformatting a file into Structure 1 or Structure 2, preserve any existing `## Register` and `## Often confused with` sections unchanged, in their `_conventions.md` section-order position (after `## Notes`, before `## See also`) — the templates below end at `## See also` and predate these sections; dropping them would wipe register-confusability-grammar's work and dangle reverse links held by other files.

#### Summary line

The gloss line (`> ...`) immediately under the main heading is the summary. It stays as a blockquote — not a separate `## Summary` header.

#### Inferring which structure to use

**Structure 1** — use when the grammar point has a single unified pattern that applies across word types in the same way.

**Structure 2** — use when the grammar point has two or more meaningfully distinct use cases that each need separate explanation.

Infer the structure from file content, propose it to the user, and **wait for confirmation before reformatting**.

If content is ambiguous, do not guess. Present:

```
Could not determine structure for: grammar-index/grammar/<slug>.md
Content summary: <brief description>

Options:
  1. Structure 1 — shared structure across word types
  2. Structure 2 — distinct numbered use cases
  3. Skip restructuring for this file

What should I do?
```

#### Structure 1 and Structure 2 templates

The full templates for Structure 1 (shared structure across word types) and Structure 2
(distinct use cases) live in `_conventions.md`'s **## Structure format** section, labeled
"Grammar point files — Structure 1" and "Grammar point files — Structure 2" — reformat the
file into whichever template was confirmed above.

Section order follows `_conventions.md` **File structure rules**: Structure → Examples → Use Cases → Notes → See also.

Omit word-type sections and tense rows that do not apply. Each remaining row must have at least one inline example (`→ example`).

**Section distinction:**
- `## Structure` rows use `→` for short inline examples showing the pattern mechanically.
- `## Examples` holds full natural sentences showing real usage in context, one Markdown
  bullet (`- `) per sentence — see `_conventions.md` "## Examples content format".
- Within `## Structure`, order content: formation rules first, exception tables/blocks after — the reader must meet the basic pattern before its special cases, regardless of the order in the source lesson.

Each use case (Structure 2) is a numbered `##` header. Structure subsections follow the same word-type / tense pattern as Structure 1, limited to what applies. **Examples nest under each use case as its own `### Examples` subsection** — unlike Structure 1's single shared `## Examples` section, Structure 2 has no top-level Examples section at all; every example belongs to exactly one use case. If the attachment structure itself is identical across use cases (only the meaning/examples differ), repeat the shared `### Structure` content under each use case rather than hoisting it out — each use-case section must stay self-contained.

**Vocabulary files are out of scope for this skill.** Vocabulary files
(`grammar-index/grammar/vocabulary/**`) are structured at creation time by
`extract-grammar.md` Step 6c-ii (Vocabulary leaf files), using the same shared inference concept from
`_conventions.md`'s **## Structure format** section, and never enter this post-processing
pass. This is a documentation cross-reference only — this skill's container-file-detection
logic and file-path handling are unchanged; it is not extended to accept `vocabulary/` paths.

---

## Handoff summary

After processing all files, print:

```
structure-grammar — N files processed

  grammar-index/grammar/<slug>.md
    Structure: Structure 1 (shared) — confirmed by user

  grammar-index/grammar/<slug>.md
    Structure: container file — Step 7 skipped

  grammar-index/grammar/<slug>.md
    Structure: Structure 2 (use cases) — 2 use cases confirmed by user
```

Then ask (skip if running in **all** mode):

```
Run register-confusability-grammar on these files? (yes / no / all)
```

- **yes** — load `.cowork/skills/lesson-to-web/register-confusability-grammar.md` and pass the file list.
- **no** — end the skill.
- **all** — load register-confusability-grammar in all mode (which itself continues to see-also-grammar in all mode; no further handoff prompts after processing).
