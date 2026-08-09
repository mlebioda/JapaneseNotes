# english-to-polish-grammar skill

## Goal
Add a new standalone skill that, given a Japanese grammar point as a lookup key only, identifies the cluster of confusable English constructs typically used to translate/express that meaning, and produces a Polish-language comparison note in `English-gaps/` — matching the format of the existing `English-gaps/used-to.md` and `English-gaps/about-to.md` files. The Japanese grammar itself is never explained, mentioned, or referenced anywhere in the output; the Japanese topic string is used only internally to detect the target English structures. This closes the real study gap: the user's shakiness is often in the English used to translate a Japanese pattern, not in the Japanese pattern itself.

## Approach
A new standalone skill `.cowork/skills/english-to-polish-grammar.md` triggered by `english gap <topic>`. On invocation it: (1) silently maps the Japanese topic to its associated English construct cluster using the model's own grammar knowledge — no Japanese appears in any output, (2) derives a kebab-case slug from the primary/most central English construct, (3) checks `English-gaps/` for an existing file with that slug, and if found, shows the user the existing file's title and covered constructs before asking whether to skip, append new material, or create a separate file — never overwriting silently, (4) if proceeding, generates the full note (Polish intro, one `##` section per construct with a **Structure:** line and a tight 2–3 row example table, a "Szybkie porównanie" table, a "Częste błędy" section, `# Summary`, then one Anki flashcard per example row) and writes it to `English-gaps/<slug>.md` with `TARGET DECK: English-Gaps` as the literal first line. Kept deliberately concise per prior feedback that long skill files cause steps to get skipped.

## Steps
1. Create `.cowork/skills/english-to-polish-grammar.md` — new skill file, starting with standard YAML frontmatter (`name`/`description`, matching the convention used in `manage-holidays.md`), covering:

   - **Trigger:** `english gap <topic>` (topic = Japanese grammar point, used only as a lookup key)

   - **Hard rule:** no Japanese text, romaji, or grammar explanation anywhere in the output file, ever

   - **Detection procedure** (concrete, repeatable — not an implicit judgment call). The skill file must encode this exact sequence:
     1. Translate the topic's core meaning into a one-line internal English gloss (never output).
     2. List the English grammatical forms that natively occupy that same semantic space (brainstorm ~3–6 candidates).
     3. Narrow to the subset Polish speakers commonly confuse when translating that meaning — typically 2–4 constructs, kept because Polish grammar (aspect, tense) doesn't map 1:1 onto them. Drop candidates that aren't genuinely confusable in practice.
     - One worked example written directly into the skill file (single example only, to keep the file short):
       `english gap ていた` → gloss: "a past state or action that was ongoing, or a past habit/lingering result — often ambiguous" → candidates: past continuous (was doing), used to + verb, simple past, past perfect continuous (had been doing) → narrowed cluster: **past continuous vs. used to vs. simple past** (past perfect continuous dropped — too rare to be a real confusion point for this topic).

   - **Fallback rule:** if step 3 above cannot confidently produce at least 2 constructs, stop before writing anything. Tell the user the topic didn't yield a clear multi-construct English gap, and ask them to rephrase or pick a related topic. Never write a single-construct file — the template structure (comparison table, Szybkie porównanie, Częste błędy) assumes ≥2 constructs throughout.

   - **Primary construct rule:** the primary construct is the one whose grammatical meaning most directly/literally corresponds to the topic's core gloss from step 1 (i.e., the default textbook translation, not a stylistic variant). It is always listed first in the H1 title and is what the slug is derived from.

   - **Slug derivation:** kebab-case of the primary construct's key phrase, stripped of filler words (e.g. "to be about to" → `about-to`, "used to + verb" → `used-to`).

   - **Duplicate check:** first look for an exact match at `English-gaps/<slug>.md`. If none, also scan the H1 titles of existing `English-gaps/*.md` files for the primary construct's name appearing as a secondary (non-primary) entry in another file's construct list — treat that as a near-match too. If any match is found, show the user that file's title and its `##` heading list (the constructs it currently covers), then ask: skip / append the delta / create a separate file with a different slug. Wait for the user's choice before writing anything.

   - **Determining the delta (for append mode):** parse the existing file's `##` headings to get the set of already-covered constructs. Delta = newly-detected cluster minus that set.
     - If delta is empty (full overlap — nothing new), tell the user there's nothing to add and stop (offer skip or cancel; "append" is not meaningful here).
     - If delta is non-empty (partial or no overlap), proceed to append only the delta constructs — never regenerate or reorder constructs already present.

   - **Generation step** (new file, or the delta portion when appending): follow the exact structure from `English-gaps/used-to.md` / `English-gaps/about-to.md`:
     1. `TARGET DECK: English-Gaps` (first line, literal — new files only)
     2. H1 title naming the constructs + "- wyjaśnienie po polsku" (primary construct first)
     3. Short Polish intro paragraph (new files only)
     4. Per construct: `##` heading, short Polish explanation, **Structure:** line, `| English | Polski |` table with 2–3 rows (tighter than the existing files — essentials only, not a 3–4 row floor)
     5. "Szybkie porównanie" table: Konstrukcja | Co opisuje | Przykład
     6. "Częste błędy": bullet list, `~~wrong~~` → explanation → correct version
     7. `# Summary` heading (never modify this heading's own text once present)
     8. Below Summary: one flashcard per example row — `Polish sentence (label - short tag) #card` then English sentence on the next line, blank line between cards

   - **Append-mode behavior:** when the user chooses "append" on a duplicate:
     - Update the H1 title line to include the newly-added delta constructs' names, appended after the existing ones (preserve existing order, primary construct of the *existing* file stays first since the file's identity doesn't change)
     - Add new `##` sections for each delta construct (with its own Structure line, example table, and Częste błędy entries)
     - Add corresponding rows to the existing Szybkie porównanie table
     - Append corresponding cards under the existing `# Summary`
     - Never touch, reorder, or regenerate existing `##` sections, table rows, or cards

   - **Explicit boundary reminder:** this skill only ever writes inside `English-gaps/`; never touches `JPLessons/`, `grammar-index/`, or lesson `TARGET DECK`/`# Summary`/`<!--ID:-->` content

2. Create `.claude/commands/english-to-polish-grammar.md` — slash command stub invoking the skill (flat file, matching the pattern of `reading-jlpt.md`, `manage-holidays.md`, since this is a standalone skill, not nested).
3. Update `.cowork/instructions.md`:
   - Add an `English-gaps/` entry to the "Directory map" section (currently missing despite the directory existing on disk) — e.g. `` `English-gaps/` — Polish-language comparison notes for confusable English grammar constructs, generated by english-to-polish-grammar (not lesson files) ``
   - Add one line under "Available skills" documenting `english-to-polish-grammar` and its trigger, consistent with how every other skill is listed there
   - (Requires user permission to edit `.cowork/` per project rules — confirm before editing.)

## Risks
- None to plugin export data — this skill never touches lesson files, `TARGET DECK`, `# Summary` (lesson meaning), or `<!--ID:-->` lines; it only creates/appends files under `English-gaps/`.
- Slug collisions across unrelated construct clusters are possible if two different meanings produce similar primary-construct names — mitigated by the mandatory duplicate-check-and-ask step (never silent overwrite), including the near-match scan across existing H1 titles.
- If detection is too permissive it could produce a low-confidence multi-construct cluster instead of correctly falling back — mitigated by requiring the skill to explicitly self-assess against the ≥2-constructs confidence bar before proceeding.
- Editing `.cowork/instructions.md` requires explicit user permission per project rules; flagged as a separate confirmable step.
