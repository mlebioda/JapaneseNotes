# Unify Structure Format Between Grammar Points and Vocabulary Files — Tasks

- [x] Read `.cowork/skills/lesson-to-web/_conventions.md`, `structure-grammar.md`, and
      `extract-grammar.md` in full immediately before editing (confirm exact current text/line
      positions haven't shifted since planning).
- [x] In `_conventions.md`, add new `## File structure rules (vocabulary file)` section
      (flat + numbered section orders; explicit list of what vocabulary files never carry;
      cross-reference to the grammar-point section and to
      register-confusability-grammar.md/see-also-grammar.md).
- [x] In `_conventions.md`, add new `## Structure format` section:
  - [x] Shared inference concept paragraph (single unified thing → flat; 2+ distinct things →
        numbered, examples never pooled across sections).
  - [x] Content-differs-by-type callout (grammar = conjugation table; vocabulary = free-form
        prose).
  - [x] Move Structure 1 template verbatim from `structure-grammar.md` into this section.
  - [x] Move Structure 2 template verbatim from `structure-grammar.md` into this section.
  - [x] Add new "Vocabulary files — flat (single sense)" template.
  - [x] Add new "Vocabulary files — numbered (2+ distinct senses)" template.
  - [x] Add "Applied by" closing note (structure-grammar.md Step 7 for grammar points;
        extract-grammar.md Step 7b for vocabulary files, creation-time only).
- [x] In `_conventions.md` `## Examples content format` section, replace the single vocabulary
      bullet (live text: "`### Examples` — inside vocabulary files ... Applies only to the
      Examples section itself; other copied content ... keeps whatever list/heading structure it
      already has in the source lesson") with two bullets covering flat `## Examples` and
      numbered `### Examples` shapes; remove the "other copied content ... keeps whatever
      structure it already has" caveat entirely (obsolete once extract-grammar.md stops copying
      vocabulary bodies verbatim); update the closing "Applies whenever this section is written
      or rewritten ..." paragraph to describe the vocabulary half via the new Step 7b
      flat/numbered inference instead of implying a flat copy-on-creation treatment.
- [x] In `structure-grammar.md`, remove the literal Structure 1 and Structure 2 template code
      blocks, replacing them with a reference to `_conventions.md`'s new `## Structure format`
      section, while retaining: the "Inferring which structure to use" one-liners and ambiguity
      prompt, "Section order follows..." paragraph, "Omit word-type sections..." paragraph, the
      "Section distinction" paragraph, and the Structure-2-specific numbered-header/scoping
      paragraph.
- [x] In `structure-grammar.md`, add one clarifying line that vocabulary files are out of scope
      for this skill and are structured at creation time by `extract-grammar.md` Step 7b instead
      — do not extend this skill to accept `vocabulary/` paths.
- [x] In `extract-grammar.md`, remove the "Do not add `## Structure`... sections" prohibition
      from the "Vocabulary file format" subsection.
- [x] In `extract-grammar.md`, add Step 7b-i (single-sense vs 2+-sense inference, with the
      user-confirmation prompt shown in the plan).
- [x] In `extract-grammar.md`, add Step 7b-ii (populate the file per the flat or numbered
      vocabulary template in `_conventions.md`'s `## Structure format` section, chosen per the
      Step 7b-i inference — reference by name only, do **not** restate the template markdown
      inline; the frontmatter block is the only content that stays literal in this step, since
      it's unique to file creation and isn't part of the shared Structure format templates).
- [x] In `extract-grammar.md`, rewrite "Rules for vocabulary file body" to describe
      reorganization into Structure/Examples buckets instead of verbatim copy, keeping the tag-
      prefix-stripping rule, the "no `## Use Cases`/`## Notes`/`## Register`/`## Often confused
      with`" rule, and the "no topic-index entry" rule unchanged.
- [x] Confirm no changes needed to `.cowork/skills/_heading-roles.md` (heading-role
      classification unaffected).
- [x] Confirm no changes needed to `register-confusability-grammar.md` (explicit `vocabulary/`
      scope guard, unaffected) or `see-also-grammar.md` (implicit exclusion via its
      `## Sub-topics`/`## Entries`-only scanning algorithm, unaffected).
- [x] Self-review: grep `structure-grammar.md` and `extract-grammar.md` for leftover Structure-
      format template markdown (stray `### Verb`/`Present:`/`Negative:` rows, or a second copy of
      the vocabulary flat/numbered skeletons) — confirm neither file restates the templates and
      both only reference `_conventions.md`'s `## Structure format` section.
- [x] Self-review: confirm `structure-grammar.md` was not extended to accept `vocabulary/` paths.
- [x] Confirm no vocabulary file under `grammar-index/grammar/vocabulary/**` was modified (out of
      scope — migration deferred).
