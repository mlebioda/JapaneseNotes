# Add 謙譲語 (Humble/Kenjougo) Form to #wc Verb Card Template — Tasks

## 謙譲語 field addition + four-tier derivation logic

- [x] `card-templates.md`: insert `謙譲語 (humble): [value]` between
      `お〜になる/special verb (honorific): [value]` and `ない形: [value]` in the canonical
      `#wc` template block
- [x] `card-templates.md`: update "The 14 form lines appear in the exact order above." →
      "The 15 form lines appear in the exact order above."
- [x] `verb-conjugation.md`: update frontmatter description "all 14 conjugation forms" →
      "all 15 conjugation forms"
- [x] `verb-conjugation.md`: insert `謙譲語 (humble)` into the canonical label list immediately
      after `お〜になる/special verb (honorific)`
- [x] `verb-conjugation.md`: add godan notes bullet pointing to the new
      "## 謙譲語 (humble) derivation rules" subsection (short pointer, no duplicated logic)
- [x] `verb-conjugation.md`: insert new ichidan table row immediately after the
      `お〜になる/special verb (honorific)` row, using 教える as the example (NOT 見せる —
      見せる has a tier-1 kenjougo special verb, お目にかける): `謙譲語 (humble) | お/ご +
      stem + いたす／します (tier 2 only) | お教えいたす／お教えします (教える)`
- [x] `verb-conjugation.md`: insert `謙譲語 (humble): 参る` into the 来る fixed-forms block,
      immediately after `お〜になる/special verb (honorific): いらっしゃる` — first verify
      whether `する` has its own separate fixed-forms block anywhere in the file requiring the
      same treatment (currently appears not to; confirm before skipping)
- [x] `verb-conjugation.md`: write new "## 謙譲語 (humble) derivation rules" subsection after
      the existing "## お〜になる/special-verb derivation rules" subsection, covering:
      tier 1 (13-entry special-verb table: 行く／来る→参る, する→いたす, 言う→申す [申し上げる
      noted as more-formal alternate], 見る→拝見する, 聞く／尋ねる／訪問する→伺う, 食べる／
      飲む→いただく, もらう→いただく, あげる→さしあげる, いる→おる, 知っている→存じておる
      [存じ上げる for people], 会う→お目にかかる, 見せる→お目にかける, 借りる→拝借する,
      single-valued); tier 2 (お/ご+ます形stem+いたす／します, dual-valued slash-separated,
      wago→お／kango→ご per honorific-forms.md cross-reference, suru-compound verbs never
      reach this tier in practice since they have zero conjugation rows — document as a
      near-dead-but-correct branch); tier 3a (deterministic `-` for 1-mora stems, verified
      real cases: 寝る/着る/出る); tier 3b (search-confirmed `-` for ambiguous 2+-mora cases);
      explicit notes that する/来る always use tier 1, and this field never resolves to
      あれる形 or to お〜になる/special verb (honorific)
- [x] `fill_extract.py`: insert `"謙譲語 (humble): ",` in the `#wc` non-suru skeleton list,
      immediately after `"お〜になる/special verb (honorific): ",` and before `"ない形: "`
- [x] `fill_extract.py`: grep for any other duplicated `#wc` field-list occurrence and apply
      the same insertion if found
- [x] `label-aliases.json`: add defensive bare-colon alias entry `"謙譲語:": "謙譲語
      (humble):"` (net-new field, no legacy-label migration needed)
- [x] `fill-templates.md`: append ", 謙譲語 (humble) derivation rules" to the Step 4 reference
      pointer line; update "all 14 forms" → "all 15 forms"
- [x] `fill-templates.md`: add "謙譲語 (humble) first-time-fill fallback" paragraph after the
      existing お〜になる fallback paragraph — tiered logic, best-effort tier-2 dual value +
      inline "(unconfirmed — verify)" flag when tier 3b search is inconclusive
- [x] `fill-templates.md`: insert `謙譲語 (humble): ...` line into the "Card format reference"
      fully-filled `#wc` example, immediately after `お〜になる/special verb (honorific): ...`
- [x] `honorific-forms.md`: add one additive cross-reference sentence after the existing
      "`#wc` cards are never eligible for this row... does not apply to `#wc` in any way"
      paragraph, clarifying that the wago/kango prefix-choice heuristic (not the row itself)
      is cross-referenced by the new `#wc` 謙譲語 tier-2 derivation rule in
      `verb-conjugation.md` — do not alter any `#w`/`#wp` eligibility rule content. Insertion
      point: must land BEFORE the `---` separator at line 20 (same intro-paragraph block),
      not after it — inserting after would land the sentence oddly right before
      `## Eligibility`
- [x] `templates-update.md`: update "known variants" count (frontmatter line + body line) from
      62 to the accurate post-edit count (count actual `label-aliases.json` entries at
      implementation time — expected 63, but verify rather than hardcode)
- [x] `templates-update.md`: update Step 3 execution-order line "1, 2, 3, 3b, 3c, 3e, 4, 4b, 3d,
      5, 6" → "1, 2, 3, 3b, 3c, 3e, 3f, 4, 4b, 3d, 5, 6"; extend the accompanying note to state
      Repair 3f has no special-ordering requirement and runs right after Repair 3e
- [x] `templates-update.md`: extend the `#wc` routing note (currently mentioning only
      Repair 3e) to also mention Repair 3f
- [x] `templates-update.md`: insert `謙譲語 (humble)` into the Repair 3 expected-label list,
      immediately after `お〜になる/special verb (honorific)`; update "Expected 14 form
      labels" → "Expected 15 form labels"
- [x] `templates-update.md`: extend Repair 3b Step 2's exemption note to also exempt
      `謙譲語 (humble)` (defers entirely to new Repair 3f, not computed/overwritten by 3b)
- [x] `templates-update.md`: insert new "Repair 3f — Verify 謙譲語 (humble) field correctness
      (`#wc` non-suru only)" subsection immediately after Repair 3e and before Repair 4 —
      recompute via tiered logic, then compare using three distinct outcomes (NOT plain
      string-equality overwrite): (a) full match — including tier-2 halves stored in reversed
      order — no-op; (b) partial fill (tier 2 only) — stored value has no `／` separator and
      matches exactly one half of the recomputed value → complete it by appending the missing
      half (いたす half first) rather than overwriting, logged separately from a generic
      correction; (c) genuine mismatch — overwrite and log as correction (old → new). Also:
      flag-don't-overwrite on tier-3b uncertainty ("Uncertain 謙譲語 (humble) value — not
      modified"), explicit "do not touch あれる形 / お〜になる" note, same skip conditions as
      Repair 3e. Verify the partial-fill check (b) runs before the generic mismatch check (c),
      not after.
- [x] `templates-update.md`: add three bullets to the Step 4 repair-summary output list ("Cards
      with 謙譲語 (humble) field corrected (Repair 3f): count", "Cards with 謙譲語 (humble)
      partial value completed (Repair 3f): count", and "Cards flagged for manual review due to
      謙譲語 derivation uncertainty (Repair 3f): count")
- [x] Verify no `.cowork/skills/` or `.claude/` file references a stray/incomplete 謙譲語 label
      after edits (grep for `謙譲語` across those directories, confirm every occurrence uses
      the canonical `謙譲語 (humble):` label or is the intentional bare-colon alias key)
- [x] Verify `あれる形 (passive/honorific)` and `お〜になる/special verb (honorific)` content
      is unchanged everywhere this plan's edits apply (grep both before/after and diff — no
      lines should change except the new adjacent 謙譲語 lines being inserted next to them)

## Verification

- [x] Confirm no files under `JPLessons/` or `Caligraphy/` were touched (this plan does not
      include a batch sweep of already-filled files) — `git diff --stat -- JPLessons/
      Caligraphy/` should show no changes from this session
