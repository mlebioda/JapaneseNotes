---
name: scheduled-grammar-practice
description: >
  Interactive grammar practice session sourced from the spaced-repetition state
  file rather than a single lesson — selects grammar points scheduled for today
  or overdue for review across all lessons, loading each source lesson/extracted
  file lazily. Generates exercises, grades answers, and writes results back to
  the spaced-repetition state file. Requires an explicit scope keyword in the
  request — "today", "today's topics", "overdue", "due today", "drill overdue
  topics". Does NOT match lesson-code/filename-shaped input (e.g. "practice
  UN5GL14") — that shape belongs to lesson-grammar-practice instead.
---

# Scheduled Grammar Practice Skill

## Trigger

User says any of:
- "practice today's topics" / "practice grammar due today" / "drill today's grammar" → scope = TODAY
- "practice overdue topics" / "practice overdue grammar" / "drill overdue topics" → scope = OVERDUE

This skill only matches when the request contains an explicit scope keyword
("today", "today's topics", "overdue", "due today"). It does not match
lesson-code/filename-shaped input such as "practice UN5GL14" — that shape
belongs to `lesson-grammar-practice`.

---

## Scope resolution

This section runs immediately once scope = TODAY or scope = OVERDUE is
determined from the Trigger. It produces `selected_entries` — a list of
grammar point entries — which the session machinery then consumes exactly
as if they came from a single lesson file.

### TODAY flow

1. Read `.cowork/progress/grammar-state.json`. If missing, treat state as empty.
2. Filter entries: keep only those where `next_review` is a valid ISO date (YYYY-MM-DD) AND `next_review == today` (exact string equality). Entries where `next_review < today` are NOT included. Entries where `next_review > today` are NOT included.
3. Apply edge-case skips (see **Edge cases** below).
4. If 0 entries remain: print `Nothing is scheduled for today.` and stop.
5. Print `count grammar points scheduled for today.` and proceed to session.

### OVERDUE flow

1. Read `.cowork/progress/grammar-state.json`. If missing, treat state as empty.
2. Filter entries: keep only those where `next_review` is a valid ISO date (YYYY-MM-DD) AND `next_review < today` (strictly less than — NOT <= and NOT ==). Entries where `next_review == today` are NOT included.
3. Apply edge-case skips (see **Edge cases** below).
4. If 0 entries remain: print `No overdue grammar points — you're up to date.` and stop.
5. Sort remaining entries by `next_review` ascending (oldest next_review first = most overdue first).
6. Print `count grammar points are overdue. How many do you want to practice? (most overdue first, or 'all')` and wait for user reply.
7. Parse user reply X — evaluated in this exact order:
   - X is `"all"` → use all count entries (no extra message).
   - X is a positive integer > count → use all count entries, print `Only count overdue points found — using all.`
   - X is a positive integer == count → use all count entries (no extra message).
   - X is a positive integer < count → use the first X entries (already sorted oldest first).
   - X is invalid (non-integer, negative, zero) → ask once more with identical prompt. If still invalid: print `Invalid selection — session cancelled.` and stop.
8. Print `Starting session with X grammar points.` and proceed to session.

### Multi-lesson file loading

Once `selected_entries` is resolved:

1. Collect unique `lesson_file` values from `selected_entries`.
2. **Source-type branch** — for each `lesson_file` path, determine its source type before loading. Load lazily in both flows — only read a file on first demand. Each path is read at most once.
   - Path starts with `grammar-index/grammar/` → **extracted-file flow** (2a below).
   - Otherwise → **lesson-file flow** (2b below).

   **2a. Extracted-file flow:**
   - Call `.cowork/skills/practice-grammar/_practice-grammar-common.md`'s **Loading an
     extracted grammar file** routine on this `lesson_file` path. That
     routine performs the whole-file read, frontmatter parse, container-file
     guard (skip with warning if `## Sub-topics` is present), `grammar_header`
     resolution (file H1, with mismatch warning but no skip), and
     `body_text` assembly. See that routine for the full behavior — no
     behavioral change from before this refactor, this is a pure move.

   **2b. Lesson-file flow:**
   - Call `.cowork/skills/practice-grammar/_practice-grammar-common.md`'s **Loading a lesson file slice** routine on this `lesson_file` path (the shared `awk '/^# Summary$/{exit}' "$LESSON_FILE"` extraction).
   - For each selected entry, locate `grammar_header` in the loaded slice by searching `# 文法` and `# Vocabulary` sections for a `## Heading` match. Strategy: exact → case-insensitive → whitespace-normalised. If no match: skip with warning. If more than one match (ambiguous): skip with warning.
   - **Migration note:** role-based parsing can change the drill-point set for lessons first drilled under older level-based rules. `grammar-state.json` entries whose `grammar_header` no longer matches any heading are skipped with a warning (per the no-match rule immediately above) — when that warning fires, tell the user which entry was orphaned so they can re-practice the lesson or delete the stale entry.
3. Build merged vocab pool — see **Vocabulary base** below for how extracted-file topics contribute. For lesson-file entries the pool is unchanged: union of all `# ごい` + `# ひょうげん` tagged lines from all loaded lesson files (parsed per the common file's Vocab pool base rules). Deduplicate by Japanese form (full kanji+reading string). When the same form appears in multiple lesson files, keep the first occurrence (session-list order).
4. If all lesson/extracted files fail to load: print `Error: no lesson files could be loaded — session cancelled.` and report all warnings. Stop.

**N (the count shown to the user) is derived solely from `grammar-state.json`** — it equals the number of entries passing the date filter. Lesson/extracted-file load failures and warned-and-skipped entries do NOT reduce N.

### Edge cases

The following cause an entry to be skipped **silently** (no output):
- `next_review` missing, null, empty, or not a parseable YYYY-MM-DD date.

The following cause an entry to be skipped **with a warning line**:
- `lesson_file` missing or empty.
- `grammar_header` missing or empty.
- Lesson/extracted file path not found on disk.
- Lesson-file flow only: `grammar_header` not found in lesson file after all match strategies.
- Lesson-file flow only: `grammar_header` matches more than one heading in the lesson file (ambiguous).
- Extracted-file flow only: the file contains `## Sub-topics` (container file) — never drilled.

The following causes a warning line but does **not** skip the entry (extracted-file flow only):
- The entry's stored `grammar_header` differs from the file's H1 — the H1 is authoritative; continue using it.

---

## Parsing — scope-only additions

The common file (`_practice-grammar-common.md`) covers Grammar-topics
parsing, Vocab-pool base parsing, and Grammar point ID construction for the
base case. This section covers what only this trigger ever needs, layered on
top of the common file's rules.

### Use case extraction — extracted-file variant

**Extracted-file flow (`## Structure` / `## Use Cases` at H2 level)**: apply
the same three-way logic as the common file's lesson-file H3 use-case
extraction, but keyed on **semantic content, not markdown heading level or
bullet/heading style**:

1. **Multiple distinct structural sub-groups** — if `## Structure` (or `## Use Cases`) contains two or more genuinely distinct structural sub-groups (e.g. different verb-group conjugation patterns, different grammatical contexts, different registers of the same pattern), each sub-group is its own use case — regardless of whether the file expresses them as H3 subheadings, bold labels, bullets, or plain prose, and regardless of heading depth. Do not key this rule on any specific markdown construct (H3, numbered list, etc.) — those are incidental formatting choices that vary file to file. Label each use case with its sub-group's own heading/label text.
2. **Single unified pattern** — if `## Structure`/`## Use Cases` describes one pattern with no distinct sub-groups, the whole point is one use case (label: the grammar header / H1 itself). **This is the common case in current data** — verified against all 8 non-container files extracted so far (all from UN4GL14); only `o-go-v-masukudasai-respectful-request-form.md` has genuinely distinct sub-groups (Group 1/2 verbs vs. Group 3 vs. Exceptions — currently marked with H3 headings, but the rule above keys on the semantic grouping, not the H3 markup itself).

Same labels-stay-internal rule as the common file's use-case extraction — the
use case label must never appear in the exercise prompt.

**Unconfirmed against a second lesson**: this extracted-file rule set is
derived from a single-lesson sample (all 8 extracted files come from
UN4GL14). Re-validate against a second lesson's extracted files, which may
use different formatting conventions, once one is available.

Minimum: every grammar point yields at least one use case; there is no
maximum, same as the common file's rule.

### Vocabulary base (`Vocabulary/*.md` — extracted-file topics only)

Extracted-file topics have no lesson `# ごい`/`# ひょうげん` pool of their
own (the file itself contains no vocab section). When a session includes at
least one extracted-file topic, supplement the pool from `Vocabulary/*.md`:

- Source: every `.md` file directly under `Vocabulary/` (**top level only**) — skip the `Vocabulary/JLPT-decks/` subdirectory entirely.
- Collect only **plain tag lines** — never lines inside an Anki card-format block.
- **Block-boundary rule (explicit, mechanical)** — real files mix both formats, so apply this test to every `#w`/`#wc`/`#wp` line encountered:
  - A **card block** starts at a tag line whose next non-blank line is a card-field line (e.g. `ほんやく:`, `Przykład:`, `informal:`, `polite:`, `sonkeigo:`, `kenjougo:`, or any other `Label:` line). The block ends at the next `<!--ID:-->` line, **inclusive**, or at the next `---` separator line — whichever comes first. Never read past a card block's closing `<!--ID:-->` line back into plain-line collection; treat it strictly as the block's closing boundary.
  - A **plain usable line** is a `#w`/`#wc`/`#wp` tag line whose next non-blank line is **not** a card-field line — i.e. it is another tag line, a `---` separator, or end of file. Collect these into the pool.
  - Files vary in how the two formats mix: `Interview.md`/`Car.md` separate card blocks with `---`; `Bank-vocabulary.md`/`Post-vocabulary.md`/`Slownictwo-kolejowe.md` interleave plain tag lines directly between card blocks with no `---` separator; a file can also be 100% cards (e.g. `Interview.md`), yielding zero usable lines — that's fine, just move to the next file.
- For each usable line, parse `{japanese, reading, translation, type}` exactly as in the common file's lesson vocab pool, but the parsing must be **tag-position-agnostic**: the lesson-pool format is tag-last (`日本語（よみ）- translation #w`), while real `Vocabulary/*.md` plain lines are tag-first (`#w 日本語（よみ）- translation`). Accept both orders.
- Prefer topically relevant words when drawing from this base for a given extracted-file topic (best-effort judgment — deterministic topic_slug-to-file matching is Phase 2, not implemented here).

**Mixed-session pool merge**: the final pool for a session = union of
(lesson `# ごい`/`# ひょうげん` pools, from lesson-file entries) +
(Vocabulary base, from extracted-file entries). Apply the existing
dedup-by-Japanese-form rule across the merged pool (keep first occurrence,
session-list order). The existing outside-vocab rule (strict N5, used only
when the pool cannot express the grammar point) remains the final fallback
and is unchanged.

---

## Metadata-driven exercise generation (extracted-file topics)

This section applies only to grammar points loaded via the **extracted-file
flow** (Multi-lesson file loading, step 2a above). Their frontmatter fields
(`confused_with`, `register`, `function`, `topic_slug`) unlock additional
exercise-generation options beyond the base rules in
`_practice-grammar-common.md`'s **Exercise generation** section.
Lesson-file topics are unaffected — nothing in this section changes their
behavior.

### confused_with — Type 2 sourcing and minimal-pair contrast

- **On-demand distractor sourcing.** For an extracted-file topic, Type 2 distractors may be drawn from its `confused_with`-linked patterns **even when those patterns are not part of the current session**. Load `grammar-index/grammar/<slug>.md` on demand, read-only, solely to retrieve its pattern name (H1, or frontmatter `pattern` if the H1 is unavailable). This relaxes, for extracted-file topics only, the base Type 2 constraint that confusable forms must come from within the lesson itself.
- **Test-line seeding.** The pre-authored `— test: <question>` line under `## Often confused with` seeds Type 2 / Type 6 prompts — build the discrimination the exercise tests from that contrast question. Wrong-answer feedback quotes or derives from the test line.
- **Broken reference fallback.** If a `confused_with` slug does not resolve to an existing file under `grammar-index/grammar/` (confirmed live example: `o-go-v-masushimasu.md` lists `o-go-v-masukudasai`, but the real file is `o-go-v-masukudasai-respectful-request-form.md`), silently skip that specific pairing and fall back to ordinary Type 2 distractor selection for the topic. Never print a warning for this — it is a data-quality issue in the extract-grammar pipeline's output, outside this skill's control, and must never block or interrupt a session.
- **Minimal-pair contrast exercise.** When both halves of a `confused_with` pair are due in the same session **and land in the same generation batch** (batch-split prompt below — batches are formed by even-count split with no `confused_with`-awareness), generate one contrast exercise (built from the pair's test line) that **replaces** one exercise slot for each of the two topics. It does not add to the session — the total exercise count stays exactly as it would without the pair merge. The self-evaluation score from this one exercise counts toward SM-2 for **both** topics (both grammar_point_ids receive the same min_score/weak_points contribution from it).
  - **Phase-1 batching constraint (known limitation).** If both halves of a pair land in the **same** batch, apply the minimal-pair replacement above. If they land in **different** batches, do **not** attempt a cross-batch merge — treat each topic independently with ordinary Type 2 distractors (using the on-demand lookup above, which works regardless of batching). This gap is fully resolved by Task C's `topic_slug`-based batching (Phase 2, deferred) and is out of scope for Phase 1.
  - **`Exercise N / T` total.** `T` must be computed **after** pair-merging is applied, at session start — the progress indicator (see the common file's Interaction flow section) must reflect the merged (post-replacement) count, not the pre-merge count.

### register — situation matching and transformation flavor

- Exercise situations for an extracted-file topic must match its `register` frontmatter value **and** the prose in its own `## Register` section — never default to a generic "polite" or "formal" flavor without reading that section.
- **`register: polite`** — situations should be business/service/customer scenarios. One of the topic's existing use-case exercises may take a **plain ↔ keigo transformation** form (student converts a given plain-register sentence to the keigo pattern, or vice versa) as an **alternative form** — this does not add an exercise, it replaces the form of one that would exist anyway; session length is unchanged.
- **`register: tiered`** (confirmed live examples due day one: `teineigo-polite-expressions.md`, `uchi-soto-in-group-out-group.md`) — do **not** apply the polite-transformation flavor above. Instead, build situations that exercise the register-**selection** logic itself: e.g. the ウチ・ソト (in-group/out-group) boundary decision, or tier-escalation across a formality scale (ます／です → ございます／でございます). Read the pattern's own `## Register` section prose for the specific selection rule to drill — which parties, which contexts trigger which tier — rather than inferring a generic transformation.

### weak_points ↔ confused_with synergy

When a stored `weak_point` string for an extracted-file topic names a
pattern confusion (e.g. `"だけ vs しか"`), look up that topic's
`confused_with` list, load the counterpart file (same on-demand, read-only
rule as above), and build a targeted discrimination drill from its test line
and pattern name — this takes priority over a generic weak-point-biased
exercise for that topic (i.e. it overrides the common file's generic
Weak-point bias rule for extracted-file topics specifically).

---

## Workflow

1. **Resolve scope and `selected_entries`** — see **Scope resolution** above.
2. **Load source files** — see **Multi-lesson file loading** above (extracted-file flow in full; lesson-file flow delegates its awk-slice step to the common file's routine).
3. **Batch-split prompt.** After assembling `selected_entries`:
   - Ask: "X topics selected. How many batches would you like to split these into?" Wait for a positive integer `num_batches`.
   - If `num_batches` == 1 or the user says "none" / "no split": set `num_batches = 1` (no batch headers, no between-batch prompts).
   - If `num_batches` > total topics: inform the user "Only X topics available — running as a single batch." and set `num_batches = 1`.
   - If `num_batches` > 1: divide `selected_entries` evenly into `num_batches` ordered batches. First batch = entries 1 through ⌈total/num_batches⌉; last batch may be smaller. Do not reorder entries.
   - If the user gives an invalid answer (non-integer, negative, zero): ask once more with the same prompt. If still invalid: set `num_batches = 1`.
4. Load `.cowork/skills/practice-grammar/_practice-grammar-common.md`. Run its **Batch-loop mechanics** with the resolved `num_batches` — this covers loading `weak_points`, exercise generation (via the common file's **Exercise generation** plus this file's **Metadata-driven exercise generation** for extracted-file topics), presentation via **Interaction flow**, and grading via **Grading**.
5. On completion, use this skill's own **Session header and footer** (below) plugged into the common file's generic Session summary / batch-prompt formats.
6. Persist via the common file's **Persistence and Calendar sync** directive with `scope="TODAY"` or `scope="OVERDUE"` (matching the resolved scope).

Don't skip any step. Start practicing immediately after the user triggers
the skill.

---

## Session header and footer

For scope sessions (TODAY / OVERDUE), use these header and footer formats —
they plug into the common file's generic batch-prompt layout and Session
summary format in place of a single-lesson variant:

**Session header — Today:**
```
Session: today's topics — N exercises across M grammar points (K lessons). Reply with all answers in one message.
```

**Session header — Overdue:**
```
Session: overdue topics — N exercises across M grammar points (K lessons). Reply with all answers in one message.
```

**Session summary footer — Today:**
```
Session complete — today's topics (N exercises across M grammar points)
```

**Session summary footer — Overdue:**
```
Session complete — overdue topics (N exercises across M grammar points)
```

`K lessons` = count of distinct lesson files successfully loaded. `M` =
count of grammar points for which at least one exercise will be generated.

---

## Study Mode

Handled entirely by `.cowork/skills/practice-grammar/_practice-grammar-common.md`'s
**Study Mode** section — see that file for the invocation hookup. No
duplicate content here.

---

## Never touch

- Lesson files under `JPLessons/` (read-only — never write)
- `<!--ID: -->` lines anywhere
- `TARGET DECK` lines
- Do not run `git push` or any remote git operation
- See `.cowork/skills/practice-grammar/_practice-grammar-common.md`'s own Never-touch list for
  the full shared rule set (this skill loads that file for everything else)
