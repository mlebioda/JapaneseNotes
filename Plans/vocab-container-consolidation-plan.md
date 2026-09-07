# Consolidate Per-Lesson Vocabulary Containers Into Shared POS Files

## Goal

`extract-grammar.md` currently creates a brand-new one-off "container" file under
`grammar-index/grammar/` every time a lesson's `# Vocabulary` section has a POS-grouping
heading (`### Verbs`, `### Nouns`, `### Adjectives`) — e.g. `un5gl13-verbs.md`,
`un5gl15-verbs.md`, `dekiru-verbs.md`, `verbs-tsukiau.md`, `verbs-informing-un4gl13.md`. Each
of these exists only to list that one lesson's vocabulary leaf files
(`grammar-index/grammar/vocabulary/<subdir>/*.md`) under a `## Sub-topics` section — they carry
no grammar content of their own, get topic-classified and cross-linked into the confusability
graph like real grammar containers, and multiply 1:1 with lessons even though "Verbs" isn't a
distinct concept per lesson.

This plan replaces that with a small number of **shared, flat, POS-keyed files**
(`grammar-index/grammar/vocabulary-verbs.md`, created on first use; `vocabulary-nouns.md` /
`vocabulary-adjectives.md` created the first time a Nouns/Adjectives POS heading is actually
extracted) that every lesson's vocabulary entries of that part of speech append into over time,
instead of spawning a new file per lesson. Entries are grouped under a `### <Theme Name>`
sub-heading only where a genuine shared theme exists across 2+ entries; everything else stays a
flat, ungrouped bullet. These files are excluded from topic classification and the entire
post-processing pipeline, matching how `grammar-index/grammar/vocabulary/**` leaf files are
already treated today.

## Resolved decisions (user interview)

1. **Location** — flat under `grammar-index/grammar/`, e.g. `grammar-index/grammar/vocabulary-verbs.md`
   — not nested under `grammar-index/grammar/vocabulary/`.
2. **Grouping** — thematic, not lesson-keyed. A `### <Theme Name>` sub-heading is used only when
   2+ entries genuinely share a topic (the user's own example: と思います and と言います could group
   under something like "Expressing opinions"). An entry with no natural thematic sibling stays a
   flat, ungrouped bullet directly under the literal `## Sub-topics` heading — same as today's
   single-lesson container already does when it has nothing to sub-group.
3. **Scope exclusion** — consolidated files skip topic classification (no `topic_slug` entry, never
   appear in a topic file's `## Entries`) **and** skip the entire post-processing pipeline
   (preprocess / review / structure / register-confusability / see-also) — same treatment as
   `vocabulary/**` leaf files get today.
4. **Adjectives file** — do not pre-create `vocabulary-adjectives.md` (or `vocabulary-nouns.md`)
   now; create either only the first time a heading of that POS is actually extracted, mirroring
   how `grammar-index/grammar/vocabulary/Adjectives/` itself was never pre-created.

## Finding: the "6 existing containers" are actually 5 + 1 unrelated file

`grep -l "^pattern: Verbs$" grammar-index/grammar/*.md` returns six files, but only five are
genuine vocabulary-only containers in scope for this migration:

| File | Lesson | Groups |
|---|---|---|
| `dekiru-verbs.md` | UN4GL1 | 1 vocabulary leaf (`vocabulary/Verbs/dekiru-can-to-be-built-completed`) |
| `un5gl13-verbs.md` | UN5GL13 | 2 vocabulary leaves (と思います, と言います) |
| `un5gl15-verbs.md` | UN5GL15 | 3 vocabulary leaves (渡す, 渡る, できる) |
| `verbs-tsukiau.md` | UN4GL6 | 1 vocabulary leaf (付き合う) |
| `verbs-informing-un4gl13.md` | UN4GL13 | 1 vocabulary leaf (知らせる) |
| **`kenjougo-verbs.md`** | UN4GL14 | **3 real grammar-index/grammar/ pattern files** (特別な動詞, お・ご V「ます形」します, お・ご V「ます形」いたします) — sourced from `# 文法`, not `# Vocabulary` |

`kenjougo-verbs.md` is a genuine grammar-pattern container: it groups standalone grammar point
files (not vocabulary leaves), is topic-classified (`humble-expressions`), and is deeply
cross-linked — 5 other files' `## See also` sections point to it
(`kenjougo-tokubetsunadoushi.md`, `o-go-v-masuitashimasu.md`, `keigo.md`,
`kenjougo-humble-expressions.md`, `o-go-v-masushimasu.md`). It must **not** be touched by this
plan — it is out of scope, not part of the migration, and the routing rule below (§"Routing
change") only fires for containers sourced from `# Vocabulary`, so `kenjougo-verbs.md`'s
`### Verbs` heading (sourced from `# 文法`) is naturally excluded by construction. Flagging this
now so it isn't accidentally swept in during implementation or migration.

## New file format

`grammar-index/grammar/vocabulary-<pos>.md` (`<pos>` ∈ `verbs` / `nouns` / `adjectives`):

```
---
pattern: Verbs
topic_slug: ""
proofread: false
---

# Verbs

> Verb vocabulary consolidated across lessons.

## Sub-topics

### <Theme Name>

- [<label>](/JapaneseNotes/grammar-index/grammar/vocabulary/Verbs/<slug>) · <level>
- [<label>](/JapaneseNotes/grammar-index/grammar/vocabulary/Verbs/<slug>) · <level>

- [<label>](/JapaneseNotes/grammar-index/grammar/vocabulary/Verbs/<slug>) · <level>
```

Differences from today's per-lesson container frontmatter:
- **No `lesson:` field** — the file spans many lessons; provenance is still one hop away in the
  linked leaf file's own `lesson:` frontmatter, so nothing is lost, just no longer inline. (An
  alternative considered: append `· <lesson-code>` to each bullet. Rejected — keeps the format
  identical to existing container bullets and avoids two sources of truth for a lesson code that
  the leaf file already owns.)
- **No `level:` field** — entries span multiple JLPT levels; level stays per-bullet as it already
  is today.
- **`topic_slug: ""`** (empty string, not `[]`) — matches the `vocabulary/**` leaf-file convention
  (never classified), not the old per-lesson container convention (`[]`, later filled as a list).
- **`proofread: false`, never touched** — matches leaf-file convention; this file never enters
  the post-processing pass that would otherwise flip it to `true`.
- The literal `## Sub-topics` heading is unchanged — it stays the load-bearing container-detection
  signature other skills key off (see "Cross-skill exclusion" below), just re-labeled internally
  in this plan to support thematic sub-grouping instead of being an implicit lesson-code
  container.

**Un-grouped vs themed bullets**: a themed group is a `### <Theme Name>` heading followed by its
member bullets; an ungrouped entry is a bare bullet with no `###` above it. Both can coexist in
the same file (mixed), matching decision 2 exactly — nothing is forced into a theme that doesn't
exist.

## Routing change — `extract-grammar.md` Step 7

Today, a `container`-classified heading sourced from `# Vocabulary` (i.e. `### Verbs` /
`### Nouns` / `### Adjectives` under the lesson's `# Vocabulary` section, grouping only
Vocabulary-sourced `grammar` children) uses the generic "Container file format" and creates a new
lesson-scoped file (`<lesson-or-content-slug>-verbs.md`).

New rule: when a `container` heading is (a) sourced from `# Vocabulary` **and** (b) its
normalized heading text is exactly `Verbs`, `Nouns`, or `Adjectives` (matching the vocabulary
subdir names) **and** (c) its children are exclusively Vocabulary-sourced `grammar` headings
(i.e. it purely groups vocabulary leaves, not other containers) — route it to the shared
consolidated file (§"Append-time theming gate" below) instead of creating a new file. Any other
`# Vocabulary`-sourced container (a non-POS-named grouping, or one that mixes in a nested
container) keeps today's one-off container behavior unchanged — this is a narrow, deliberate
scope: no evidence of such a case exists in the vault today (all five migrated containers are
plain `### Verbs`), so it's called out as an edge case rather than designed against speculatively.

A `container` heading sourced from `# 文法` is **never** affected by this rule regardless of its
heading text — this is what keeps `kenjougo-verbs.md`-style containers (grammar patterns grouped
under a `### Verbs` heading inside a 文法 section) on the existing container-file path.

**Literal replacement text — Step 4b carry-forward list.** The current "Carry the classification
forward" bullet list (`.cowork/skills/lesson-to-web/extract-grammar.md`, § "4b. Classify headings
— ask the user") reads:

```
Carry the classification forward:
- `grammar` from `文法` → `grammar-index/grammar/<slug>.md` (normal flow, steps 5–11)
- `grammar` from `Vocabulary` → `grammar-index/grammar/vocabulary/<subdir>/<slug>.md` (vocabulary file format, step 7b)
- `container` → step 7 creates a container file; step 8 inserts wikilink in lesson
- `skip` → no file created, no wikilink inserted
```

Replace the single `container` bullet with two bullets, verbatim:

```
Carry the classification forward:
- `grammar` from `文法` → `grammar-index/grammar/<slug>.md` (normal flow, steps 5–11)
- `grammar` from `Vocabulary` → `grammar-index/grammar/vocabulary/<subdir>/<slug>.md` (vocabulary file format, step 7b)
- `container` sourced from `# Vocabulary`, whose normalized heading text is exactly `Verbs`,
  `Nouns`, or `Adjectives`, and whose children are exclusively Vocabulary-sourced `grammar`
  headings → routes to step 7c (vocabulary POS container, consolidated) instead of step 7;
  step 8 inserts a bare, anchor-less wikilink to `grammar-index/grammar/vocabulary-<pos>.md`
- `container` (any other case — a non-POS-named `# Vocabulary` heading, one that mixes in a
  nested container, or **any** `# 文法`-sourced container regardless of heading text) → step 7
  creates a container file; step 8 inserts wikilink in lesson
- `skip` → no file created, no wikilink inserted
```

**Literal insertion text — Step 7 "Container file format" section.** Immediately after the
existing container template block and its two following sentences ("List only the sub-headings
that were classified as `grammar` or `container` (not `skip`)." / "As with grammar point files,
always omit `## Notes` on creation — never emit an empty section."), insert this new sentence
verbatim, as its own paragraph:

```
**Not used for a routed Vocabulary POS container.** A `container` heading matching the Step 4b
routing criteria (§"Routing change") uses the consolidated file format and append logic in Step 7c
instead of this template — this template is only ever used for the non-routed container cases
listed in the Step 4b carry-forward bullets above.
```

## Append-time theming gate (new Step 7c)

This replaces file *creation* with file *append* for the routed case above. Runs after the
vocabulary leaf files themselves are created (so their slugs/labels are known) and before the
lesson-file wikilink step (Step 8, updated below).

**Runs regardless of Step 6's Created/Skip outcome for the underlying leaf.** Step 7c fires for
every Vocabulary-sourced leaf file under a routed container heading whether Step 6 resulted in
*Created* (a new leaf file this run) or *Skip* (the leaf file already existed from a prior run) —
its own per-entry dedup (the link-target check in item 2 below) is the only gate Step 7c needs, and
is sufficient on its own regardless of which case produced the leaf. This must be stated as a
general rule extract-grammar.md carries going forward, not treated as true only incidentally for
this migration: the migration itself (§"Migration of the 5 existing containers" below) depends on
Step 7c firing for entries that are *all* pre-existing leaf files (Skip, not Created, since they
were extracted in earlier runs before this plan existed) — if Step 7c were gated on Step 6's
Created outcome the way Step 8 and Step 9 are (see their "Only for files Created in step 7" /
"Only process files that were Created" rules), the migration's own append step would never fire,
and future non-migration lessons whose vocabulary leaves already exist (e.g. a re-run, or a leaf
extracted by hand before Step 7c existed) would silently fail to get themed/appended. This is the
one place in the pipeline that deliberately does **not** inherit the "Created only" gate used
everywhere else (Step 8, Step 9) — call this out explicitly in the skill file so a future editor
doesn't "fix" it into matching Step 8/9's gate by mistake.

1. **Read the target file** (`grammar-index/grammar/vocabulary-<pos>.md`) if it exists; otherwise
   this append creates it fresh with the format above and an empty `## Sub-topics` body — no
   theming decision needed for a first entry, skip straight to step 3.
2. **Per-entry dedup (idempotency)** — before adding any new bullet, check whether a bullet
   already links to this exact `grammar-index/grammar/vocabulary/<subdir>/<slug>` path anywhere
   in the file (inside any theme, or ungrouped) — search by the **link target path**, not by a
   lesson-code section (there is no longer a per-lesson section to key off — see "Idempotency
   check update" below). If found, skip — do not add a duplicate bullet.
3. **Propose theme placement to the user** — for each new entry being appended (there may be
   several from one lesson, e.g. UN5GL15's three verbs), and considering it against both the
   *existing* themed groups in the file and the *other new entries from this same run*, propose
   one of:
   - **Join an existing theme** — the new entry genuinely shares that theme's topic with its
     current members.
   - **Start a new theme** — 2+ of the entries being considered (existing ungrouped entries in
     the file, and/or entries from this run) share a genuine topic not yet represented as a theme.
   - **Stay ungrouped** — no genuine shared topic found; add as a flat bullet.

   Prompt format (same style as `structure-grammar.md`'s ambiguity prompt and Step 7b-i's
   sense-count prompt):
   ```
   New vocabulary entries to add to grammar-index/grammar/vocabulary-verbs.md:
     - 渡す（わたす）- to hand over  (N5, from UN5GL15)
     - 渡る（わたる）- to cross / go overseas  (N5, from UN5GL15)
     - できる - can  (N5, from UN5GL15)

   Existing themes in the file: <list, or "(none yet)">
   Existing ungrouped entries: <list, or "(none)">

   Proposed placement:
     1. 渡す, 渡る → new theme "渡す／渡る (transitivity pair)" — both are the transitive/
        intransitive pair of the same root
     2. できる → ungrouped (no shared theme found with existing entries)

   Confirm, or override any entry's placement (join <theme name> / new theme <name> / ungrouped)?
   ```
   Wait for confirmation before writing. A user override is used verbatim.
4. **Never force a theme** — this mirrors the "don't force `## Often confused with` matches"
   caution already used in `register-confusability-grammar.md`. If nothing genuine is found,
   propose "stay ungrouped" as the default, not a strained theme.
5. **Write the append**:
   - Themed placement: insert the bullet under the matching `### <Theme Name>` heading (creating
     the heading, immediately after `## Sub-topics`, if this is the theme's first appearance —
     or immediately after the last existing themed group if joining one already created).
   - Ungrouped placement: append the bullet as a flat, un-headed bullet — grouped conventionally
     after any themed sections, or interspersed; keep it simple and append flat bullets at the end
     of the file's `## Sub-topics` content, after all themed groups, so themed groups stay visually
     contiguous at the top.
   - Bullet format is unchanged from today: `- [<label>](/JapaneseNotes/grammar-index/grammar/vocabulary/<subdir>/<slug>) · <level>`.

## Idempotency check update (Step 6)

The existing Step 6 dedup for grammar/container files (`grep -rlF 'pattern: <exact heading
text>'`) does not apply to the consolidated file — its `pattern:` frontmatter is always the fixed
POS name (`Verbs`), which would trivially "match" on every single append and is useless as a
duplicate signal. For the consolidated-file path specifically, idempotency is entirely handled by
Step 7c's per-entry link-target check (§ above) — dedup by the vocabulary leaf file's path, not by
a lesson-code section or by frontmatter `pattern` text. This is the direct consequence of moving
from lesson-keyed sections to thematic ones: there is no longer a predictable per-lesson anchor to
check against, so the check must live at the entry (bullet) level instead of the file/section
level.

## Lesson-file wikilink (Step 8) — no per-lesson anchor

Previously, a lesson's `### Verbs` heading got a wikilink to its own dedicated container file
(`[[grammar-index/grammar/un5gl15-verbs]]`), which doubled as a deep anchor — opening that link
always landed on exactly that lesson's entries. Under thematic grouping, a lesson's vocabulary
entries can scatter across multiple themes or land ungrouped, so **no predictable per-lesson
anchor exists inside the shared file**. This is a deliberate, called-out consequence, not an
oversight:

- The wikilink inserted under the lesson's `### Verbs` heading becomes a link to the **bare
  consolidated file** — `[[grammar-index/grammar/vocabulary-verbs]]` — landing at the top of the
  file, same as any other wikilink to a page without an anchor. No deep-link behavior is
  preserved or attempted.
- This is a real (small) navigation regression versus today's one-lesson-one-file setup, accepted
  in exchange for not duplicating "Verbs" containers per lesson. Not something to silently
  degrade — surfaced here for the user's final sign-off before implementation.

## Cross-skill exclusion (structure-grammar / register-confusability / see-also)

All three post-processing skills currently detect "container file" purely by the presence of a
`## Sub-topics` heading (`structure-grammar.md` "Container file detection",
`register-confusability-grammar.md` "Container / vocabulary scope guard",
`see-also-grammar.md`'s container-scanning algorithm). The new consolidated files keep that same
`## Sub-topics` heading (needed for the container-detection signature to still work per decision
2), which means, without a further change, these three skills would still technically recognize
`vocabulary-verbs.md` as a "container" and:
- `structure-grammar.md` / `register-confusability-grammar.md`: already **skip** files they detect
  as containers for their own normalization/register/confused-with steps — so if either were ever
  invoked directly on `vocabulary-verbs.md` (e.g. a manual "structure grammar vocabulary-verbs"
  call, not part of the normal pipeline), the existing container-skip logic already produces the
  correct no-op behavior. No code change strictly required here, but see below for the more
  important guard.
- `see-also-grammar.md`'s "scan all files in `grammar-index/grammar/` with `## Sub-topics`" step
  (used when computing *other* files' backlinks) would include `vocabulary-verbs.md` in its
  candidate-container pool. In practice this produces no incorrect output today — a real grammar
  point's slug never appears among `vocabulary-verbs.md`'s bullets (which only ever link to
  `vocabulary/<subdir>/*` leaf slugs), so no false backlink is ever added — but it is wasted work
  and conceptually wrong to scan it at all, since decision 3 puts these files entirely outside the
  confusability graph.

**Concrete guard to add**: give all three skills an explicit, filename-based exclusion — a file
directly under `grammar-index/grammar/` whose basename matches `vocabulary-*.md` (i.e.
`vocabulary-verbs.md`, `vocabulary-nouns.md`, `vocabulary-adjectives.md`) is never treated as a
container or scanned as one, regardless of whether it has a `## Sub-topics` heading. This is
simpler and more robust than relying on `## Sub-topics` presence/absence alone (which must stay
present for decision 2's grouping mechanics) and gives a single, unambiguous signature the three
skills can share. Concretely:
- `structure-grammar.md` "Container file detection" — add: "Files matching
  `grammar-index/grammar/vocabulary-*.md` are vocabulary consolidation files, not containers —
  never processed by this skill at all (not even the container-skip log line); this guard is
  checked before the `## Sub-topics` check."
- `register-confusability-grammar.md` "Container / vocabulary scope guard" — same addition,
  alongside the existing `vocabulary/` subdirectory guard (this is a sibling case: the exclusion
  is now by top-level filename pattern *in addition to* the `vocabulary/` subdirectory rule, not a
  replacement for it).
- `see-also-grammar.md` — exclude `grammar-index/grammar/vocabulary-*.md` from the "scan all files
  with `## Sub-topics`" candidate-container pool used when computing other files' backlinks.

**Never invoked directly**: because these files are never in the "Created" list `extract-grammar`
step 10 offers to preprocess-grammar (§"Scope exclusion" below — same as leaf vocabulary files
today), the normal pipeline never reaches them. The filename guard above is defense-in-depth for
manual/backfill invocations, not the primary mechanism.

## Interaction with `.claude/scripts/grammar-audit.py`

`grammar-audit.py` was not part of the original design pass and has an unconsidered interaction
with decision 1 (flat placement) that produces a false-positive audit error once
`vocabulary-verbs.md` exists.

**The bug, precisely:**
- `grammar-audit.py` builds its file set with `grammar_files = {f.stem: f for f in
  sorted(grammar_dir.glob('*.md'))}` — a **non-recursive** glob directly under
  `grammar-index/grammar/`. Today's `vocabulary/**` leaf files live under a nested subdirectory
  and are invisible to this glob — they have never been orphan/mismatch-checked by this script.
  Decision 1 places the new consolidated files **flat** (`grammar-index/grammar/vocabulary-
  verbs.md`), so — unlike every existing vocabulary file — `vocabulary-verbs.md` **will** be
  picked up by this glob and enter the script's checks for the first time.
- The new file format (§"New file format" above) borrows the leaf-file convention `topic_slug:
  ""` (empty string, not `[]`). `grammar-audit.py`'s `parse_topic_slug()` runs `json.loads('""')`
  → `''`, then wraps it as `{str('')}` → the non-empty set `{''}`, not an empty set.
- In `main()`: `declared = parse_topic_slug(content)` → `{''}` (truthy); `actual =
  slug_to_topics[slug]` → `set()` (nothing will ever reference `vocabulary-verbs.md` from a
  topic file's `## Entries`, by design — decision 3). `if declared and declared != actual:` — a
  truthy, non-matching `declared` — appends a **false "topic_slug mismatch"** to every future
  `grammar-audit.py` run, on top of the (correct, but also unwanted) orphan report, once
  `vocabulary-verbs.md` exists.

**Fix — exclude `vocabulary-*.md` from the script's scan**, for consistency with the exclusion
strategy this plan already applies to `structure-grammar.md` / `register-confusability-
grammar.md` / `see-also-grammar.md` (§"Cross-skill exclusion" above), rather than trying to fix
`parse_topic_slug`'s empty-string handling in the script itself. Literal change to
`.claude/scripts/grammar-audit.py` line 62:

```python
# Before:
grammar_files = {f.stem: f for f in sorted(grammar_dir.glob('*.md'))}

# After:
grammar_files = {
    f.stem: f for f in sorted(grammar_dir.glob('*.md'))
    if not f.name.startswith('vocabulary-')
}
```

This keeps the script's existing (already-correct) blind spot toward nested `vocabulary/**` leaf
files and extends the same blind spot to the new flat `vocabulary-<pos>.md` files, rather than
teaching the script to understand the new file kind.

**Self-review addition:** after migration, run `python3 .claude/scripts/grammar-audit.py
--verbose` from the vault root and confirm `vocabulary-verbs.md` does not appear in the output at
all (excluded/clean) — not as a surprise orphan or `topic_slug` mismatch entry.

## Step 9 / Step 10 exclusion (topic classification & post-processing offer)

- **Step 9 (classify into grammar-index topics)** — `vocabulary-<pos>.md` files are excluded,
  exactly like `vocabulary/**` leaf files are today. The existing line in
  `.cowork/skills/lesson-to-web/extract-grammar.md` § "9. Classify into grammar-index topics"
  reads: "Containers never receive `function`. Vocabulary files are excluded (their subdir path
  is their classification)." Do **not** reuse "their subdir path is their classification" for
  the new files — they are flat under `grammar-index/grammar/` per decision 1 and have no subdir,
  so that rationale would be factually wrong for them. Replace the sentence with, verbatim:
  "Containers never receive `function`. Vocabulary files are excluded (their subdir path is
  their classification); `vocabulary-<pos>.md` consolidated files are excluded too — POS-
  consolidated vocabulary files, never individually topic-classified."
- **Step 10 (completion report / preprocess offer)** — the `N` count of "newly created grammar
  point and container files" offered to `preprocess-grammar` must **not** include
  `vocabulary-<pos>.md` files, appended or newly created. Extend the existing carve-out ("`N`
  counts only grammar point and container files; vocabulary files ... are complete at creation
  and never enter the post-processing chain") to explicitly name `vocabulary-<pos>.md` alongside
  `vocabulary/**` leaf files.
- The completion report itself should still show the consolidated-file appends under a `[Vocabulary]` line so the user sees what happened, e.g.:
  ```
  [Vocabulary]
  Appended: grammar-index/grammar/vocabulary-verbs.md ← watasu-to-hand-over, wataru, dekiru-can (new theme: 渡す／渡る transitivity pair; dekiru-can ungrouped)
  ```

## Migration of the 5 existing containers

**Combined entry set** (5 files, 8 vocabulary leaves total):

| Entry | Source lesson | Leaf slug |
|---|---|---|
| 思う — と思います (to think) | UN5GL13 | `vocabulary/Verbs/i-think-toimasu` |
| 言う — と言います (to say) | UN5GL13 | `vocabulary/Verbs/v-dict-toimasu-say` |
| 渡す — to hand over | UN5GL15 | `vocabulary/Verbs/watasu-to-hand-over` |
| 渡る — to cross / go overseas | UN5GL15 | `vocabulary/Verbs/wataru` |
| できる — can | UN5GL15 | `vocabulary/Verbs/dekiru-can` |
| 出来る — can, to be built/completed | UN4GL1 | `vocabulary/Verbs/dekiru-can-to-be-built-completed` |
| 付き合う — to associate with / go out with | UN4GL6 | `vocabulary/Verbs/tsukiau` |
| 知らせる — to inform, let know | UN4GL13 | `vocabulary/Verbs/shiraseru-to-inform-let-know` |

**Proposed clustering** (applying the "don't force it" rule, same reasoning as the append-time
gate above — presented here for the user's confirmation, not decided silently):

- **Theme "と思います／と言います — reporting thoughts and speech"**: 思う + 言う. Matches the user's
  own example from the interview. Genuine shared theme (と-quotation constructions for
  opinion/speech reporting).
- **Theme "渡す／渡る — transitivity pair"**: 渡す + 渡る. Genuine shared theme — a textbook
  transitive/intransitive verb pair, same root.
- **できる (UN5GL15) and 出来る (UN4GL1)** — flagged as a **separate data-quality finding, not
  silently resolved**: these are the same lemma (dekiru, "can") extracted from two different
  lessons into two separate leaf files (`dekiru-can.md` and
  `dekiru-can-to-be-built-completed.md`) with slightly different glosses. Migration will surface
  both as candidates for a theme (e.g. "できる — ability/possibility") but the duplicate-lemma
  question (merge the two leaf files into one, or keep both as separate senses under one theme)
  is called out for explicit user decision during implementation — not assumed either way here.
- **付き合う** and **知らせる** — no natural shared theme with each other or with the above; migrate
  as flat ungrouped bullets.

**Migration steps** (per file, requires explicit user confirmation before any deletion — see
"Never remove files without permission"):
1. Create `grammar-index/grammar/vocabulary-verbs.md` in the new format, populated with the 8
   entries above per the confirmed clustering.
2. Update the 5 lesson-file wikilinks (currently pointing at the old per-lesson container slugs)
   to point at the bare `[[grammar-index/grammar/vocabulary-verbs]]` instead:
   - `JPLessons/Udemy/N4/Grammar/UN4GL1.md:547` → `[[grammar-index/grammar/dekiru-verbs]]`
   - `JPLessons/Udemy/N4/Grammar/UN4GL13.md:618` → `[[grammar-index/grammar/verbs-informing-un4gl13]]`
   - `JPLessons/Udemy/N5/Grammar/UN5GL13.md:334` → `[[grammar-index/grammar/un5gl13-verbs]]`
   - `JPLessons/Udemy/N4/Grammar/UN4GL6.md:414` → `[[grammar-index/grammar/verbs-tsukiau]]`
   - `JPLessons/Udemy/N5/Grammar/UN5GL15.md:301` → `[[grammar-index/grammar/un5gl15-verbs]]`
3. Remove the corresponding entry from each affected topic file (these 3 old containers were
   topic-classified; `un5gl13-verbs.md` and `un5gl15-verbs.md` were not, `topic_slug: []`, so
   nothing to remove for those two):
   - `grammar-index/verb-potential-form.md` — remove the `- [Verbs](.../dekiru-verbs) · N4` entry
     (file keeps its other entry, `kanoukei-potential-form-can`, and its `## See also` — stays
     otherwise intact).
   - `grammar-index/communication-verbs.md` — remove the `- [Verbs](.../verbs-informing-un4gl13) ·
     N4` entry (file keeps its other 4 entries).
   - `grammar-index/relationships.md` — remove the `- [Verbs](.../verbs-tsukiau) · N4` entry. This
     was `relationships.md`'s **only** entry — removal leaves an empty `## Entries` section.
     **Flagged for user decision**: leave the topic file in place with an empty `## Entries`
     (default — no file deletion without permission, and it may attract future non-vocabulary
     `relationships`-topic grammar points), or the user may separately choose to prune it later.
     Not deleted as part of this migration.
4. **Delete the 5 old container files** — `dekiru-verbs.md`, `un5gl13-verbs.md`,
   `un5gl15-verbs.md`, `verbs-tsukiau.md`, `verbs-informing-un4gl13.md`. Per the project's "Never
   remove files without my permission" rule, this step requires explicit user go-ahead at
   implementation time — do not delete as a side effect of an unrelated confirmation.
5. Regenerate `grammar-index/index.md`'s affected sections only if a topic file's presence/absence
   changes materially (none of the 3 topic files above are being deleted, so no `index.md` change
   is expected — confirm during implementation).
6. `kenjougo-verbs.md` is **not** touched by any of the above (see "Finding" section).

## Steps (implementation)

1. Read `.cowork/skills/lesson-to-web/extract-grammar.md`,
   `.cowork/skills/lesson-to-web/structure-grammar.md`,
   `.cowork/skills/lesson-to-web/register-confusability-grammar.md`, and
   `.cowork/skills/lesson-to-web/see-also-grammar.md` in full immediately before editing (confirm
   current line positions).
2. In `extract-grammar.md`:
   - Rewrite the container-routing rule: replace the Step 4b carry-forward `container` bullet and
     insert the new paragraph into Step 7's "Container file format" section, using the literal
     text given in "Routing change → Literal replacement text / Literal insertion text" above
     (not a paraphrase).
   - Add new **Step 7c — Vocabulary POS container (consolidated)**, covering: read-or-create
     target file, per-entry dedup by link-target path, the theming-gate user prompt, theme vs
     ungrouped write logic, and the new file format (frontmatter + `## Sub-topics` shape) — per
     "New file format" and "Append-time theming gate" above. Explicitly state that Step 7c runs
     for every Vocabulary-sourced leaf under a routed container heading regardless of whether
     Step 6 produced Created or Skip for that leaf, and that this is unlike Step 8/Step 9's
     "Created only" gate — per the "Runs regardless of Step 6's Created/Skip outcome" paragraph
     above.
   - Update Step 6 (Idempotency check) to note the consolidated-file path uses Step 7c's per-entry
     check instead of the `pattern:` grep, per "Idempotency check update" above.
   - Update Step 8 (lesson wikilink) to note that for the consolidated-file routing case, the
     inserted link has no anchor and points at the bare `vocabulary-<pos>` file, per "Lesson-file
     wikilink" above.
   - Update Step 9's vocabulary-file exclusion line to also name `vocabulary-<pos>.md` files.
   - Update Step 10's carve-out line (both the `N`-count text and the "yes/no/all" prompt context)
     to also name `vocabulary-<pos>.md` files, and update the completion-report example to show a
     consolidated-file append line.
3. In `structure-grammar.md`, add the `vocabulary-*.md` filename guard to "Container file
   detection", checked before the `## Sub-topics` check, per "Cross-skill exclusion" above.
4. In `register-confusability-grammar.md`, add the same filename guard to "Container / vocabulary
   scope guard", alongside (not replacing) the existing `vocabulary/` subdirectory guard.
5. In `see-also-grammar.md`, exclude `grammar-index/grammar/vocabulary-*.md` from the
   container-scanning candidate pool used when computing other files' backlinks.
6. In `.claude/scripts/grammar-audit.py`, apply the literal line-62 change in "Interaction with
   `.claude/scripts/grammar-audit.py`" above — exclude `vocabulary-*.md` from `grammar_files`.
7. Present the migration clustering proposal (§"Migration of the 5 existing containers") to the
   user for confirmation before touching any file.
8. On confirmation, execute the migration: create `vocabulary-verbs.md`, update the 5 lesson
   wikilinks, remove the 3 stale topic-file entries (flagging the now-empty `relationships.md`
   explicitly rather than deleting it), and — only with explicit separate go-ahead — delete the 5
   old container files.
9. Self-review: grep all four edited skill files for the old "one container per lesson" framing
   to make sure nothing still describes the retired behavior as current; grep the vault for any
   remaining references to the 5 old container slugs after migration (should be zero outside git
   history); run `python3 .claude/scripts/grammar-audit.py --verbose` from the vault root and
   confirm `vocabulary-verbs.md` does not appear in its output (excluded/clean), not as a
   surprise orphan or `topic_slug` mismatch entry.

## Out of scope

- `kenjougo-verbs.md` and any other `# 文法`-sourced container — untouched.
- `vocabulary-nouns.md` / `vocabulary-adjectives.md` creation — deferred to first real use
  (decision 4); no placeholder files created by this plan.
- Merging the `dekiru-can.md` / `dekiru-can-to-be-built-completed.md` duplicate-lemma leaf files —
  flagged during migration, not resolved by this plan.
- Any change to `grammar-index/grammar/vocabulary/**` leaf-file format itself (structure/examples
  templates) — unrelated, unaffected.
- `preprocess-grammar.md` / `review-grammar.md` — no changes needed; they're only ever invoked on
  the Step 10 "Created" list, which already excludes these files by construction once Step 10's
  carve-out is updated.

## Risks

- **Theming judgment drift over many appends.** As `vocabulary-verbs.md` grows across dozens of
  future lessons, the append-time gate (Step 7c) only ever sees the file's *current* state — a
  theme that would make sense in hindsight across 10 lessons might not be visible when only 2 of
  its members exist yet. This is accepted as inherent to append-time (not batch) theming, same
  tradeoff the user's own worked example implies; no batch re-theming pass is proposed here.
- **Lost per-lesson deep-link is a real regression**, not fully mitigated — surfaced explicitly
  above per the interview's requirement, not silently absorbed.
- **Filename-guard scope.** The new `vocabulary-*.md` exclusion in the three post-processing
  skills is filename-pattern-based; if a future *legitimate* grammar container happens to get a
  slug starting with `vocabulary-` (unlikely — container slugs are derived from heading text, and
  no heading naturally produces this prefix), it would be incorrectly excluded. Not considered a
  realistic collision, but worth a implementation-time grep to confirm no existing container slug
  already starts with `vocabulary-`.
- **Never touch:** `<!--ID: -->` lines, `TARGET DECK` lines, and anything below `# Summary` in any
  lesson file — this plan's lesson-file edits are limited to the single wikilink line per affected
  lesson (Step 8/migration), inserted the same way Step 8 already does today.
