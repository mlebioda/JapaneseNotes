# Add 謙譲語 (Humble/Kenjougo) Form to #wc Verb Card Template

## Goal
Add `謙譲語 (humble): [value]` as a new 15th form field on the canonical `#wc` (verb) card
template, positioned directly after `お〜になる/special verb (honorific): [value]` and before
`ない形: [value]` — grouping the two keigo (respect-language) fields together. The field
covers 謙譲語（けんじょうご）— humble forms that lower the speaker's own action to indirectly
show respect toward the listener/referent — resolved via a four-tier derivation logic that
mirrors the existing `お〜になる/special verb (honorific)` field's structure:

1. **Tier 1 — special verb table** (highest priority) — always used if the verb's meaning
   matches an entry in a 13-verb humble-verb table (行く／来る → 参る, する → いたす, 言う →
   申す, 見る → 拝見する, 聞く／尋ねる／訪問する → 伺う, 食べる／飲む → いただく, もらう →
   いただく, あげる → さしあげる, いる → おる, 知っている → 存じておる, 会う → お目にかかる,
   見せる → お目にかける, 借りる → 拝借する).
2. **Tier 2 — お/ご + ます形(stem) + いたす／します** — used only when no special verb applies
   and the ます-stem is 2+ morae. お for wago-origin verbs, ご for kango/verbal-noun verbs
   (reuses the existing wago/kango prefix-choice rule in `honorific-forms.md`, see Step 6
   below for the required scope clarification in that file). **This field's tier-2 value is
   dual-valued** — both the いたす form and the する／します form, slash-separated, e.g.
   `お手伝いいたす／お手伝いします` — a deliberate, explicit deviation from every other
   single-valued form field on this card. Confirmed directly with the user after they asked
   twice to see both auxiliary forms on the card itself, not just documented as an alternate
   in prose (which is how every other field's alternates — e.g. いらっしゃる's おいでになる／
   お越しになる — are handled). Tier-1 special-verb entries stay single-valued; the dual-value
   format applies to tier 2 only, since that's the only tier where the auxiliary itself
   (いたす vs する/します) is the thing varying.
3. **Tier 3a — deterministic `-`** for 1-mora ます-stems where no special verb applies
   (お/ご+stem+いたす is grammatically impossible for a 1-mora stem, same physical constraint
   as tier 3a on the お〜になる field). Verified against real vault verbs: 寝る, 着る, 出る are
   all tagged `#wc` in multiple lessons (UN4GL13, UN5GL5, UN5GL7, UN5GL13, UNK5L8,
   UN4KL5-Shopping, etc.), none map to a tier-1 kenjougo special verb (寝る's sonkeigo special
   verb お休みになる does not carry over — 謙譲語 has no equivalent lexical humble form for
   寝る), and all three have 1-mora ます-stems (寝/着/出) — お寝いたします／お着いたします／
   お出いたします are not natural Japanese, confirming this tier is a real, non-hypothetical
   case, not speculative edge-case coverage.
4. **Tier 3b — search-confirmed `-`** for genuinely ambiguous 2+-mora cases where it's unclear
   whether お/ご+stem+いたす is idiomatically natural for that specific verb.

This field never resolves to `あれる形 (passive/honorific)` or to
`お〜になる/special verb (honorific)` — both are separate, unrelated fields on the same card
and must not be touched by any 謙譲語-specific edit, even though they sit on adjacent lines.

## Source note
Unlike `お〜になる/special verb (honorific)`, whose full three-tier logic came directly from
`JPLessons/Udemy/N4/Grammar/UN4GL13.md`'s 尊敬語 section, that lesson's 謙譲語 section (line
466, `## 謙譲語（けんじょうご）`) only lists 2 special verbs (拝見する, 伺う) plus non-verb
humble vocabulary (わたくし, 弊社, 粗品) — it has no derivation table. The tier-1 special-verb
table and tier-2 auxiliary rule in this plan were derived from standard Japanese grammar
(broader than the lesson's coverage) and confirmed interactively with the user, including two
rounds of worked-example review (手伝う and 行く, both reviewed in full-card form) before this
plan was written. 申し上げる was explicitly considered as a possible separate field/tier and
rejected — it stays documented as a more-formal prose alternate to 申す in the tier-1 table,
the same treatment いらっしゃる's alternates (おいでになる／お越しになる) already receive on
the お〜になる field.

## Approach
Edit the same 6 files touched by the `お〜になる/special verb (honorific)` plan
(`Plans/wc-honorific-special-verb-plan.md`, fully implemented — this plan mirrors its
structure directly): `card-templates.md` (canonical block), `verb-conjugation.md` (derivation
rules — gets the substantial new subsection), `fill_extract.py` (skeleton generator),
`label-aliases.json` (defensive bare-colon alias for the new field), `fill-templates.md`
(generation skill + reference example + first-time-fill fallback rule), and
`templates-update.md` (repair skill — gets a new "Repair 3f" verification step). Additionally,
`honorific-forms.md` needs a narrow scope-clarification edit (Step 6) because its current text
states unconditionally that "`#wc` cards are never eligible for this row" and "this file does
not apply to `#wc` in any way" — true for the `お/ご (honorific):` row itself, but the file's
wago/kango prefix-choice heuristic (a distinct, reusable sub-rule) is now also cross-referenced
by 謙譲語's tier-2 derivation, which does apply to `#wc`. This must be an additive carve-out,
not a rewrite of the file's actual eligibility rules for `#w`/`#wp`.

Existing filled lesson files are updated lazily — only when `templates-update` is next run on
that specific file — no batch sweep, matching the お〜になる plan's precedent.

## Steps

1. **`.cowork/skills/references/card-templates.md`**
   - In the canonical `#wc` template code block (currently lines 20–39), insert a new line
     `謙譲語 (humble): [value]` between `お〜になる/special verb (honorific): [value]`
     (line 28) and `ない形: [value]` (line 29).
   - Update the notes bullet "The 14 form lines appear in the exact order above." (line 42) →
     "The 15 form lines appear in the exact order above."

2. **`.cowork/skills/references/verb-conjugation.md`**
   - Frontmatter description (line 4): "all 14 conjugation forms" → "all 15 conjugation forms".
   - Canonical label list (line 33): insert `謙譲語 (humble)` immediately after
     `お〜になる/special verb (honorific)` in the ordered list.
   - Godan notes bullet list (after line 48's `お〜になる` pointer bullet): add a new bullet
     `- 謙譲語 (humble) — see ## 謙譲語 (humble) derivation rules below.` (same short-pointer
     style as the お〜になる bullet — avoid duplicating the tiered logic in two places).
   - Ichidan table (lines 60–75): insert a new row immediately after the
     `お〜になる/special verb (honorific)` row (line 72):
     `| 謙譲語 (humble) | お/ご + stem + いたす／します (tier 2 only) | お教えいたす／お教えします (教える) |`.
     Use **教える** as the example verb, not 見せる — 見せる already has a tier-1 kenjougo
     special verb (お目にかける), so using it here would document a wrong derivation (same
     mistake the お〜になる plan explicitly avoided when it swapped its own ichidan-table
     example from 食べる to 見せる for the identical reason). 教える has no tier-1 entry, wago
     origin (お prefix), and a 3-mora ます-stem (教え = お・し・え), making it a genuine
     tier-2-only example.
   - 来る fixed forms block (lines 121–138): insert `謙譲語 (humble): 参る` immediately after
     `お〜になる/special verb (honorific): いらっしゃる` (line 134). する's own fixed-forms
     handling — if `する` has an equivalent fixed-forms block elsewhere, or is documented only
     via the tier-1 table — should resolve to `いたす`; verify whether `する` has its own fixed
     forms block in this file (it does not appear to, based on current content) before deciding
     whether any additional edit is needed here.
   - New subsection **`## 謙譲語 (humble) derivation rules`**, inserted immediately after the
     existing `## お〜になる/special-verb derivation rules` subsection (after line 193, i.e. at
     the end of the file). Must document:
     - **Tier 1 — special verb table.** The 13-entry table from the Goal section above
       (行く／来る → 参る; する → いたす; 言う → 申す — default, 申し上げる noted as a valid
       more-formal alternate; 見る → 拝見する; 聞く／尋ねる／訪問する → 伺う; 食べる／飲む →
       いただく; もらう → いただく; あげる → さしあげる; いる → おる; 知っている →
       存じておる（存じ上げる — for people）; 会う → お目にかかる; 見せる → お目にかける;
       借りる → 拝借する). Tier-1 entries are single-valued — no いたす／します dual form,
       since there is nothing to derive; the special verb itself is already fully humble.
     - **Tier 2 — お/ご + ます形(stem) + いたす／します.** Used only when no special verb
       applies and the ます-stem is 2+ morae. Prefix choice (お for wago, ご for kango/verbal
       noun) reuses the wago/kango rule in `honorific-forms.md`'s "Prefix choice" section
       (cross-reference only — see Step 6 for the required scope-note carve-out in that file).
       **Value is dual-valued, slash-separated**: `[stem]いたす／[stem]します` for wago verbs,
       `ご[noun]いたす／ご[noun]します` for kango/suru-compound verbs — note that suru-compound
       (`〜する`) verbs never reach this tier in practice, since they have zero conjugation
       rows entirely (existing, unrelated rule — `#wc` suru verbs skip all form fields). This
       makes the ご-branch of this rule real in principle but rarely-if-ever exercised on an
       actual filled card; document it for correctness, and flag this as a near-dead branch in
       practice (do not remove it — a future verbal-noun edge case could still need it).
       Example: 手伝う → ます stem 手伝い (4 morae) → お手伝いいたす／お手伝いします.
     - **Tier 3a — deterministic exclusion (1-mora stem, no search).** If no special verb
       applies and the ます-stem is exactly 1 mora (e.g. 寝る, 着る, 出る — real `#wc` entries
       in the vault, none tier-1-covered for 謙譲語), お/ご+ます形+いたす is grammatically
       impossible. Computable fact (mora count), resolve directly to `-` without any web
       search.
     - **Tier 3b — search-confirmed exclusion (ambiguous idiomatic usage).** If the ます-stem
       is 2+ morae, no special verb applies, but it's genuinely unclear whether
       お/ご+stem+いたす is idiomatically natural for that verb, web-search e.g. `[verb] 謙譲語
       いたす` before deciding — same escalation pattern as お〜になる's tier 3b and the
       verb-type heuristic. Only write `-` once the search confirms the verb has no idiomatic
       humble form in active use.
     - Explicit note: tier 3a and 3b both produce `-` but are distinguishable — 3a is a
       deterministic mora-count check, 3b requires search-confirmed ambiguous usage.
     - Explicit note: する/来る always use their tier-1 special verb (いたす／参る) — they never
       take tier 2.
     - Explicit note: this field never resolves to `あれる形 (passive/honorific)` or to
       `お〜になる/special verb (honorific)` — both are separate fields, unaffected by this
       rule.

3. **`.cowork/skills/fill_extract.py`**
   - In `skeleton()`'s `#wc` non-suru branch (currently lines 103–120), insert
     `"謙譲語 (humble): ",` immediately after `"お〜になる/special verb (honorific): ",`
     (line 111) and before `"ない形: "` (line 112).
   - Grep the whole file for any other place the `#wc` field list might be duplicated (e.g. a
     separate suru-branch skeleton) and apply the same insertion if found — do not assume only
     one occurrence.

4. **`.cowork/skills/references/label-aliases.json`**
   - Add one defensive alias entry: `"謙譲語:": "謙譲語 (humble):"` — the bare-colon variant,
     matching the existing pattern used for other fields (e.g. `"ば形:": "ば形 (if):"`). This
     is a net-new field, so no legacy-label migration entries are needed (unlike the
     お〜になる rename, which had to handle pre-existing labels on already-filled files).

5. **`.cowork/skills/fill-templates.md`**
   - Step 4's reference-file pointer line (currently line 53: "...そう form rules, 来る fixed
     forms, お〜になる/special-verb derivation rules."): append ", 謙譲語 (humble) derivation
     rules" and update "all 14 forms" (line 52) → "all 15 forms".
   - Add a new fallback-rule paragraph immediately after the existing
     `お〜になる/special verb (honorific) first-time-fill fallback` paragraph (currently lines
     55–61), titled `**謙譲語 (humble) first-time-fill fallback:**`, mirroring its structure:
     apply the tiered logic in `verb-conjugation.md`'s new derivation-rules subsection; if tier
     3b requires a web search and the result is genuinely inconclusive, do not silently write
     `-` and do not silently write an unflagged tier-2 guess — default to a best-effort tier-2
     dual value (いたす／します) with an inline flag, e.g.
     `謙譲語 (humble): お見せいたす／お見せします (unconfirmed — verify)`.
   - Card format reference `#wc` fully-filled example (currently lines 128–147): insert
     `謙譲語 (humble): ...` immediately after `お〜になる/special verb (honorific): ...`
     (line 137).

6. **`.cowork/skills/references/honorific-forms.md`**
   - This file currently states (lines 15–19): "`#wc` (verb) cards are never eligible for this
     row... This file does not apply to `#wc` in any way." That statement is still correct for
     the actual `お/ご (honorific):` row (eligibility, placement, value format all remain
     `#w`/`#wp`-only) — but is no longer fully accurate as a blanket statement, since the
     wago/kango **prefix-choice heuristic** (the "## Prefix choice (お vs ご vs none)" section,
     currently lines 80–86) is now additionally cross-referenced by the `#wc` 謙譲語 (humble)
     field's tier-2 derivation rule in `verb-conjugation.md` (Step 2 above).
   - Add one sentence immediately after the existing paragraph at lines 15–19, e.g.: "Exception:
     the wago/kango prefix-choice heuristic below (see '## Prefix choice (お vs ご vs none)')
     is additionally reused, by cross-reference only, by the `#wc` 謙譲語 (humble) field's
     tier-2 derivation rule in `references/verb-conjugation.md`. That field's own eligibility,
     tiering, and dual-value format logic lives entirely in `verb-conjugation.md`, not here —
     this file's actual `お/ご (honorific):` row remains `#wc`-ineligible as stated above." Do
     not modify the "Prefix choice" section's content itself — only add the cross-reference
     note at the top of the file. **Insertion point:** the new sentence must land **before**
     the `---` separator currently at line 20 — i.e. as part of the same intro paragraph
     block that lines 15–19 belong to, not after the separator. Inserting after line 20 would
     land the sentence awkwardly positioned immediately before the `## Eligibility` heading
     (line 23) rather than as part of the file's scope-statement intro.

7. **`.cowork/skills/templates-update.md`**
   - Frontmatter/body "known variants" count (lines 6 and 111, currently "62"): update to the
     accurate figure after Step 4's `label-aliases.json` addition (62 existing + 1 new = 63 —
     count actual entries at implementation time rather than hardcoding, in case the count has
     drifted further, per the same caution already applied in the お〜になる plan).
   - Step 3's execution-order line (line 101): "Apply repairs 1, 2, 3, 3b, 3c, 3e, 4, 4b, 3d, 5,
     6 in that execution order" → "Apply repairs 1, 2, 3, 3b, 3c, 3e, 3f, 4, 4b, 3d, 5, 6 in
     that execution order". Update the accompanying note (lines 102–105) to also state Repair
     3f has no special-ordering requirement and executes right after Repair 3e, for `#wc`
     non-suru cards only (same phrasing pattern already used for 3e itself).
   - `#wc` routing note (lines 139–142): extend to mention 謙譲語 alongside お〜になる — e.g.
     "...continue through the existing Repair 3c for the legacy `尊敬語 (honorific):` label.
     Non-suru `#wc` cards are additionally routed through Repair 3e (お〜になる) and Repair 3f
     (謙譲語), which verify those fields' values."
   - Repair 3 expected-label list (line 149): insert `謙譲語 (humble)` immediately after
     `お〜になる/special verb (honorific)`; update "Expected 14 form labels" (line 148) →
     "Expected 15 form labels".
   - Repair 3b Step 2 exemption note (line 167, currently exempting only
     `お〜になる/special verb (honorific)`): extend to also exempt `謙譲語 (humble)` — both
     fields defer entirely to their own dedicated verification repairs (3e and the new 3f
     respectively) and must not be computed or overwritten by Repair 3b's generic per-verb-type
     recompute.
   - Insert a new subsection **Repair 3f — Verify 謙譲語 (humble) field correctness (`#wc`
     non-suru only)**, placed immediately after Repair 3e (line 306, the `---` separator before
     Repair 4) and before Repair 4. Steps, mirroring Repair 3e's structure:
     1. Re-read the `ほんやく:` value (furigana stripped) and confirm verb type (same detection
        as Repair 3).
     2. Apply tier 1: check whether the verb's meaning matches an entry in the 謙譲語
        special-verb table. If it matches, the expected value is that special verb.
     3. If no special-verb match and the verb is not する/来る: apply tier 2 if the ます-stem
        is 2+ morae (dual value: お/ご+stem+いたす／します), or tier 3a if the ます-stem is
        exactly 1 mora (`-`, deterministic, no search).
     4. If tier 2 eligibility holds but idiomaticity is genuinely unclear, apply tier 3b:
        web-search before deciding, resolving to `-` only once confirmed.
     5. Compare the recomputed dual value (for tier 2) or single value (tiers 1/3a/3b) against
        the value currently in the file, using three distinct outcomes for tier-2 comparisons:
        - **(a) Full match** — the stored value equals the recomputed value, including the
          case where the two いたす／します halves are simply stored in reversed order (e.g.
          stored `お手伝いします／お手伝いいたす` vs recomputed
          `お手伝いいたす／お手伝いします`). No change, no repair-summary entry.
        - **(b) Partial fill** (tier 2 only) — the stored value contains no `／` separator and
          matches exactly one half of the recomputed dual value (either order). Treat this as
          a user who has intentionally filled in only one half by hand, not a wrong value:
          complete it by appending the missing half in canonical order (いたす half first,
          then `／`, then する／します half) rather than overwriting. Record separately in the
          repair summary from a generic correction — see the new summary bullet below.
        - **(c) Genuine mismatch** — the stored value matches neither the full recomputed
          dual value (in either half-order) nor exactly one half of it. Overwrite and record
          in the repair summary as a correction: old value → new value, same as every other
          field's Repair 3b/3e-style overwrite behavior.
        For tiers 1/3a/3b (single-valued), comparison is the existing simple equality check —
        no partial-fill case applies, since there is no second half to be missing.
     - **Uncertainty rule** (mirrors Repair 3e): if recomputation requires a tier 3b web search
       and the result is still ambiguous after searching, do NOT overwrite — flag the card for
       user review: "Uncertain 謙譲語 (humble) value — not modified." Tier 3a needs no such
       fallback.
     - Explicitly do not touch `あれる形 (passive/honorific)` or
       `お〜になる/special verb (honorific)` — both separate fields, verified elsewhere or
       unaffected.
     - Skip conditions: same as Repair 3e (`#w` cards, `#wp` cards, suru verb cards — skip
       entirely).
   - Step 4 repair-summary output list (currently lines 396–404): add three bullets, following
     the existing お〜になる/Repair-3e pattern:
     - "Cards with 謙譲語 (humble) field corrected (Repair 3f): count"
     - "Cards with 謙譲語 (humble) partial value completed (Repair 3f): count"
     - "Cards flagged for manual review due to 謙譲語 derivation uncertainty (Repair 3f): count"

## Existing filled lesson files (explicit non-scope for this plan)
Lazy update only, per the same precedent as the お〜になる plan: a file only gets its new
`謙譲語 (humble)` row the next time someone runs `templates-update` on that specific file (via
Repair 3 inserting the missing label + Repair 3f computing its value). No batch sweep script or
task is included here. If a batch sweep is ever wanted, it must be scoped as a separate plan
with its own sign-off.

## Risks
- The dual-value (いたす／します) format is a genuine precedent-break — every other field on
  this card, including the structurally similar `お〜になる/special verb (honorific)`, is
  single-valued. Repair 3f's comparison logic (Step 7, sub-step 5) must use the three-outcome
  logic (full match incl. reversed halves / partial fill / genuine mismatch) — not a plain
  string-equality overwrite — otherwise a hand-filled half value would be silently overwritten
  and logged as a generic "correction" instead of being recognized and completed, and reversed
  but otherwise-correct halves would be flagged as spuriously "corrected" on every run.
- Reviewer flagged (pre-implementation review) that a naive full-string-equality Repair 3f
  would give a half-filled dual value and a genuinely wrong value the identical silent-overwrite
  treatment, unlike every other field's repair (3b/3d/3e/4b), which pause-and-flag on ambiguous
  input rather than overwriting outright. The three-outcome fix above addresses this — verify
  during implementation that the "no `／` separator + matches one half" partial-fill detection
  is checked before falling through to the generic mismatch/overwrite branch, not after.
- 見せる must NOT be used as the ichidan-table tier-2 example for 謙譲語 — it has a tier-1
  special verb (お目にかける) for this field, unlike for お〜になる where it correctly is the
  tier-2 example. Using the same example verb for both fields would silently document a wrong
  derivation for one of them. 教える is the correct tier-2-only example for 謙譲語 specifically.
- The ご-branch of the tier-2 auxiliary rule is a near-dead branch in practice (suru-compound
  verbs get zero conjugation rows), but must still be documented correctly — don't let its
  rare real-world applicability lead to cutting it from the write-up.
- `honorific-forms.md`'s Step 6 edit must be strictly additive (one clarifying sentence) — it
  must not weaken or rewrite the file's actual `#w`/`#wp` eligibility rules, and must not make
  the `お/ご (honorific):` row itself eligible for `#wc` (it remains ineligible; only the
  underlying prefix-choice heuristic is cross-referenced).
- `verb-conjugation.md`'s 来る fixed-forms block: verify whether `する` has an equivalent fixed
  forms block elsewhere in the file before assuming only 来る's block needs the new
  `謙譲語 (humble): 参る`-style line — if `する`'s conjugation is documented only via the
  tier-1 table (not a dedicated fixed-forms block), no additional edit is needed there, but
  confirm this rather than assuming it.
- `<!--ID:-->` lines and positions must not be affected by the new field, per existing
  "what never to touch" rules in `templates-update.md`.
- This plan makes no change to any file under `JPLessons/` or `Caligraphy/`. A future batch
  sweep of existing filled files must go through a fresh plan/approval cycle.
- The special-verb table itself is broader than what `UN4GL13.md`'s 謙譲語 section documents
  (see "Source note" above) — if that lesson's content is later revised or expanded, the table
  in `verb-conjugation.md` may need a follow-up plan to reconcile.

## Not in scope for this plan
- No new `.claude/commands/` stub — this is an edit to existing skill definitions, not a new
  skill.
- No changes to `.cowork/skills/references/adj-forms.md` or `kanji-links.md` — unaffected.
- No batch sweep of already-filled lesson files (lazy update only, per user precedent).
- No separate field or tier for 申し上げる — stays as a documented prose alternate to 申す in
  the tier-1 table.
- No change to `honorific-forms.md`'s actual `#w`/`#wp` eligibility, placement, or value-format
  rules — Step 6 is a single additive cross-reference sentence only.
