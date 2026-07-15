# Remove 尊敬語 (honorific) row from #wc verb card template — Tasks

- [x] `card-templates.md`: remove `尊敬語 (honorific): [value]` line from canonical `#wc`
      template code block (leave `お〜になる (honorific): [value]` untouched)
- [x] `card-templates.md`: update "The 15 form lines..." note → "The 14 form lines..."
- [x] `card-templates.md`: add clarifying note under `## Label alias table` about why the
      `honorific:` / `尊敬語:` aliases are retained (support Repair 3c stripping)
- [x] `fill-templates.md`: line 47 — update "godan table (all endings × all 15 forms)" →
      "14 forms"
- [x] `fill-templates.md`: line 48 — remove "尊敬語 and ", rename phrase to "お〜になる
      derivation rule"
- [x] `fill-templates.md`: remove `尊敬語 (honorific): ...` line from the fully-filled
      `#wc` example in "Card format reference" (leave `お〜になる (honorific): ...` line)
- [x] `verb-conjugation.md`: update frontmatter description "15 conjugation forms" → "14"
- [x] `verb-conjugation.md`: remove `尊敬語 (honorific)` from the canonical 15-label
      ordered list (leave `お〜になる (honorific)` in place)
- [x] `verb-conjugation.md`: remove godan note bullet "`尊敬語 (honorific)` = same as
      `受身形 (passive)` value" (leave the お〜になる bullet untouched)
- [x] `verb-conjugation.md`: remove `尊敬語 (honorific)` row from ichidan table (leave
      `お〜になる (honorific)` row untouched)
- [x] `verb-conjugation.md`: remove `尊敬語 (honorific): 来られる` line from 来る fixed
      forms block (leave `お〜になる (honorific): お出でになる` untouched)
- [x] `verb-conjugation.md`: remove 尊敬語 bullet from "## 尊敬語 and お〜になる derivation
      rules" subsection, retitle subsection to "## お〜になる derivation rule", keep the
      お〜になる bullet content verbatim
- [x] `templates-update.md`: line 28 (References blurb) — update "all 15 conjugation form
      rules" → "all 14 conjugation form rules"
- [x] `templates-update.md`: update Repair 3 "Expected 15 form labels" → "14 form labels"
      and remove `尊敬語 (honorific)` from the list (leave `お〜になる (honorific)`)
- [x] `templates-update.md`: Repair 1 rules (lines 106–109) — add sub-point exempting
      `尊敬語 (honorific):` from the "unrecognized → flag" path so it defers silently to
      Repair 3c instead of being flagged for user review
- [x] `templates-update.md`: Repair 3b step 2 (currently line 150) — update "For each of
      the 15 form labels..." → "For each of the 14 form labels..." (prevents Repair 3b from
      trying to compute a value for a form with no defined rule on legacy files)
- [x] `templates-update.md`: Repair 3b risk note (currently line 161) — update "will replace
      all 15 forms" → "will replace all 14 forms"
- [x] `templates-update.md`: insert new "Repair 3c — Strip deprecated 尊敬語 (honorific)
      row (#wc non-suru only)" subsection after Repair 3b and before Repair 4
- [x] `templates-update.md`: add "Cards with deprecated 尊敬語 row stripped (Repair 3c):
      count" bullet to the Step 4 repair summary output list
- [x] `fill_extract.py`: remove `"尊敬語 (honorific): ",` from the `#wc` skeleton list in
      `skeleton()` (leave `"お〜になる (honorific): ",` untouched)
- [x] Verify no other `.cowork/skills/` or `.claude/` file references `尊敬語` after edits
      (re-run `grep -rn "尊敬語" .cowork/skills .claude`) except `label-aliases.json`
      (intentionally unchanged) and the retitled verb-conjugation.md subsection reference
- [x] Verify no stale "15 form"/"15 conjugation" references remain (re-run
      `grep -rn "15 form\|15 conjugation" .cowork/skills`) — should return no matches after
      all four 15→14 edits (card-templates.md, fill-templates.md, verb-conjugation.md,
      templates-update.md ×3) are applied
- [x] Confirm `label-aliases.json` left unchanged (no task — verification only)
- [x] Confirm no files under `JPLessons/` or `Caligraphy/` were touched (verification only
      — this plan does not include a batch sweep of the 40 already-filled files)
