---
name: english-to-polish-grammar
description: >
  Given a Japanese grammar point as a lookup key only, identifies the cluster of
  confusable English constructs typically used to translate/express that meaning,
  and writes a Polish-language comparison note to English-gaps/<slug>.md. The
  Japanese grammar itself is never explained, mentioned, or referenced anywhere
  in the output -- the topic string is used only internally to detect the target
  English structures. Closes the real study gap: shakiness in the English used
  to translate a Japanese pattern, not in the Japanese pattern itself.
---

# English-to-Polish Grammar Gap Skill

## Trigger

User says:
- `english gap <topic>` (topic = a Japanese grammar point, used only as an internal lookup key)

## Hard rule

No Japanese text, romaji, or explanation of Japanese grammar appears anywhere in the output file, ever. The topic is used only inside this skill's own reasoning -- it is never written to disk.

---

## Workflow

### 1. Detect the English construct cluster

Follow this exact three-step procedure. Do not skip steps or jump straight to a guess.

1. **Gloss** -- translate the topic's core meaning into one internal English sentence-level gloss (never output; reasoning only).
2. **Candidates** -- list ~3-6 English grammatical forms that natively occupy that same semantic space.
3. **Narrow** -- from the candidates, keep only the subset (typically 2-4 constructs) that Polish speakers commonly confuse when translating that meaning, because Polish grammar (aspect, tense) doesn't map 1:1 onto them. Drop any candidate that isn't genuinely confusable in practice, even if it's technically a valid translation.

**Worked example** (the only one in this file -- use it as the template for the reasoning process, not as literal output text):

> `english gap ていた`
> - Gloss: a past state or action that was ongoing, or a past habit/lingering result -- often ambiguous.
> - Candidates: past continuous (was doing), used to + verb, simple past, past perfect continuous (had been doing).
> - Narrowed cluster: **past continuous vs. used to vs. simple past** -- past perfect continuous dropped, too rare to be a real confusion point for this topic.

### 2. Fallback -- fewer than 2 constructs

If step 3 above cannot confidently produce at least 2 constructs, stop before writing anything. Tell the user: "This topic didn't yield a clear multi-construct English gap." and ask them to rephrase or pick a related topic. Never write a single-construct file -- the template (comparison table, Szybkie porównanie, Częste błędy) assumes >= 2 constructs throughout.

### 3. Identify the primary construct

The primary construct is the one whose grammatical meaning most directly/literally corresponds to the gloss from step 1 -- i.e. the default textbook translation, not a stylistic variant. It is always listed first in the H1 title and is the source of the slug.

### 4. Derive the slug

Kebab-case the primary construct's key phrase, stripped of filler words.
- "to be about to" -> `about-to`
- "used to + verb" -> `used-to`

### 5. Duplicate check -- always run before writing anything

1. Look for an exact match at `English-gaps/<slug>.md`.
2. If none, scan the H1 titles and `##` headings of every other file in `English-gaps/*.md` for the primary construct's name appearing there (even as a non-primary/secondary entry) -- treat that as a near-match too.
3. If either check finds a match, show the user:
   - The matched file's path and H1 title.
   - Its current `##` heading list (the constructs it already covers).
   Then ask: **skip / append the delta / create a separate file with a different slug?** Wait for the user's choice. Never overwrite silently.
4. If no match at either step, proceed directly to generation as a new file.

### 6. Compute the delta (append mode only)

Parse the existing file's `##` headings to get the set of already-covered constructs. Delta = newly-detected cluster minus that set.
- **Empty delta** (full overlap, nothing new): tell the user there's nothing to add and stop. Offer skip or cancel -- "append" is not meaningful here.
- **Non-empty delta**: proceed to append only the delta constructs. Never regenerate, reorder, or touch constructs already present in the file.

### 7. Generate the note

New-file structure (follow `English-gaps/used-to.md` / `English-gaps/about-to.md` exactly):

1. `TARGET DECK: English-Gaps` -- literal first line, new files only.
2. H1 title naming all constructs in the cluster + ` - wyjaśnienie po polsku`, primary construct first.
3. One short Polish intro paragraph (new files only).
4. Per construct, one `##` section:
   - Short Polish explanation of when this construct is used.
   - `**Structure:**` line.
   - `| English | Polski |` table, **2-3 rows** (tighter than the reference files -- essentials only, no 3-4 row floor).
5. `## Szybkie porównanie` table: `Konstrukcja | Co opisuje | Przykład`, one row per construct.
6. `## Częste błędy`: bullet list, each entry `~~wrong~~` -> explanation -> correct version.
7. `# Summary` heading -- write it once; never modify its own text after it exists.
8. Below Summary: one flashcard per example-table row, in this exact format:
   ```
   Polish sentence (label - short tag) #card
   English sentence
   ```
   Blank line between cards. `label` = the construct's short name (e.g. "used to"), `short tag` = a 1-3 word tag matching the row's nuance (e.g. "nawyk").

**Append mode** (delta constructs only, onto an existing file):
- Update the H1 title line: append the delta constructs' names after the existing ones. Preserve the existing constructs' order and keep the existing file's primary construct first -- the file's identity doesn't change.
- Add new `##` sections for the delta constructs only (own Structure line, example table).
- Add the delta constructs' Częste błędy entries into the existing `## Częste błędy` list.
- Add corresponding rows to the existing `## Szybkie porównanie` table.
- Append corresponding cards under the existing `# Summary` heading, after the last existing card.
- Never touch, reorder, or regenerate any existing `##` section, table row, or card.

### 8. Write the file

New file: write to `English-gaps/<slug>.md`.
Append mode: edit the existing matched file in place, per the append-mode rules above.

---

## Scope boundary

This skill only ever writes inside `English-gaps/`. It never touches `JPLessons/`, `grammar-index/`, or any lesson file's `TARGET DECK` / `# Summary` / `<!--ID:-->` content.

## Never touch

- Lesson files under `JPLessons/` (read-only -- never write)
- `<!--ID: -->` lines anywhere
- `TARGET DECK` lines in lesson files (the literal `TARGET DECK: English-Gaps` line this skill writes as line 1 of new `English-gaps/` files is the sole exception -- it matches the existing reference files and is not a lesson file)
- Do not run `git push` or any remote git operation
- Do not modify other skill files or `.cowork/instructions.md`
