# Remove 尊敬語 (honorific) row from #wc verb card template

## Goal
Drop the `尊敬語 (honorific)` form line from the canonical `#wc` verb card template so that
future card generation (`fill-templates`) and future template repair (`templates-update`)
stop producing/expecting it. The distinct `お〜になる (honorific)` row is unaffected and
stays exactly as-is — it is a separate field that happens to also render as "(honorific)"
in its label, but conveys a different derivation (お + stem + になる) and must not be
touched by any edit in this plan.

The canonical `#wc` template shrinks from 15 form lines to 14. Already-filled lesson files
that still contain a `尊敬語 (honorific)` row are explicitly **not** touched by this plan —
see "Existing filled files" below.

## Approach
Edit the template-definition files only: `card-templates.md` (source of truth for the
block structure), `fill-templates.md` (generation skill + its manual-fix reference
example), `verb-conjugation.md` (conjugation rules referenced by both generation and
repair), `templates-update.md` (repair skill's expected-label list), and `fill_extract.py`
(skeleton generator). Additionally, add a new repair step to `templates-update.md`
("Repair 3c") that lazily strips any leftover `尊敬語 (honorific)` line it finds when a
user runs `templates-update` on an already-filled file — no batch sweep, no separate
script, no touching of lesson files by this plan itself.

`label-aliases.json` is left unchanged: its `honorific:` → `尊敬語 (honorific):` and
`尊敬語:` → `尊敬語 (honorific):` entries are repurposed (documented, not renamed) to
support Repair 3c's ability to recognize legacy spelling variants before stripping them.

## Steps

1. **`.cowork/skills/references/card-templates.md`**
   - Remove the line `尊敬語 (honorific): [value]` (currently line 33) from the canonical
     `#wc` template code block (lines 20–40). `お〜になる (honorific): [value]` (line 28)
     stays untouched.
   - Update the note "The 15 form lines appear in the exact order above." → "The 14 form
     lines appear in the exact order above."
   - Add one clarifying line under `## Label alias table`: note that the `honorific:` and
     `尊敬語:` entries in `label-aliases.json` map to the now-deprecated `尊敬語
     (honorific):` label and are retained solely so `templates-update`'s Repair 3c can
     recognize and strip legacy spelling variants — they are not part of the current
     canonical template.

2. **`.cowork/skills/fill-templates.md`**
   - Line 47 (verb-conjugation.md pointer): update "godan table (all endings × all 15
     forms)" → "14 forms".
   - Line 48 (same pointer, next line): remove "尊敬語 and " from "来る fixed forms, 尊敬語
     and お〜になる derivation rules." → "来る fixed forms, お〜になる derivation rule."
   - In the "Card format reference" fully-filled `#wc` example (lines 79–99), remove the
     line `尊敬語 (honorific): ...` (currently line 93). Keep `お〜になる (honorific): ...`
     (line 88) as-is.

3. **`.cowork/skills/references/verb-conjugation.md`**
   - Frontmatter description: "all 15 conjugation forms" → "all 14 conjugation forms".
   - Line 33 (canonical 15-label ordered list): remove `尊敬語 (honorific)` from the list,
     leaving 14 labels, `お〜になる (honorific)` remains in place.
   - Godan notes (around line 48): remove the bullet `尊敬語 (honorific)` = same as `受身形
     (passive)` value`. Leave the adjacent `お〜になる (honorific)` bullet (line 49)
     untouched.
   - Ichidan table (lines 61–77): remove the row `| 尊敬語 (honorific) | = 受身形 |
     食べられる |`. Leave the `お〜になる (honorific)` row untouched.
   - 来る fixed forms block (lines 125–141): remove the line `尊敬語 (honorific): 来られる`.
     Leave `お〜になる (honorific): お出でになる` untouched.
   - Subsection "## 尊敬語 and お〜になる derivation rules" (lines 145–150): remove only the
     尊敬語-specific bullet ("`尊敬語 (honorific)` is always the same value as `受身形
     (passive)`..."). Retitle the subsection to "## お〜になる derivation rule" and keep the
     お〜になる bullet content verbatim (お + ます stem + になる; 渡る example; 来る
     exception お出でになる). No information is lost — this rule is not duplicated in full
     elsewhere, so it keeps its own trimmed subsection rather than being folded in.

4. **`.cowork/skills/templates-update.md`**
   - Line 28 (References section blurb pointing at verb-conjugation.md): update "verb type
     detection and all 15 conjugation form rules" → "...all 14 conjugation form rules".
   - Repair 3 intro (line 131–132): update "Expected 15 form labels" → "Expected 14 form
     labels" and remove `尊敬語 (honorific)` from the list. `お〜になる (honorific)` stays
     in the list.
   - Repair 1 rules (lines 106–109): add a new sub-point exempting the deprecated label from
     the "unrecognized → flag" path, so Repair 3c's cleanup stays silent instead of also
     surfacing as a spurious "flagged for review" entry on every legacy file:
     "If an unrecognized/uncounted label is exactly `尊敬語 (honorific):`, do not flag it —
     defer silently to Repair 3c, which strips it later in the same pass."
   - Repair 3b, step 2 (currently line 150): update "For each of the 15 form labels, compute
     the expected value..." → "For each of the 14 form labels, compute the expected
     value...". This one matters beyond cosmetics: verb-conjugation.md will only define
     derivation rules for 14 forms after step 3 below, so if this line still said 15, Repair
     3b would try to "compute the expected value" for a form with no defined rule on any
     legacy file that still has the old 尊敬語 line — risking a hallucinated value right
     where Repair 3c is supposed to just cleanly strip the line instead.
   - Repair 3b risk note (currently line 161): update "will replace all 15 forms" → "will
     replace all 14 forms".
   - Insert a new subsection **Repair 3c — Strip deprecated 尊敬語 (honorific) row (`#wc`
     non-suru only)** immediately after Repair 3b and before Repair 4:
     - Scan the block for any line beginning with `尊敬語 (honorific):` (already normalized
       to this canonical spelling by Repair 1 / `preprocess-templates.py`, which still maps
       `honorific:` and `尊敬語:` variants to it for exactly this purpose).
     - If found, remove the entire line (label + value) from the block.
     - Record the block in the repair summary as "尊敬語 row stripped".
     - Explicitly do not touch `お〜になる (honorific):` — distinct, still-canonical field.
     - If no such line exists in the block: no-op.
   - Step 4 repair summary output list: add a bullet "Cards with deprecated 尊敬語 row
     stripped (Repair 3c): count".

5. **`.cowork/skills/fill_extract.py`**
   - Remove the line `"尊敬語 (honorific): ",` (currently line 116) from the `#wc` skeleton
     list in the `skeleton()` function. `"お〜になる (honorific): "` (line 111) stays.

6. **`.cowork/skills/references/label-aliases.json`**
   - No edit. Keep `"honorific:": "尊敬語 (honorific):"` (line 23) and `"尊敬語:": "尊敬語
     (honorific):"` (line 48) as-is — they now serve only to let Repair 3c recognize legacy
     spellings before stripping them (documented via the card-templates.md note in step 1).

## Existing filled lesson files (explicit non-scope for this plan)

40 already-filled files (grep-confirmed) still contain a `尊敬語 (honorific)` row, e.g.
`JPLessons/Udemy/N4/Grammar/UN4GL1.md` through `UN4GL12.md`, `JPLessons/Udemy/N5/Grammar/UN5GL5.md`
through `UN5GL15.md`, and several `Caligraphy/UN4KL*`/`UN5KL*`/`UNK5L*` files. **This plan does
not touch any of them.** Per explicit user decision, cleanup is lazy: a file's `尊敬語
(honorific)` row is only stripped the next time someone runs `templates-update` on that
specific file (via new Repair 3c in step 4). No batch sweep script or task is included here.
If a batch sweep is ever wanted, it must be scoped as a separate plan with its own sign-off,
since it would mean skill-implementer editing lesson files directly.

## Risks
- `お〜になる (honorific)` must never be removed by any edit above — it is a separate,
  still-canonical field. Every step that touches a 尊敬語 line has an explicit note
  confirming the adjacent お〜になる line/row/bullet is left untouched; skill-implementer
  should diff each edit against this to avoid accidentally deleting the wrong line.
- Field-count check in templates-update.md Repair 1 (line ~108, "verify the block's total
  field count matches the canonical template count") will now compare against 14, not 15.
  For old files that still have all 15 canonical-named fields (14 canonical + a still
  correctly-named `尊敬語 (honorific)` line), Repair 1's positional-matching step will see a
  count mismatch and fall back to name-only matching. Without a fix, this would surface the
  leftover `尊敬語 (honorific)` line as a spurious "flagged for user review" entry on every
  legacy file, undermining the intended silent/lazy cleanup — step 4 above adds an explicit
  Repair 1 exemption for this exact label so it defers silently to Repair 3c instead.
- `<!--ID:-->` values and positions must not be affected by Repair 3c — it only removes a
  form-label line, never touches the ID line's content, per existing "What never to touch"
  rules in templates-update.md.
- This plan makes no change to any file under `JPLessons/` or `Caligraphy/`. If a future
  session decides to batch-sweep the 40 existing files, that must go through a fresh
  plan/approval cycle, not be inferred from this one.

## Not in scope for this plan
- No new `.claude/commands/` stub — this is an edit to existing skill definitions, not a
  new skill.
- No changes to `.cowork/skills/references/adj-forms.md` or `kanji-links.md` — unaffected.
- No changes to `label-aliases.json` content (see step 6).
