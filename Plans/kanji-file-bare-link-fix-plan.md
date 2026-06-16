# Kanji-File: Bare Link Migration and Broken Link Removal Fix

## Status
DRAFT

## Goal

Two bugs were observed running `kanji-file` on existing kanji files that had old-style bare
wikilinks (written before the current section structure existed):

1. **Step 5** migrates all bare links (those appearing outside any `##` section) to
   `## Occurences`. This is wrong for links that represent structural parts (components OF the
   kanji). Those belong under `### Parts`, not `## Occurences`.

2. **Step 4** keeps links whose target file cannot be found in `Caligraphy/`, logging only a
   warning. The user expects such broken links to be removed outright.

Concrete example from `Caligraphy/Kanji/千-1000.md`:
- Original bare links: `[[丿 - component]]` (no file found), `[[十-ten,10]]` (component OF 千),
  `[[UN5KL2#千 - 1000・ち・セン]]` (lesson occurrence).
- Wrong result: all three were sent to `## Occurences`; `### Parts` was left empty.
- Correct result: `[[丿 - component]]` removed (no file); `[[十-ten,10]]` moved to `### Parts`;
  `[[UN5KL2#…]]` stays in `## Occurences` (lesson link — never touch rule already handles this).

The same pattern was confirmed across `百-100.md`, `後-after,back.md`, `左-left.md`,
`右-right.md`, and `円-yen.md` (already manually corrected by the user).

---

## Approach

Make two targeted changes to `.cowork/skills/kanji-file.md`:

**Change 1 — Step 4 (Link verification):** When a bare wikilink (no `#`) cannot be resolved to
any file in `Caligraphy/Kanji/` or `Caligraphy/Primitives/`, remove the link from the file
entirely instead of keeping it with a warning.

**Change 2 — Step 5 (Bare link migration):** Apply a classification step before migrating:
- Bare links without `#` that resolve to a file in `Caligraphy/Kanji/` or
  `Caligraphy/Primitives/` → move to `### Parts`.
- Bare links containing `#` → move to `## Occurences` (lesson occurrences; though these should
  already be skipped by the "never touch `#` links" rule).
- After Step 4 has run, any unresolved bare links will already have been removed, so Step 5
  only sees surviving (verified) component links.

**Change 3 — Step 6 (Consistency check):** Update the check language to reflect that broken
links are now removed rather than warned about, and that bare component links now land in
`### Parts` instead of `## Occurences`.

**Follow-up task:** Apply the fix manually to `千-1000.md` (still incorrect after the original
skill run): remove `[[丿 - component]]`, move `[[十-ten,10]]` to `### Parts`.

The ordering of Step 4 → Step 5 is important: Step 4 (removal of broken links) must run first
so that Step 5 (migration) only operates on verified links.

---

## Steps

1. Edit `.cowork/skills/kanji-file.md` — **Step 4 (Link verification)**
   - Change rule 3 from "log a warning; do not remove the link" to: "remove the link from the
     file and record it in the completion report as `REMOVED: [[<link>]] — no file found`".

2. Edit `.cowork/skills/kanji-file.md` — **Step 5 (Bare link migration)**
   - Replace the single-destination rule ("move to `## Occurences`") with a two-destination
     classification:
     - Bare links **without `#`** (component/kanji references, verified to exist by Step 4) →
       move to `### Parts`. If `### Parts` does not exist, create it.
     - Bare links **containing `#`** (lesson occurrence links) → move to `## Occurences`
       (existing behavior; these are already skipped by the "never touch `#`" rule, so in
       practice this branch is a safety catch only).
   - Update the section header in the skill accordingly.

3. Edit `.cowork/skills/kanji-file.md` — **Step 6 (Consistency check)**
   - Remove the line implying broken links are only warned about.
   - Add: "Verify no bare links remain outside named `##` sections after Steps 4–5."

4. Edit `.cowork/skills/kanji-file.md` — **Completion report examples**
   - Update the report format to show `REMOVED` lines and `### Parts migration` count instead
     of a single `bare link migration` count.

5. Fix `Caligraphy/Kanji/千-1000.md` manually (one-off data repair, not part of the skill
   rewrite):
   - Remove `[[丿 - component]]` from `## Occurences` (broken link — no file exists for 丿).
   - Move `[[十-ten,10]]` from `## Occurences` to `### Parts`.
   - Verify `[[UN5KL2#千 - 1000・ち・セン]]` remains untouched in `## Occurences`.

---

## Risks

- **`### Parts` already populated**: if a file already has a correctly filled `### Parts`
  section, Step 5's new logic may attempt to add duplicates. The de-duplicate rule ("each
  wikilink appears at most once") already guards against this — confirm it is enforced.
- **Lesson occurrence links with `#`**: the "never touch `#` links" rule in Step 4 already
  skips them. The new Step 5 classification adds a redundant safety catch; do not remove the
  original Step 4 skip rule.
- **千-1000.md manual fix**: this is a data file, not a skill file. No `<!--ID:-->` lines or
  `TARGET DECK` lines are present in kanji reference files, so edits are safe. Confirm by
  reading the file before editing.
