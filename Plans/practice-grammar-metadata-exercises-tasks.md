# Practice-grammar: metadata-driven exercise generation — Tasks

All edits target `.cowork/skills/practice-grammar.md` unless stated otherwise. Phase 2 tasks are DEFERRED — skip unless explicitly told otherwise.

## Phase 1 — Task A: dual-source topic resolution (prerequisite)

- [x] Add source-type branch to "Multi-lesson file loading": `lesson_file` starting with `grammar-index/grammar/` → extracted-file flow (whole-file read, no awk slice); otherwise → existing lesson-file flow unchanged
- [x] Extracted-file flow: `grammar_header` = H1; warn (don't skip) on H1 ≠ stored `grammar_header`, then use H1
- [x] Extracted-file flow: `body_text` = gloss + Structure + Examples + Use Cases (if present) + Notes (if present) + Register (if present) + Often confused with (if present); exclude frontmatter and `## See also`
- [x] Extracted-file flow: skip container files (`## Sub-topics`) with a warning naming the file
- [x] Extracted-file flow: parse frontmatter (`pattern`, `register`, `confused_with`, `function`, `topic_slug`, `level`) for exercise generation
- [x] Update Edge cases list: container-file skip warning; H1-authoritative rule for extracted files
- [x] Extend "Use case extraction" to extracted-file sections using a semantic rule (not keyed on markdown heading level/numbered lists): distinct structural sub-groups within `## Structure`/`## Use Cases` → one use case per sub-group, regardless of formatting; single unified pattern → one use case (the common case in current data); note rule is unconfirmed beyond the UN4GL14 sample
- [x] Add "Vocabulary base" pool: `Vocabulary/*.md` top level only, skip `JLPT-decks/`, only plain `#w`/`#wc`/`#wp` lines
- [x] Implement explicit block-boundary rule: card block = tag line immediately followed by card-field lines (`ほんやく:`, `Przykład:`, etc.) through the next `<!--ID:-->` line (inclusive) or next `---`, whichever first; plain usable line = tag line NOT immediately followed by card-field lines; never read past a card block's closing `<!--ID:-->` back into plain-line collection
- [x] Mixed-session pool merge: lesson pools + Vocabulary base, existing dedup rule; parsing must be tag-position-agnostic (accept both tag-last `... #w` and tag-first `#w ...` forms); strict-N5 outside-vocab rule remains fallback

## Phase 1 — Task B: mandatory metadata rules

- [x] Add new section "Metadata-driven exercise generation (extracted-file topics)"
- [x] confused_with: Type 2 distractors from linked files even when not in session (on-demand read-only load of `grammar-index/grammar/<slug>.md` for pattern name)
- [x] confused_with: `— test:` lines seed Type 2 / Type 6 prompts; wrong-answer feedback quotes/derives from the test line
- [x] confused_with: broken/unresolvable slug fallback — silently skip that pairing, fall back to ordinary Type 2 selection, no warning (data-quality issue outside this skill's control)
- [x] Minimal-pair contrast exercise when both halves of a confused pair are due together AND land in the same generation batch — REPLACES one exercise slot for each of the two topics (session N stable); score counts toward both topics
- [x] Batching constraint: if a confused pair spans two different batches, do NOT merge — treat each topic independently with ordinary Type 2 distractors; document as known Phase-1 limitation resolved by Task C (topic_slug batching)
- [x] Register: exercise situations must match `register` frontmatter + `## Register` section
- [x] Register: `register: polite` → business/service/customer scenarios, plain↔keigo transformation flavor
- [x] Register: `register: tiered` → do NOT apply polite transformation; situations exercise the register-selection logic itself (e.g. uchi/soto boundary, tier-escalation) per the pattern's own `## Register` section prose
- [x] Grading section: add register dimension — grammatically correct but wrong register = mistake with register-specific feedback (cite the specific selection rule violated for `tiered` patterns)
- [x] Register-transformation flavor (plain ↔ keigo) for `register: polite` patterns only — alternative form of one existing use-case exercise, no extra exercises
- [x] weak_points ↔ confused_with synergy: weak_point naming a pattern confusion → look up confused_with, build targeted discrimination drill
- [x] Update "Type selection rule" + "Weak-point bias" paragraphs to reference metadata sources without changing lesson-file behavior
- [x] Ensure `Exercise N / T` total T is computed after pair-merging, at session start

## Phase 1 — verification and bookkeeping

- [x] Verify `.cowork/skills/practice-grammar-srs.md` and `practice-grammar-study-mode.md` need no changes; if a hidden lesson-path assumption is found, stop and report — do not edit helpers
- [x] Ask user for permission before adding one line about extracted-file support to the practice-grammar description in `.cowork/instructions.md` (never modify without explicit permission)
- [x] Self-review: confirm lesson-triggered sessions and lesson-file scheduled entries behave exactly as before

## Phase 2 — Task C (DEFERRED — skip unless explicitly requested)

- [ ] [PHASE 2] `function`-based grouping: same-function due topics as mutual Type 2 distractors; function → type heuristics (request/permission/prohibition → 1/3; conditional/temporal → 4; hearsay-appearance → 5)
- [ ] [PHASE 2] `topic_slug`-based batching in scheduled sessions (coherent batches)
- [ ] [PHASE 2] Deterministic topical vocab preference when drawing from `Vocabulary/` (match file topic vs topic_slug/function)
