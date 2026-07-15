# Rename お〜になる (honorific) → お〜になる/special verb (honorific) + tiered derivation — Tasks

## お〜になる rename + tiered derivation logic

- [x] `card-templates.md`: rename `お〜になる (honorific): [value]` → `お〜になる/special verb
      (honorific): [value]` in the canonical `#wc` template block (leave `あれる形
      (passive/honorific):  [value]` untouched)
- [x] `fill-templates.md`: rename `お〜になる (honorific): ...` → `お〜になる/special verb
      (honorific): ...` in the "Card format reference" fully-filled `#wc` example (leave
      `あれる形 (passive/honorific): ...` untouched)
- [x] `fill-templates.md`: update verb-conjugation.md pointer line "...お〜になる derivation
      rule." → "...お〜になる/special-verb derivation rules."
- [x] `fill-templates.md`: add explicit first-time-fill fallback rule (Step 4 or wherever this
      field's fill logic lives) — when web search is genuinely inconclusive during initial
      fill (no confirmation gate in that workflow), default to a best-effort tier-2
      お+ます形+になる value with an inline flag/note for the user to double-check, rather
      than silently guessing `-` or silently guessing tier-2
- [x] `fill_extract.py`: rename `"お〜になる (honorific): ",` → `"お〜になる/special verb
      (honorific): ",` in the `#wc` non-suru skeleton list
- [x] `fill_extract.py`: grep for any other `お〜になる (honorific)` occurrence (e.g. suru
      branch) and rename each one found; leave all `あれる形` occurrences untouched
- [x] `verb-conjugation.md`: rename `お〜になる (honorific)` → `お〜になる/special verb
      (honorific)` in the canonical 14-label ordered list (line 33)
- [x] `verb-conjugation.md`: replace the godan notes bullet with a short pointer to the
      rewritten derivation-rule subsection (avoid duplicating tiered logic)
- [x] `verb-conjugation.md`: rename the ichidan table row label AND replace the 食べる/
      お食べになる example with a genuine tier-2-only example (e.g. 見せる → お見せになる)
- [x] `verb-conjugation.md`: rename the label in the 来る fixed-forms block AND change the
      value from `お出でになる` → `いらっしゃる` (alignment with lesson's default pick, not
      an error fix — leave `あれる形 (passive/honorific)` line in that block untouched)
- [x] `verb-conjugation.md`: rewrite "## お〜になる derivation rule" → "## お〜になる/
      special-verb derivation rules" with full tier 1 (special-verb table) / tier 2
      (お+ます形+になる, 2+ morae) / tier 3a (deterministic 1-mora exclusion, no search) /
      tier 3b (search-confirmed ambiguous-usage exclusion) logic, plus explicit notes that
      する/来る always use tier 1 and this field never resolves to the passive-honorific value
- [x] `templates-update.md`: rename `お〜になる (honorific)` → `お〜になる/special verb
      (honorific)` in the Repair 3 expected-label list (line 133)
- [x] `templates-update.md`: update Repair 3c's existing bullet ("Explicitly do not touch
      `お〜になる (honorific):`...") to reference the new label
      `お〜になる/special verb (honorific):`
- [x] `templates-update.md`: add explicit exemption note to Repair 3b Step 2 stating the
      `お〜になる/special verb (honorific)` field is excluded from Repair 3b's generic
      recompute and defers entirely to the new Repair 3e
- [x] `templates-update.md`: insert new "Repair 3e — Verify お〜になる/special-verb field
      correctness" subsection after Repair 3c and before Repair 4 (recompute via tiered logic,
      compare, overwrite if different, flag-don't-overwrite on tier-3b search uncertainty,
      explicit "do not touch あれる形" note). Note: `Plans/w-honorific-form-plan.md`
      separately inserts its own Repair 3d (お/ご honorific row, `#w`/`#wp`) in this same
      after-3c/before-4 span — sequence is 3c → 3d → 3e → 4; these are independent repairs,
      not a numbering conflict
- [x] `templates-update.md`: add two bullets to the Step 4 repair summary output list ("Cards
      with お〜になる/special-verb field corrected (Repair 3e): count" and "Cards flagged for
      manual review due to derivation uncertainty (Repair 3e): count")
- [x] `templates-update.md`: fix stale "34 known variants" reference (frontmatter + body
      ~line 100) to the accurate `label-aliases.json` entry count after this plan's edits are
      applied (count entries at implementation time rather than hardcoding a number) — actual
      count confirmed at 62 entries via `json.load` at implementation time; updated all 3
      occurrences (frontmatter line 6, Step 1.3 body line 51, Repair 1 body line 111)
- [x] `label-aliases.json`: add entry mapping old label `お〜になる (honorific):` → new
      canonical `お〜になる/special verb (honorific):` (verify exact current string before
      adding)
- [x] `label-aliases.json`: repoint existing entry (~line 49) `"お〜になる:": "お〜になる
      (honorific):"` directly to `"お〜になる:": "お〜になる/special verb (honorific):"` to
      avoid a two-hop lookup chain
- [x] Verify no other `.cowork/skills/` or `.claude/` file references the old
      `お〜になる (honorific)` label after edits (re-run
      `grep -rn "お〜になる (honorific)" .cowork/skills .claude` — should return no matches
      except the new alias entry in label-aliases.json, which intentionally keeps the old
      string as a key) — found and fixed 4 stray references in
      `.cowork/skills/references/honorific-forms.md` (lines 16, 172, 174, 178), a file not
      originally in this plan's file list, per coordinator confirmation; grep now clean
- [x] Verify `あれる形 (passive/honorific)` content is unchanged wherever this plan's
      お〜になる-specific edits apply (re-run `grep -rn "あれる形" .cowork/skills` before/after
      and diff — no lines should change except the 4 explicit Step 7 conversions below) —
      confirmed: all pre-existing あれる形 lines untouched; new occurrences are only
      newly-authored text (Repair 3e, derivation-rules rewrite) using the already-correct label

## Also fixing: 受身形 (passive) → あれる形 (passive/honorific) label drift (separate concern)

- [x] `verb-conjugation.md` line 33 (canonical 14-label list): rename `受身形 (passive)` →
      `あれる形 (passive/honorific)` (verify exact current text before editing)
- [x] `verb-conjugation.md` line 35 (godan table header): rename `受身形 (passive)` →
      `あれる形 (passive/honorific)` (verify exact current text before editing) — note: actual
      header row uses abbreviated labels without parentheticals (て形, 可能形, 使役形, etc.),
      so renamed to `あれる形` for consistency with that established column-header style
- [x] `verb-conjugation.md` ichidan table, `受身形 (passive)` row: rename to `あれる形
      (passive/honorific)` (verify exact current text before editing)
- [x] `templates-update.md` line 133 (Repair 3 expected-label list): rename `受身形 (passive)`
      → `あれる形 (passive/honorific)` (verify exact current text before editing)

## Verification

- [x] Confirm no files under `JPLessons/` or `Caligraphy/` were touched (verification only —
      this plan does not include a batch sweep of already-filled files, for either the
      お〜になる rename or the 受身形 label-drift fix) — confirmed via
      `git diff --stat -- JPLessons/ Caligraphy/`: no changes from this session
