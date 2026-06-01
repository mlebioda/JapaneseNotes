---
name: see-also-grammar
description: >
  Populate ## See also sections in grammar files under grammar-index/grammar/ by
  scanning container files, then set proofread: true. Final step in the grammar
  post-processing pipeline. Trigger: "see-also grammar <file>" or called from
  structure-grammar.
---

# See Also Grammar Skill

## Trigger

- "see-also grammar `<slug>`" — filename without `.md`
- "see-also grammar grammar-index/grammar/`<slug>`.md" — full relative path
- (called automatically from structure-grammar with a list of file paths)

---

## Workflow

## Shared files

Load `.cowork/skills/lesson-to-web/_conventions.md` before starting.

---

Process each file in order. Apply both steps to one file before moving to the next.

---

### Step 8 — Populate ## See also

**Core rule: `## See also` must only contain links to container files (files with a `## Sub-topics` section). Never link to individual grammar point files.**

- A grammar point file may belong to multiple containers — all appear in its `## See also`.
- A container file links to peer container files from the same topic group (not to grammar points it owns).

**Orphan warning:** While reading topic files, check whether the current file's slug appears in at least one topic's `## Entries`. If not, warn:

```
[WARN] <slug>.md has no entry in any grammar-index topic file.
Add it manually or re-run extract-grammar classification (step 9).
```

To check all grammar files at once: `python3 .claude/scripts/grammar-audit.py --verbose`

#### Algorithm — grammar point files (no `## Sub-topics`)

1. Scan all files in `grammar-index/grammar/` (exclude `index.md` if present) that contain a `## Sub-topics` section.
2. For each container file, check whether the current file's slug appears in any of its `## Sub-topics` links.
3. Collect all container files that include the current file. Extract each container's pattern name from its `# heading`.
4. Format each as: `- [Container Name](/JapaneseNotes/grammar-index/<slug>) — <short phrase: what this container groups>`
5. Replace the entire content of `## See also` with the formatted list. If no containers include this file, write `*(none)*`.

#### Algorithm — container files (has `## Sub-topics`)

1. List all topic files in `grammar-index/` non-recursively. Exclude `index.md`:
   ```bash
   find grammar-index -maxdepth 1 -name "*.md" ! -name "index.md"
   ```
2. For each topic file, scan its `## Entries` for lines matching `- [Pattern Name](/JapaneseNotes/grammar-index/grammar/<slug>) · <level>`. Check whether any slug matches the current file's slug.
3. Collect all co-entry slugs from matching topic files. Exclude the current file's own slug. De-duplicate across files.
4. For each co-entry slug, read `grammar-index/<slug>.md`. If it has no `## Sub-topics` section, skip it. If it does, extract the pattern name from its `# heading`.
5. Format each as: `- [Container Name](/JapaneseNotes/grammar-index/<slug>) — <short phrase describing the relationship>`
6. Replace the entire content of `## See also` with the formatted list. If no container co-entries exist, write `*(none)*`.

---

### Step 9 — Set proofread: true

```bash
python3 .claude/scripts/grammar-process.py --set-proofread <file> [<file> ...]
```

If the script is unavailable, replace `proofread: false` with `proofread: true` in frontmatter manually. Do not modify any other frontmatter field.

---

## Completion report

After processing all files, print:

```
see-also-grammar — N files processed

  grammar-index/grammar/<slug>.md
    See also: 1 link added (sentence-final-particles group)
    → proofread: true

  grammar-index/grammar/<slug>.md
    See also: 2 links added (demonstratives group)
    → proofread: true

  grammar-index/grammar/<slug>.md
    See also: *(none)* — [WARN] no entry in any topic file
    → proofread: true
```

