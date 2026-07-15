# #w / #wp honorific (お/ご) row

## Goal
Add an optional お/ご honorific-prefix row to both `#w` (noun/expression/sentence) and `#wp`
(adjective) Anki card templates, showing the honorific form of a word (e.g. 電話 → お電話,
忙しい → お忙しい) when one naturally exists. The row must appear only for genuinely eligible
single-word entries — not phrases/sentences for `#w`, not non-adjective/misclassified `#wp`
entries — and only when お/ご + the word is a natural, actually-used Japanese honorific form.
`#wc` (verb) cards are excluded entirely — verbs already have their own distinct
`お〜になる (honorific)` mechanism, governed by a separate plan. Both `fill-templates`
(new cards) and `templates-update` (existing cards) must apply this consistently across both
eligible card types.

## Approach
Introduce a new canonical row `お/ご (honorific): [word with furigana]` into both the `#w`
and `#wp` templates. Because correctness is a linguistic judgment call (wago vs kango, common
exceptions, loanwords/lexicalized お-words with no separable honorific prefix) rather than a
mechanical conjugation table, the rule of thumb, known exceptions, and card-type-specific
eligibility notes are documented in a new reference file
`.cowork/skills/references/honorific-forms.md` — following the existing pattern of
`verb-conjugation.md` / `adj-forms.md` — that both skills defer to. Eligibility, the
already-prefixed exclusion, and the omit-if-uncertain rule are shared concepts across both
card types, but their concrete criteria differ: `#w` eligibility hinges on "bare noun, no
particle"; `#wp` eligibility hinges on "single adjective in plain dictionary form, not a
non-adjective/all-dash entry." Placement also differs structurally: `#w` has nothing between
the Japanese line and kanji links, so the row goes directly after the Japanese line; `#wp` has
4 existing form lines ending in そう (looks), so the row is appended as the new final form row.

When Claude is not confident a natural form exists, the row is simply omitted (fill-templates)
or left untouched/flagged (templates-update) — there is no placeholder value (e.g. no `—`).
This is carried over unchanged from the original `#w`-only design: forcing a placeholder onto
every eligible word risks normalizing incorrect or invented お/ご forms.

`templates-update` treats this as a single shared, proactive, retroactive repair (Repair 3d)
covering both `#w` and `#wp` cards in one pass — eligibility/value logic is identical in shape
across both types (just different concrete criteria per type), and placement is the only
card-type-conditional branch. This mirrors how Repair 5 (kanji links) already handles both
`#w`/`#wp`/`#wc` with type-conditional placement inside a single repair, rather than
duplicating near-identical repair logic per card type.

## Design decisions (confirmed)

### Eligibility
- **`#w`:** unchanged from the original design — eligible only if the Japanese field
  (furigana stripped) is a bare noun: no particles (は/が/を/に/で/と/の/へ/も, etc.) and not
  a conjugated verb/adjective ending. Judgment call, not a rigid word-count/character check.
  Suru-noun entries (e.g. `入院(にゅういん)(する)`) still count as bare nouns.
- **`#wp`:** eligible only if the entry is a genuine single adjective in plain dictionary
  form — い-adjective or な-adjective, per the type determination already used by
  `adj-forms.md`. `#wp` entries classified as non-adjective/other (the "all fields dash" case
  in `adj-forms.md`) are never eligible — there is nothing to honorific-prefix. Because `#wp`
  cards are, by the vault's tagging convention, already single words (not phrases/sentences),
  there is no separate "no particles" check needed the way there is for `#w` — the
  type-determination step itself is the eligibility gate.
- **`#wc` is never eligible for this row.** Verbs have their own distinct
  `お〜になる (honorific)` field (a different mechanism: verb-stem + になる derivation, not a
  noun/adjective prefix). This plan does not touch that field, its logic, or the separate
  `Plans/wc-honorific-special-verb-plan.md` that governs it.

### Already-prefixed exclusion
- **`#w`:** if the base word (furigana stripped) already begins with お or ご — e.g. お願い,
  お金, お弁当, お邪魔, all real vault entries that would otherwise pass the "bare noun, no
  particle" test — it is ineligible for a second prefix. Stacking a prefix (おお願い) is
  invalid Japanese.
- **`#wp`:** the same "starts with お/ご → exclude" outcome applies, but for a **different
  underlying reason**, and the reference file must document this distinction explicitly (not
  just silently reuse the `#w` heuristic): many い-adjectives have お lexicalized into the
  word root itself — おいしい, おかしい, おしゃれ, おもい — where お is not a separable,
  stackable honorific prefix at all, it's simply part of the word. The exclusion check is the
  same mechanical test (does the furigana-stripped base begin with お/ご) but the reference
  file must note that for `#wp` this is catching "lexically fused お," not "already
  honorific-prefixed," so a future implementer doesn't assume the `#w` rationale carries over
  unchanged.

### Prefix choice (お vs ご vs none)
- Same wago/kango rule-of-thumb approach for both types: native Japanese-origin (wago) words
  tend toward お, Sino-Japanese (kango) words tend toward ご, with well-known exceptions and
  loanwords generally taking no prefix at all. The reference file's exception list needs
  **adjective-specific entries** in addition to the existing noun ones (e.g. お忙しい, お若い,
  ご立派, お元気, ご親切) — these are curated into `honorific-forms.md` at implementation
  time, not exhaustively enumerated in this plan.
- If Claude is not confident, treat as "no natural form" (omit) — same rule for both types.

### `(する)`-dropping rule — `#w`-only, confirmed N/A for `#wp`
- The rule that suru-noun `#w` values drop `(する)` in the honorific row (e.g.
  `担当(たんとう)(する)` → `ご担当(たんとう)`, not `ご担当(たんとう)(する)`) is unchanged
  from the original design and remains `#w`-only.
- Explicitly checked and confirmed **not applicable** to `#wp`: `adj-forms.md` and the
  canonical `#wp` template (`card-templates.md`) confirm `#wp` values never carry a `(する)`
  suffix — that formatting only exists for `#w` suru-noun entries. This is recorded as a
  verified fact in the reference file, not a silent omission.

### Label and value format
- Same label for both types: `お/ご (honorific):` — one canonical label, not two.
- Value: the honorific word with inline furigana, e.g. `お/ご (honorific): お電話(でんわ)`
  (`#w`) or `お/ご (honorific): お忙(いそが)しい` (`#wp`). No extra annotation of which
  prefix was used — it's visible in the value itself.

### Placement
- **`#w`:** immediately after the Japanese field line, before the kanji-trainer `<a href>`
  links, before `<!--ID:-->` — unchanged from the original design (there is nothing else
  between the Japanese line and kanji links in the `#w` template).
- **`#wp`:** inserted as the **new final form row** — immediately after そう (looks), which
  is already the last of `#wp`'s 4 existing form lines (過去形, 否定形, 副詞形, そう
  (looks)) — before kanji links, before `<!--ID:-->`. This is structurally different from
  `#wc`'s お〜になる placement (which sits mid-list, between そう (looks) and ない形, because
  `#wc` has 9 more form lines after そう) even though both could loosely be described as
  "after そう" — for `#wp` it is simply an append to the end of the form list, not a
  mid-list insert. This distinction is stated explicitly so it isn't read as reusing `#wc`'s
  positioning rule.

### No natural form exists
- Omit the row entirely — no placeholder/N/A value. Applies to both `#w` and `#wp`, in both
  fill-templates (never add the row) and templates-update (never force the row; remove it if
  incorrectly present from a prior run or manual edit).

### Retroactive backfill
- `templates-update` proactively re-evaluates every eligible `#w` **and** `#wp` card in a
  processed file on every run, via the shared Repair 3d — not an opt-in backfill.

### Legacy label note (resolved by reference, not by quoting)
- The mis-mapped-label safeguard in Repair 3d must detect a stray line carrying the label
  that `label-aliases.json`'s existing generic `honorific:` key maps to. This plan
  intentionally does not repeat that literal string here — it belongs to a separate,
  already-completed `#wc` deprecation cleanup (see `label-aliases.json` and
  `templates-update.md`'s existing Repair 3c, both unchanged and out of scope for this plan).
  Implementers should read the current value of that alias entry directly from
  `label-aliases.json` at implementation time rather than trusting a copy pasted into this
  plan.
- Repair 3c itself is **not modified by this plan** — confirmed still live and load-bearing
  (the `label-aliases.json` `honorific:` alias still exists, and `templates-update.md`'s
  Repair 1 explicitly declines to flag lines matching that legacy label because it expects
  Repair 3c to clean them up downstream). Removing or altering Repair 3c is out of scope
  here.

## Steps

1. **Create `.cowork/skills/references/honorific-forms.md`** — new reference file, single
   source of truth for both skills and both card types. (This supersedes the earlier draft
   name `honorific-noun-forms.md`, which was never actually created — a clean rename.)
   Contents:
   - Eligibility heuristic, stated separately per card type: `#w` (bare noun, no particle,
     not a conjugated ending, suru-nouns count) and `#wp` (single い/な-adjective in plain
     dictionary form per `adj-forms.md`'s type determination; non-adjective/all-dash `#wp`
     entries never eligible). `#wc` explicitly never eligible for this row.
   - Already-prefixed exclusion for both types, with the `#wp`-specific note explaining the
     different underlying rationale (lexically-fused お in words like おいしい/おかしい vs. a
     genuine second-prefix conflict for `#w`).
   - お vs ご rule of thumb (wago → お, kango → ご) with known exceptions, split into a noun
     exception list (お電話, お食事, お時間, お店, etc.) and an adjective exception list
     (お忙しい, お若い, ご立派, お元気, ご親切, etc.), plus loanword guidance (generally no
     prefix, both types).
   - Explicit uncertainty instruction: if not confident, treat as "no natural form" (omit) —
     both types.
   - Value/furigana format, including the `#w`-only, confirmed-N/A-for-`#wp` suru-noun
     `(する)`-dropping rule.
   - Placement rule, stated separately per type (`#w`: after Japanese line; `#wp`: new final
     form row, after そう (looks)).
   - Clarifying note distinguishing this row from the unrelated `#wc`
     `お〜になる (honorific)` verb form — different mechanism, different card type, `#wc` is
     never eligible for this row.

2. **Update `.cowork/skills/references/card-templates.md`** — add the conditional
   `お/ご (honorific):` row to both the canonical `#w` template block and the canonical
   `#wp` template block (as the new 5th/last form line, after そう (looks)), each with a note
   pointing to `honorific-forms.md`.

3. **Update `.cowork/skills/references/label-aliases.json`** — add only unambiguous
   variant-spelling entries for the new label (full-width slash `お／ご (honorific):`,
   `o/go honorific:`, `お/ご honorific:`), usable for both card types since the label is
   shared. Do **not** reuse or repoint the existing generic `honorific:` key, which stays
   mapped to its current legacy target for the unrelated, already-completed `#wc`
   deprecation cleanup (see `label-aliases.json` for that entry's exact current value — not
   reproduced here).

4. **Update `.cowork/skills/fill-templates.md`**:
   - **`#w`:** split existing Step 8 into Step 8a (evaluate eligibility per
     `honorific-forms.md`; insert `お/ご (honorific): [word+furigana]` after the Japanese
     field line if a natural form exists) and Step 8b (was Step 8: append kanji links after
     the Japanese line or the honorific row, whichever is last).
   - **`#wp`:** add a new sub-instruction to **Step 5** (adjective skeleton fill): after
     computing and filling the 4 standard adjective forms (過去形, 否定形, 副詞形, そう
     (looks)), evaluate honorific eligibility per `honorific-forms.md` and, if a natural
     form exists, append the `お/ご (honorific):` row as the new 5th/last form line — before
     the block's kanji links are added in Step 6.
   - **Kanji trainer links section:** update the `#w` bullet (currently "append links after
     the Japanese field line (Step 8)") to reference Step 8b and the honorific row. The
     `#wc`/`#wp` bullet (currently "append links after the last conjugation/adjective row
     (Step 6)") needs no wording change, since it is already generic to "last row" — but
     state explicitly, in this step, that this wording only stays correct because the new
     `#wp` honorific sub-instruction (added to Step 5) runs *before* Step 6, so the
     honorific row (when present) is already the "last adjective row" by the time Step 6
     executes. Do not leave this ordering dependency implicit.
   - Update both the `#w` and `#wp` example blocks in "Card format reference" to show the
     optional row.
   - Cite `.cowork/skills/references/honorific-forms.md` inline within both Step 8a and the
     new Step 5 sub-instruction (matching the existing inline-citation pattern used for
     `verb-conjugation.md`/`adj-forms.md`; no consolidated reference list exists in this
     file).

5. **Update `.cowork/skills/templates-update.md`**:
   - Add `honorific-forms.md` to the `## References` section (plain heading, fifth entry).
   - Update Step 2's block-structure description to mention the optional extra line for both
     `#w` (optional 3rd line) and `#wp` (optional 5th form line).
   - Update Repair 2's card-type table: add an explicit `#wp` honorific carve-out — `#wp`
     cards continue through Repairs 4/4b as today, and are *also* explicitly routed through
     the new Repair 3d. `#w` cards continue to skip Repairs 3/3b/4/4b as today, and are also
     routed through Repair 3d. Do not leave the `#wp` routing implicit in the existing
     table.
   - Add **Repair 3d (`#w` and `#wp`, shared)** — one repair, single set of steps,
     card-type-conditional only on placement:
     1. **Mis-mapped-label safeguard (run first):** on `#w` or `#wp` cards, scan for a
        stray line carrying the label that the existing generic `honorific:` alias in
        `label-aliases.json` maps to (see that file for the exact current string — not
        reproduced here, since it belongs to the unrelated, already-completed `#wc`
        deprecation). If found, extract its value and proceed to step 3 below to
        re-evaluate and either rewrite it to the canonical `お/ご (honorific):` label or
        remove it — never leave it stray. `#wc` cards keep going through the existing,
        unmodified Repair 3c for the same literal label.
     2. Determine eligibility using `honorific-forms.md`'s per-type criteria (including
        each type's already-prefixed/lexically-fused-お exclusion).
     3. If not eligible: remove the row (or the mis-mapped line from step 1) if present;
        otherwise no-op.
     4. If eligible: judge whether a natural お/ご form exists (`#w` suru-noun values omit
        `(する)`; not applicable to `#wp`).
        - Missing + natural form exists → insert at the canonical position for that card
          type (`#w`: after Japanese line; `#wp`: new final form row, after そう (looks)).
        - Present + correct → no-op.
        - Present + incorrect → correct it.
        - No natural form exists + row present → remove it (never replace with a
          placeholder).
     5. **Uncertainty rule:** if Claude cannot confidently judge eligibility or prefix
        choice, do not guess — leave the card unchanged and flag it in the repair summary
        ("Uncertain honorific eligibility/prefix — not modified").
   - **Ordering constraint (`#wp` only):** Repair 3d must run **after Repair 4b**, not
     merely wherever its written position in the step list might imply. Repair 4b is what
     finalizes そう (looks)'s correct value; if Repair 3d ran before 4b, it would anchor its
     "insert after そう" placement and/or eligibility judgment on a stale そう value that 4b
     would later overwrite. State this explicitly as a required execution-order note.
   - Skip conditions: `#wc` cards skip Repair 3d entirely — they keep their own, separate,
     unmodified `お〜になる (honorific)` field and continue through the existing Repair 3c
     for the legacy label, unchanged by this plan.
   - Update the Step 4 repair summary list to include Repair 3d counts/details (combined
     `#w`+`#wp`, or broken out by type — implementer's choice, consistent with how other
     repairs report).
   - Update Repair 6's placement rule: for `#w` cards with no kanji links, ID goes after the
     honorific row (if present) or after the Japanese line (if not) — unchanged from the
     original design. For `#wp` cards with no kanji links, ID goes after the honorific row
     (if present) or after そう (looks) (if not) — new addition, parallel logic.
   - **Verify no changes needed to `.cowork/skills/references/adj-forms.md`** — confirmed
     out of scope: `adj-forms.md` governs the 4 mechanical conjugation forms only; honorific
     eligibility/value logic lives entirely in the new `honorific-forms.md`, and the
     `(する)`-dropping question was explicitly checked and confirmed N/A for `#wp` (see
     Design decisions above). Record this as a verified checkbox, not a silent omission.

6. **Verify no changes needed to `.cowork/skills/references/verb-conjugation.md`** —
   confirmed out of scope (verb-only reference; `#wc` is never eligible for this row).

## Risks
- **Generic `honorific:` alias key remains shared/ambiguous by design**, same trade-off as
  the original `#w`-only plan, now extended to also cover `#wp`: relies on Repair 3d's
  shared mis-mapped-label safeguard to catch and correct any mis-mapping after the fact, for
  both card types. `fill-templates` never goes through the alias table (only affects
  hand-edits to already-filled cards).
- **No placeholder means no "already evaluated" marker**, for both `#w` and `#wp` — every
  `templates-update` run re-judges every eligible card from scratch. Accepted, deliberate
  trade-off, carried over unchanged from the original design.
- **Judgment-call correctness risk**, now doubled in surface area across two card types:
  お/ご selection has real exceptions and no fully reliable algorithm for either nouns or
  adjectives. The uncertainty rule (flag rather than force) mitigates this but relies on
  Claude's honest self-assessment.
- **`#wp` ordering dependency is easy to get wrong at implementation time**: Repair 3d must
  run after Repair 4b (so そう's value is final before the honorific row is placed/judged
  relative to it), not simply wherever Repair 3d happens to sit in the numbered step list.
  skill-implementer should treat this as a hard execution-order requirement.
- **Never touch `<!--ID:-->` lines or values, `TARGET DECK`, or anything above
  `# Summary`** — Repair 3d only inserts/edits/removes the honorific row itself; ID values
  and positions are governed unchanged by Repair 6.
- **`#wc` exclusion must stay hard-coded** — any future template refactor must not
  accidentally extend this row to `#wc` cards, which already have their own distinct
  honorific mechanism (`お〜になる (honorific)`, governed by the separate
  `Plans/wc-honorific-special-verb-plan.md`). The two plans' `templates-update.md` repairs
  are independent and sequential (3c → 3d [this plan] → 3e [that plan] → 4) — not competing
  for the same numbering slot.
- **`#wp`'s already-prefixed exclusion has a different rationale than `#w`'s**, even though
  the mechanical check is identical — the reference file must document this distinction
  (lexically-fused お vs. genuine double-prefixing) so a future implementer doesn't assume
  one explanation covers both card types.

## Not in scope for this plan
- No changes to `#wc`'s `お〜になる (honorific)` field, its derivation logic, or
  `templates-update.md`'s (separately renumbered) Repair 3e — that is entirely
  `Plans/wc-honorific-special-verb-plan.md`'s scope.
- No changes to `templates-update.md`'s existing Repair 3c (尊敬語 cleanup) or
  `label-aliases.json`'s existing generic `honorific:` alias entry — both confirmed live,
  load-bearing, and unrelated to this plan.
- No batch sweep of already-filled lesson files — lazy update only, applied the next time
  `templates-update` runs on a given file (same precedent as the original `#w`-only design
  and the `wc-honorific-special-verb` plan).
