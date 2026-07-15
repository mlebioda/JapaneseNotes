# #w / #wp honorific (お/ご) row — Tasks

- [x] Create `.cowork/skills/references/honorific-forms.md` with:
  - [x] Eligibility heuristic, per card type: `#w` (bare noun, no particles, not a
        conjugated ending, suru-nouns count) and `#wp` (single い/な-adjective in plain
        dictionary form per `adj-forms.md`'s type determination; non-adjective/all-dash
        `#wp` entries never eligible); `#wc` explicitly never eligible
  - [x] Already-prefixed exclusion for both types, including the `#wp`-specific note that
        this catches lexically-fused お (おいしい, おかしい, おしゃれ, おもい) — a
        different underlying reason than `#w`'s genuine already-prefixed case (お願い,
        お金, お弁当, お邪魔)
  - [x] お/ご rule of thumb + known exceptions, split into a noun list (お電話, お食事,
        お時間, お店) and an adjective list (お忙しい, お若い, ご立派, お元気, ご親切) +
        loanword guidance (generally no prefix, both types)
  - [x] Uncertainty instruction: if not confident, treat as "no natural form" (omit) —
        both types
  - [x] Value/furigana format, including the fixed rule that `#w` suru-noun entries drop
        `(する)` in the honorific value (e.g. `担当(たんとう)(する)` →
        `ご担当(たんとう)`, not `ご担当(たんとう)(する)`), and an explicit note that this
        rule is confirmed N/A for `#wp` (verified via `adj-forms.md` — `#wp` values never
        carry `(する)`)
  - [x] Placement rule, per type: `#w` after Japanese line, before kanji links (unchanged);
        `#wp` as the new final form row, immediately after そう (looks), before kanji links
  - [x] Clarifying note distinguishing this row from the unrelated `#wc`
        `お〜になる (honorific)` verb form — `#wc` never eligible for this row
- [x] Update `.cowork/skills/references/card-templates.md` — add conditional
      `お/ご (honorific):` row to both the canonical `#w` template block and the canonical
      `#wp` template block (as the new 5th/last form line, after そう (looks)), each with a
      note pointing to `honorific-forms.md`
- [x] Update `.cowork/skills/references/label-aliases.json`:
  - [x] Add only unambiguous variant-spelling entries for the new shared label (full-width
        slash `お／ご (honorific):`, `o/go honorific:`, `お/ご honorific:`) — do **not**
        reuse or repoint the existing generic `honorific:` key, which stays mapped to its
        current legacy target for the unrelated, already-completed `#wc` deprecation
        cleanup (see the file itself for that entry's exact current value)
- [x] Update `.cowork/skills/fill-templates.md`:
  - [x] `#w`: split Step 8 into Step 8a (evaluate eligibility, insert honorific row after
        Japanese field line if a natural form exists) and Step 8b (append kanji links after
        the Japanese line or the honorific row, whichever is last)
  - [x] `#wp`: add a new sub-instruction to Step 5 (adjective skeleton fill) — after
        filling the 4 standard forms, evaluate honorific eligibility and append the row as
        the new 5th/last form line, before Step 6's kanji links
  - [x] Update the "## Kanji trainer links" section: `#w` bullet references Step 8b and the
        honorific row; state explicitly that the `#wc`/`#wp` bullet needs no wording change
        only because the new Step 5 sub-instruction runs before Step 6 (don't leave this
        ordering dependency implicit)
  - [x] Update both the `#w` and `#wp` example blocks in "Card format reference" to show
        the optional row
  - [x] Cite `honorific-forms.md` inline within Step 8a and the new Step 5 sub-instruction
        (matching the existing inline-citation pattern; no consolidated reference list
        exists in this file)
- [x] Update `.cowork/skills/templates-update.md`:
  - [x] Add `honorific-forms.md` to the `## References` section (plain heading, fifth
        entry)
  - [x] Update Step 2's block-structure description to mention the optional extra line for
        both `#w` (optional 3rd line) and `#wp` (optional 5th form line)
  - [x] Update Repair 2's card-type table: explicit `#wp` honorific carve-out (continues
        through Repairs 4/4b, also routed through new Repair 3d) alongside the existing
        `#w` carve-out (also routed through Repair 3d)
  - [x] Add Repair 3d (`#w` and `#wp`, shared — single repair, card-type-conditional only
        on placement):
    - [x] Mis-mapped-label safeguard: detect a stray line carrying the label the existing
          generic `honorific:` alias maps to (see `label-aliases.json` for the exact
          string — not reproduced in the skill file either), extract its value, and
          re-evaluate/rewrite or remove it — never leave it stray. `#wc` cards keep using
          the existing, unmodified Repair 3c for the same literal label
    - [x] Eligibility check per `honorific-forms.md`'s per-type criteria (including each
          type's already-prefixed/lexically-fused-お exclusion)
    - [x] Add/correct/remove the row per the natural-form judgment (`#w` suru-noun values
          drop `(する)`; not applicable to `#wp`), with type-conditional placement
    - [x] Uncertainty rule: flag for user review instead of guessing
    - [x] Skip conditions: `#wc` cards skip Repair 3d entirely (they keep the existing
          Repair 3c for the legacy label, unchanged by this plan)
  - [x] Add explicit ordering-constraint note: Repair 3d must run after Repair 4b (not
        merely wherever it sits in the written step list), so it never anchors on a stale
        そう (looks) value that 4b later overwrites
  - [x] Update Repair 6's placement rule: `#w` — ID goes after the honorific row (if
        present) or after the Japanese line (if not), unchanged. `#wp` — ID goes after the
        honorific row (if present) or after そう (looks) (if not), new addition
  - [x] Update the Step 4 repair summary list to include Repair 3d counts/details
  - [x] Verify no changes needed to `.cowork/skills/references/adj-forms.md` (confirm
        `(する)`-dropping rule is N/A for `#wp` and honorific logic lives entirely in
        `honorific-forms.md` — record as verified, not a silent omission)
- [x] Verify no changes needed to `.cowork/skills/references/verb-conjugation.md` (confirm
      out of scope — `#wc` never eligible for this row, no edit required)
- [x] Self-review: confirm `#wc` cards are never eligible anywhere in the updated skill
      files; already-prefixed/lexically-fused-お words are excluded for both `#w` and
      `#wp`; the `(する)`-dropping rule applies only to `#w` and is confirmed N/A for `#wp`;
      the generic `honorific:` alias key and existing Repair 3c are both untouched; Repair
      3d runs after Repair 4b; no `<!--ID:-->`/`TARGET DECK`/above-`# Summary` content is
      touched by the new repair logic

## Cross-plan consistency fix (completed as part of this revision)

- [x] `Plans/wc-honorific-special-verb-plan.md`: renumber all "Repair 3d" references to
      "Repair 3e" (Approach paragraph, Step 5 body, summary bullets, Risks section) and add
      a cross-reference note at the Repair 3e insertion point clarifying it runs after this
      plan's Repair 3d (sequence: 3c → 3d [this plan] → 3e [that plan] → 4)
- [x] `Plans/wc-honorific-special-verb-tasks.md`: renumber all "Repair 3d" references to
      "Repair 3e" and add the same cross-reference note
