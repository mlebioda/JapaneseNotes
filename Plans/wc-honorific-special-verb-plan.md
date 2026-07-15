# Rename お〜になる (honorific) → お〜になる/special verb (honorific) + add tiered derivation logic

## Goal
Rename the `お〜になる (honorific)` field in the canonical `#wc` verb card template to
`お〜になる/special verb (honorific)`, and replace its current single-mode derivation rule
(お + ます形 + になる, unconditionally) with the three-tier honorific logic established in
`JPLessons/Udemy/N4/Grammar/UN4GL13.md` (「敬語」→「尊敬語」section):

1. **Special verb** (highest politeness) — always used if the verb's meaning has an entry in
   the lesson's special-verb table (行く／来る／いる → いらっしゃる, 食べる／飲む → 召し上がる,
   寝る／休む → お休みになる, 死ぬ → お亡くなりになる, 言う → おっしゃる, 見る → ご覧になる,
   着る → お召しになる, する → なさる, 知っている → ご存じ(です), くれる → くださる).
2. **お + ます形 + になる** — used only when no special verb applies, the verb is not する/来る
   (which always use tier 1), and the ます-stem is 2+ morae (see tier 3a below for the 1-mora
   exclusion).
3. **`-` (dash/none)** — used when tier 1 and tier 2 both fail to apply. This has two distinct
   paths (kept separate — see the rewritten derivation-rule subsection in Step 4):
   - **3a — deterministic:** ます-stem is exactly 1 mora → お+ます形+になる is grammatically
     impossible, no search needed.
   - **3b — search-confirmed:** ます-stem is 2+ morae but it's genuinely unclear whether
     お+ます形+になる is idiomatically natural for that verb → resolve via web search.

This field never resolves to the られる/passive-honorific form itself — that is the separate
`あれる形 (passive/honorific)` field (already correctly renamed by the user outside this
plan in most places — see the "Also fixing" step below for the handful of locations that
still lag behind that earlier rename). `あれる形 (passive/honorific)` is explicitly out of
scope for this plan's core お〜になる logic and must not be touched by any お〜になる-specific
edit, even though it sits on an adjacent line at every edit site.

## Approach
Edit the same 5 template-definition files touched by the recent 尊敬語-removal plan
(`Plans/wc-remove-sonkeigo-plan.md`, fully implemented): `card-templates.md` (canonical
block), `fill-templates.md` (generation skill + reference example), `fill_extract.py`
(skeleton generator), `verb-conjugation.md` (derivation rules — gets the substantial rewrite),
and `templates-update.md` (repair skill — gets a new "Repair 3e" verification step, plus an
exemption note in Repair 3b). Add entries to `label-aliases.json` so `templates-update`'s
Repair 1 can recognize both the old `お〜になる (honorific):` label and the even-older
`お〜になる:` label on already-filled files and normalize either straight to the new
canonical label (single-hop, no chained lookups) before Repair 3e recomputes the value.
Existing filled lesson files are updated lazily — only when `templates-update` is next run
on that specific file — no batch sweep, matching the sonkeigo plan's precedent.

One correction rides along with the rename: 来る's fixed value moves from お出でになる →
いらっしゃる. This is **not** a fix for a factual error — お出でになる is a valid,
lesson-listed variant (the kanji form of おいでになる) — it is an alignment with the lesson's
explicitly stated *default* pick for the 行く／来る／いる group, which is いらっしゃる.
`verb-conjugation.md`'s ichidan-table example row is also swapped (食べる/お食べになる →
見せる/お見せになる), since 食べる now resolves via the tier-1 special-verb table
(召し上がる), not tier 2 — keeping 食べる as the tier-2 example would document a wrong
derivation.

Additionally, a reviewer pass surfaced that the user's earlier direct rename of `受身形
(passive)` → `あれる形 (passive/honorific)` was applied inconsistently across the vault: it
landed in `card-templates.md`, `fill-templates.md`, `fill_extract.py`, and
`verb-conjugation.md`'s 来る fixed-forms block, but four locations still say the old `受身形
(passive)`. Since this plan's edits already touch three of those four exact lines/files for
the お〜になる rename, the user decided to fix all four in this same plan (see the dedicated
"Also fixing" step below) rather than opening a separate plan — but it is kept textually
separate from the お〜になる logic throughout, since it is a different, unrelated field.

## Steps

1. **`.cowork/skills/references/card-templates.md`**
   - Rename the line `お〜になる (honorific): [value]` (currently line 28, in the canonical
     `#wc` template code block, between `そう (looks): [value]` and `ない形: [value]`) to
     `お〜になる/special verb (honorific): [value]`.
   - Leave `あれる形 (passive/honorific):  [value]` (currently line 31) untouched — this file
     already has the correct label from the user's earlier direct edit.
   - Field count is unchanged (still 14 form lines) — no "N form lines" note needs updating.

2. **`.cowork/skills/fill-templates.md`**
   - In the "Card format reference" fully-filled `#wc` example, rename the
     `お〜になる (honorific): ...` line to `お〜になる/special verb (honorific): ...`. Leave
     the `あれる形 (passive/honorific): ...` line untouched (already correct here).
   - Update the `verb-conjugation.md` pointer line: "...来る fixed forms, お〜になる
     derivation rule." → "...来る fixed forms, お〜になる/special-verb derivation rules."
     (plural, reflecting the new three-tier logic).
   - Add an explicit fallback rule to Step 4 (the initial-fill workflow step, wherever this
     field's fill logic is documented): when web search is genuinely inconclusive during a
     **first-time fill** (as opposed to a `templates-update` repair pass), there is no
     user-confirmation gate in the fill workflow to fall back on. Default to a best-effort
     tier-2 お+ます形+になる value **with an inline note/flag for the user to double-check**,
     rather than silently guessing `-` or silently guessing tier-2 with no flag. This mirrors
     Repair 3e's "flag, don't silently guess" spirit but adapted to a workflow with no
     confirmation step.

3. **`.cowork/skills/fill_extract.py`**
   - In `skeleton()`, rename `"お〜になる (honorific): ",` (currently sitting between
     `"そう (looks): "` and `"ない形: "` in the `#wc` non-suru branch) to
     `"お〜になる/special verb (honorific): ",`.
   - Grep the whole file for any other occurrence of `お〜になる (honorific)` (e.g. a
     suru-verb branch) and rename each one found — do not assume only one occurrence exists.
   - Leave every `あれる形 (passive/honorific)` occurrence untouched (already correct here).

4. **`.cowork/skills/references/verb-conjugation.md`**
   - Line 33 (canonical 14-label ordered list): rename `お〜になる (honorific)` →
     `お〜になる/special verb (honorific)`. This same line also contains the still-unmigrated
     `受身形 (passive)` label — see Step 7 for that separate rename (same line, unrelated
     field, don't conflate the two edits).
   - Line 48 (godan notes bullet): replace the current bullet (`お〜になる (honorific)` = お
     + ます stem + になる) with a short pointer to the rewritten derivation-rule subsection
     (avoid duplicating the full tiered logic in two places) — e.g. "`お〜になる/special verb
     (honorific)` — see ## お〜になる/special-verb derivation rules below."
   - Ichidan table row (currently ~line 69–72; verify exact current line before editing):
     rename label to `お〜になる/special verb (honorific)` AND replace the example. Current
     row: `| お〜になる (honorific) | お + stem + になる | お食べになる |`. Replace with a
     genuine tier-2-only example, e.g. `| お〜になる/special verb (honorific) | お + stem +
     になる (tier 2 only) | お見せになる (見せる) |` — do not keep 食べる as the example,
     since 食べる now resolves via tier 1 (召し上がる), not tier 2. This table also has a
     separate `受身形 (passive)` row — see Step 7 for that unrelated rename.
   - Lines 121–138 (来る fixed forms block): rename the label to `お〜になる/special verb
     (honorific)` AND change the value from `お出でになる` → `いらっしゃる` — this aligns
     with the lesson's stated default pick for 行く／来る／いる (お出でになる remains a valid
     lesson-listed variant, just not the default; する/来る always use their tier-1 special
     verb, never tier 2). Leave the adjacent `あれる形 (passive/honorific)` line in that block
     untouched — already correct here.
   - Lines 142–146 (currently "## お〜になる derivation rule" subsection): full rewrite.
     Retitle to "## お〜になる/special-verb derivation rules". New content must document:
     - **Tier 1 — special verb table.** Reproduce the lesson's table (行く／来る／いる →
       いらっしゃる — default; note おいでになる／お越しになる as more formal alternates but
       いらっしゃる is the default pick; 食べる／飲む → 召し上がる; 寝る／休む → お休みになる；
       死ぬ → お亡くなりになる; 言う → おっしゃる; 見る → ご覧になる; 着る → お召しになる;
       する → なさる; 知っている（ている形）→ ご存じ(です); くれる → くださる). If the verb's
       meaning matches a table entry, always use the special verb — this tier wins regardless
       of tier 2 eligibility.
     - **Tier 2 — お + ます形(stem) + になる.** Used only when (a) no special verb applies,
       (b) the verb is not する/来る (those always use tier 1), and (c) the ます-stem is 2+
       morae. Example: 見せる → ます stem 見せ → お見せになる.
     - **Tier 3a — deterministic exclusion (1-mora stem, no search).** If no special verb
       applies and the ます-stem is exactly 1 mora (e.g. 見る, 着る — both already covered by
       the tier-1 table in practice, so this rarely surfaces as its own case), お+ます形+になる
       is grammatically impossible. This is a computable fact (mora count), not a judgment
       call — resolve directly to `-` without any web search.
     - **Tier 3b — search-confirmed exclusion (ambiguous idiomatic usage).** If the ます-stem
       is 2+ morae, no special verb applies, but it's genuinely unclear whether
       お+ます形+になる is idiomatically natural for that specific verb, web-search e.g.
       `[verb] 尊敬語 おになる` before deciding — mirroring the existing web-search escalation
       pattern already used for verb-type detection (this file's verb-type heuristic section)
       and in `templates-update.md`. Only write `-` once the search confirms the verb
       customarily relies solely on the plain られる/passive-honorific form (the separate
       `あれる形 (passive/honorific)` field) with no idiomatic お+ます形+になる or special-verb
       form in active use.
     - Explicit note: tier 3a and 3b both produce `-` but are distinguishable and must not be
       conflated — 3a is a deterministic mora-count check requiring no search; 3b requires
       search-confirmed ambiguous usage.
     - Explicit note: する/来る never take tier 2 — always resolve to なさる／いらっしゃる.
     - Explicit note: this field never resolves to the られる/passive-honorific value — that
       is the separate `あれる形 (passive/honorific)` field, unaffected by this rule.

5. **`.cowork/skills/templates-update.md`**
   - Line 28 (References blurb): no count change needed (still 14 conjugation forms); no
     edit required unless the blurb names the field directly, in which case rename it there
     too.
   - Line 133 (Repair 3 expected-label list): rename `お〜になる (honorific)` →
     `お〜になる/special verb (honorific)`. This same list also contains the still-unmigrated
     `受身形 (passive)` label — see Step 7 for that separate rename (verify exact current
     label text before editing, matching the caveat already noted for `verb-conjugation.md`
     line 33).
   - Repair 3c section (currently ~line 178, existing bullet "4. Explicitly do not touch
     `お〜になる (honorific):` — a distinct, still-canonical field."): update the referenced
     label string to `お〜になる/special verb (honorific):`, so Repair 3c doesn't reference a
     now-renamed string. This is exactly the kind of leftover the plan's own verification
     grep (see Tasks file) would otherwise flag.
   - Repair 3b, Step 2 (currently ~line 150, "For each of the 14 form labels, compute the
     expected value using the verb type rules in verb-conjugation.md"): add an explicit
     exemption note stating the `お〜になる/special verb (honorific)` field is excluded from
     Repair 3b's generic per-verb-type recompute and defers entirely to the new Repair 3e.
     Without this, Repair 3b could naively overwrite a correctly tier-1-resolved value (e.g.
     食べる→召し上がる) with a flat tier-2 guess, which Repair 3e would then have to
     re-correct in the same pass — harmless net result, but wasted work and a misleading
     intermediate repair-summary entry.
   - Insert a new subsection **Repair 3e — Verify お〜になる/special-verb field correctness**
     after Repair 3c and before Repair 4. Note: `Plans/w-honorific-form-plan.md` separately
     inserts its own **Repair 3d** (お/ご honorific row, `#w`/`#wp`) in this same after-3c/
     before-4 span — the two are independent, sequential repairs (3c → 3d → 3e → 4), not
     competing for the same slot:
     - For each `#wc` non-suru card, recompute the expected value for this field using the
       tiered logic in `verb-conjugation.md` (special-verb table → お+ます形+になる → tier 3a
       deterministic `-` → tier 3b search-confirmed `-`).
     - Compare the recomputed value to the filled value; if different, overwrite and record
       the card in the repair summary.
     - **Uncertainty rule** (mirrors Repair 3b/4b): if recomputation requires a tier 3b web
       search and the result is still ambiguous/unresolved after searching, do NOT overwrite —
       flag the card for user review instead, using the same wording pattern already
       established for Repair 3b/4b's low-confidence handling. (Tier 3a needs no such
       fallback — it's deterministic.)
     - Explicitly do not touch `あれる形 (passive/honorific)` — separate field, verified
       elsewhere (if a separate repair step exists for it) or left as-is.
   - Step 4 repair summary output list (currently lines ~257–267): add two bullets, following
     the existing pattern (e.g. "Cards with deprecated 尊敬語 row stripped (Repair 3c):
     count"):
     - "Cards with お〜になる/special-verb field corrected (Repair 3e): count"
     - "Cards flagged for manual review due to derivation uncertainty (Repair 3e): count"
   - Frontmatter description and body (~line 100) reference `label-aliases.json` as having
     "34 known variants" — this is stale pre-existing drift (actual count is 58 entries as of
     this reviewer pass, unrelated to this plan's changes, but a natural point to fix since
     this file is already being edited). Update the count to the accurate figure **after**
     Step 6's `label-aliases.json` edits are applied (58 existing + 1 new entry from Step 6 =
     59 — skill-implementer should count actual entries at implementation time rather than
     hardcode a number, in case the count has drifted further).

6. **`.cowork/skills/references/label-aliases.json`**
   - Add a new entry mapping the old label to the new canonical one:
     `"お〜になる (honorific):": "お〜になる/special verb (honorific):"`, so Repair 1 can
     recognize and rename legacy-labeled rows on already-filled files before Repair 3e
     recomputes their value. This mirrors the precedent set by the 尊敬語 plan, which added
     alias entries for exactly this kind of legacy-label recognition.
   - Repoint the existing entry (currently ~line 49) `"お〜になる:": "お〜になる
     (honorific):"` directly to the new canonical label:
     `"お〜になる:": "お〜になる/special verb (honorific):"`. Reason: `preprocess-templates.py`
     does a single non-chained lookup per line — left unchanged, this entry would normalize
     the oldest legacy label to the now-also-deprecated intermediate label and stop there in
     one pass, potentially never reaching the new canonical label without relying on Repair
     1's positional-matching fallback (which the plan doesn't currently invoke or mention for
     this purpose).

7. **Also fixing (separate issue from this plan's お〜になる rename): `受身形 (passive)` →
   `あれる形 (passive/honorific)` label drift.** The user's earlier direct rename of this
   field didn't reach every location. Since Steps 4 and 5 above already touch three of the
   four remaining locations for the お〜になる rename, fix all four here, in the same plan,
   as a clearly separate concern:
   - `verb-conjugation.md` line 33 (canonical 14-label list, same line touched in Step 4)
   - `verb-conjugation.md` line 35 (godan table header — **new** edit, not otherwise touched
     by this plan)
   - `verb-conjugation.md`'s ichidan table, the `受身形 (passive)` row (same table touched in
     Step 4, different row)
   - `templates-update.md` line 133 (Repair 3 expected-label list, same line touched in
     Step 5)
   - At every location: verify the exact current label text before editing — do not assume it
     matches the card-template field name verbatim if it differs (same caveat already applied
     to the お〜になる edits in Steps 4–5).

## Existing filled lesson files (explicit non-scope for this plan)
Lazy update only, per user decision: a file's `お〜になる (honorific)` row (old label, and
possibly the old お出でになる value for 来る) is only renamed and recomputed the next time
someone runs `templates-update` on that specific file (via Repair 1's alias lookup + new
Repair 3e). No batch sweep script or task is included here. If a batch sweep is ever wanted,
it must be scoped as a separate plan with its own sign-off, since it would mean
skill-implementer editing lesson files directly. (This also applies to the `受身形 (passive)`
→ `あれる形 (passive/honorific)` label drift on already-filled files — Step 7 only fixes the
skill-definition files, not lesson files.)

## Risks
- `あれる形 (passive/honorific)` must never be touched by any お〜になる-specific edit above —
  it sits on an adjacent line/row at every single お〜になる edit site (card-templates.md's
  template block, fill-templates.md's example, fill_extract.py's skeleton,
  verb-conjugation.md's 来る fixed-forms block and ichidan table, templates-update.md's
  Repair 3e). Step 7 is the only step permitted to touch `受身形 (passive)`/`あれる形
  (passive/honorific)` text, and only at the four named locations. Every other step has an
  explicit "leave it untouched" callout; skill-implementer should diff each edit against this.
- 来る's fixed value changes from お出でになる → いらっしゃる — a real output change for 来る
  cards (aligning with the lesson's stated default, not fixing an error), so it must not be
  silently dropped or mistaken for a typo revert during implementation.
- The ichidan-table example swap (食べる/お食べになる → 見せる/お見せになる) changes
  documentation content, not just a label — verify the new example verb genuinely has no
  special-verb table entry before using it, to avoid re-creating the same inconsistency with
  a different verb.
- Repair 3b must explicitly defer this field to Repair 3e (Step 5) — without that exemption
  note, Repair 3b's generic recompute could overwrite a correct tier-1 value before Repair 3e
  gets a chance to verify it, producing a confusing (though ultimately self-correcting)
  repair-summary trail.
- Repair 3e's tier 3b web-search escalation has no hard success/failure contract defined
  elsewhere except by analogy to Repair 3b/4b and the existing verb-type-detection heuristic —
  skill-implementer should reuse the exact "flag, don't overwrite" wording already present in
  Repair 3b/4b to keep behavior consistent across repairs. Tier 3a (1-mora, deterministic)
  needs no such fallback.
- `fill-templates.md`'s first-time-fill path has no confirmation gate, unlike Repair 3e — the
  new fallback rule in Step 2 (best-effort tier-2 value + flag, on inconclusive search) must
  not be confused with Repair 3e's "don't overwrite, flag" behavior; they are different
  defaults for different workflows and should stay documented separately.
- `label-aliases.json`'s two edits (new entry + repointed entry) must map exactly the current
  literal label text (spacing, colon placement) — verify exact current strings before editing,
  since Repair 1's alias lookup is presumably exact-match, and confirm the repointed entry no
  longer produces a two-hop chain.
- The "34 known variants" count fix in `templates-update.md` is pre-existing drift unrelated
  to this plan's core change — do not let it distract from or get conflated with the
  お〜になる/受身形 edits; it is a one-line factual correction, not new logic.
- `<!--ID:-->` lines and positions must not be affected by any renamed/recomputed field, per
  existing "what never to touch" rules in `templates-update.md`.
- This plan makes no change to any file under `JPLessons/` or `Caligraphy/`. If a future
  session decides to batch-sweep existing filled files (for either the お〜になる rename or
  the 受身形 label drift), that must go through a fresh plan/approval cycle, not be inferred
  from this one.
- The special-verb table itself is fixed content sourced from `UN4GL13.md`; if that lesson's
  content is later revised, the table in `verb-conjugation.md` would need a follow-up
  plan — not in scope here.

## Not in scope for this plan
- No new `.claude/commands/` stub — this is an edit to existing skill definitions, not a new
  skill.
- No changes to `.cowork/skills/references/adj-forms.md` or `kanji-links.md` — unaffected.
- No batch sweep of already-filled lesson files, for either the お〜になる rename or the
  受身形 → あれる形 label-drift fix (lazy update only, per user decision).
- No change to the *content* or *meaning* of `あれる形 (passive/honorific)` anywhere — Step 7
  only fixes lagging label text at 4 specific locations to match the user's earlier direct
  edit; it does not alter what the field means or how it's derived.
