# Grammar Container Drift Fix

## Goal

Fix the class of bug where a grammar point file is correctly classified into a topic file's
`## Entries` (`grammar-index/*.md`) but is missing from the `## Sub-topics` of a container file
(`grammar-index/grammar/<slug>.md`) that shares the same topic — even though they are the same
theme. Example: `grammar-index/grammar/mai-counter-for-flat-thin-objects.md` is listed in
`grammar-index/counters-numbers.md`'s `## Entries`, alongside `grammar-index/grammar/counters.md`
(a container), but is absent from `counters.md`'s `## Sub-topics`. Because
`see-also-grammar.md` builds a point's `## See also` exclusively from container `## Sub-topics`
membership, this drift silently produces a permanent `*(none)*` See Also for the point, even
though it obviously belongs with its topic's container.

## Approach

Two independent, non-communicating grouping mechanisms exist today: topic files (populated by
`extract-grammar.md` Step 7, run on every point) and container files (populated only at
container-creation time from literal nested headings in the same lesson run, never revisited
later). The fix has two parts, confirmed with the user:

1. **Prevention at the source** — `extract-grammar.md` Step 7 gets a new gated sub-step: after a
   newly created point is classified into a topic, check whether that topic also contains a
   container file. If so, and the point isn't yet in that container's `## Sub-topics`, prompt the
   user to add it (same gated "join / skip" pattern already used by Step 6d.3's vocabulary-theme
   placement prompt). This stops new drift from being created.
2. **Detection as a safety net** — `.claude/scripts/grammar-audit.py` gets a new check
   ("container drift") that reports, for every topic file, which of its `## Entries` are absent
   from a co-entry container's `## Sub-topics`. This surfaces the *existing* backlog and any
   future drift class-wide (not just counters-numbers/counters), without auto-fixing anything.

`see-also-grammar.md`'s algorithm is explicitly left unchanged — its "See also = container
`## Sub-topics` membership only" rule is intentional (point-to-point relationships belong in
`## Often confused with`, not `## See also`). Keeping containers in sync at the source is the
correct fix; loosening what `## See also` reads would blur its meaning.

Retroactively fixing the ~11 already-affected files under `counters-numbers`/`counters` (and any
others the new audit check surfaces) is explicitly out of scope for this plan, per user decision.

## Steps

1. **`.claude/scripts/grammar-audit.py`** — add a "container drift" check:
   - Add a helper to extract `## Sub-topics` link targets from a container file's body (mirrors
     the existing `entries_in_topic()` helper, reusing `ENTRY_RE`).
   - Build `container_slugs` (files matching `SUBTOPICS_RE`) and, for each, its set of
     sub-topic slugs.
   - For every topic file, for every container slug that is also one of that topic's `## Entries`,
     check all *other* (non-container) entries in that topic: if an entry's slug is not present in
     the container's Sub-topics set, record `(topic_stem, container_slug, missing_slug)`.
   - **Broken-link guard:** before running the container-membership check on an "other entry",
     skip any entry slug that is not present in the script's existing `grammar_files` set (i.e.
     the slug has no matching file under `grammar-index/grammar/`). These are already caught and
     reported by the existing `broken_links` check (~lines 78-85); including them here would both
     crash trying to read a nonexistent file and double-report the same problem under a second
     heading.
   - Add a new report section "Container drift (topic entry missing from container Sub-topics)"
     alongside the existing Orphans/Broken links/Mismatches/Missing Examples sections, using the
     same `--verbose` formatting convention. Count it toward the existing `errors` total and exit
     code (consistent with the other structural-integrity checks).
   - No auto-fix — read-only reporting only.
   - Update the module docstring's numbered "Checks" list (currently 5 items, ~lines 3-16) to add
     "6. Container drift — topic entries missing from a co-entry container's Sub-topics", so the
     docstring doesn't go stale the moment this ships.

2. **`.cowork/skills/lesson-to-web/extract-grammar.md`** — extend Step 7 ("Classify into
   grammar-index topics") with a new item after the existing bidirectional-`## See also` step:
   - **Timing:** this substep runs once, after items 1–4 of Step 7 have finished writing for the
     *entire* run (all points/containers processed, all topic files patched) — not interleaved
     per-file mid-run. This matters because a container can be newly created earlier in the same
     Step 7 pass; the membership check must see that container as it exists at the end of the run,
     not a stale snapshot from before Step 7 started.
   - For each grammar **point** file (never container files) classified into a topic during this
     run, check whether that topic's `## Entries` also includes a container file (a file with
     `## Sub-topics`).
   - If so, and the point's slug is not already present in that container's `## Sub-topics` list,
     prompt (one prompt per point/container pair, in topic order):
     ```
     <point-name> (<slug>) was classified into topic "<Topic Title>", which also contains
     container "<Container Name>" (<container-slug>).
     Add <point-name> to <Container Name>'s Sub-topics? (yes / no)
     ```
   - **yes** → append `- [<pattern>](/JapaneseNotes/grammar-index/grammar/<slug>) · <level>` to
     the container's `## Sub-topics` list, in the same bullet format as the Step 6c container
     template; dedup by link path first. `<pattern>` and `<level>` are read from the target
     point file's own frontmatter (`pattern:` / `level:` fields) — the same field-source
     convention already used by every other bullet-writing step in this file (e.g. Step 6d's
     `## Sub-topics` bullets).
   - **no** → skip, no file changes.
   - A point may be classified into multiple topics (up to 3) and a topic may contain more than
     one container — prompt once per distinct (point, container) pair found.
   - Update the Step 7 heading's step list / mermaid diagram only if needed for clarity; do not
     renumber Steps 8–11.

3. **`.cowork/skills/lesson-to-web/see-also-grammar.md`** — no change. Explicitly confirmed out
   of scope: its container-only `## See also` algorithm stays as-is.

4. **Backlog note** — one line only, no task: the ~11 files already affected under
   `counters-numbers`/`counters` (and any others the new audit check in Step 1 surfaces) are not
   retroactively fixed by this plan. Left as future work, to be picked up as its own plan if
   wanted, now that the audit check makes the full scope visible.

5. **Container-to-container sync note** — one line only, no task: syncing Sub-topics *between two
   containers* that share the same topic file (i.e. a container-to-container relationship) is
   deliberately out of scope for both halves of this fix. The Step 1 audit check only examines
   non-container topic entries when looking for drift (containers are excluded from the "other
   entries" set it scans); the Step 2 skill substep only ever fires for grammar **point** files,
   never for container files. Container-to-container grouping, if ever needed, is a separate
   concern from this plan.

## Risks

- No risk to `<!--ID:-->`, `TARGET DECK`, or lesson-file content — every file touched lives under
  `grammar-index/`.
- Step 2's new prompt could add a noticeable number of extra gated prompts per extraction run if a
  point lands in a topic with several containers — acceptable since it's gated (user can always
  say no), but worth watching during implementation review.
- Step 1's audit check adds a new error category that increases `grammar-audit.py`'s error count
  and non-zero exit code for the existing backlog immediately upon implementation, even though no
  backlog files are fixed by this plan. This is intentional (visibility), but should be called out
  in the completion report so it isn't mistaken for a regression.
