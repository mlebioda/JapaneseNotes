# Tasks: kanji-headers + update-kanji-list speed improvements

**Date:** 2026-06-07
**Plan:** `Plans/kanji-speed-plan.md`
**Target files:** `.cowork/skills/kanji-headers.md`, `.cowork/skills/update-kanji-list.md`
**Status:** done

---

## Task list

| # | File | Change | Status |
|---|------|--------|--------|
| 1 | **kanji-headers.md** | Change 1 — Compile `kanji-file-map` during step 2; pass it to `update-kanji-list` in step 5 handoff | [x] |
| 2 | **update-kanji-list.md** | Change 1 — Add `[kanji-file-map]` optional input; add skip logic in Step 2 "Check if kanji file exists" | [x] |
| 3 | **update-kanji-list.md** | Change 2 — Add Pre-flight check section before the processing loop | [x] |
| 4 | **update-kanji-list.md** | Change 3 — Split Step 1 into Phase A (read once) / Phase B (per-kanji check) / Phase C (single write) | [x] |
| 5 | **update-kanji-list.md** | Change 4 — Rewrite processing order to Phase I (all fetches) / Phase II (all file ops); update Step 0 and Step 3 opening lines | [x] |
| 6 | **Scribe capture** | Log all changes via scribe agent capture mode | [x] |

---

## Notes

- Tasks 1 and 2 are paired: the `kanji-file-map` is in-memory data only — no file on disk is created.
- Tasks 3 and 4 are independent of each other and of Tasks 1/2/5.
- Task 5 does not alter content written to any file — only the timing of fetches vs. writes.
- Identical output and behaviour is the constraint — no feature changes.
