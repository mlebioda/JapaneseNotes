# Plan: kanji-headers + update-kanji-list speed improvements

**Goal:** reduce wall-clock execution time without changing output or behaviour.  
**Scope:** `.cowork/skills/kanji-headers.md` and `.cowork/skills/update-kanji-list.md`.  
**Constraint:** identical output and behaviour — no feature changes.

---

## Background

When the user runs "kanji headers [file]", the following happens:

1. `kanji-headers` reads the target file and extracts N kanji from `##` headers.
2. For **each** kanji, `kanji-headers` searches `Kaligrafia/Kanji/**/漢*` to find or confirm the wikilink.
3. `kanji-headers` writes the formatted kanji blocks to the file.
4. `kanji-headers` hands off to `update-kanji-list`, which:
   - For each kanji: does **another** `Kaligrafia/Kanji/**/漢*` search (and a `Kaligrafia/Primitives/` search) to decide routing/existence.
   - Reads `KanjiList.md` inside the loop to check for duplicates.
   - Fires a `WebFetch` per kanji, then writes files for that kanji, then fetches the next kanji.

The four biggest time-wasters, in priority order:

| # | Problem | Why it hurts |
|---|---------|-------------|
| 1 | Duplicate file searches | `kanji-headers` runs one `find` per kanji; `update-kanji-list` runs the same `find` again for every kanji |
| 2 | No fail-fast on missing source file | `update-kanji-list` may run N web fetches before discovering the source file is wrong |
| 3 | `KanjiList.md` read inside the loop | One read per kanji instead of one read total |
| 4 | Web fetches interleaved with file writes | Fetches run one at a time, stalled behind file I/O |

---

## Changes

### Change 1 — Pass the file-existence map from kanji-headers to update-kanji-list (eliminates finding #1)

**File:** `kanji-headers.md` and `update-kanji-list.md`

**How:**

In `kanji-headers`, after all `Kaligrafia/Kanji/**/漢*` searches are complete (step 2 of its workflow), compile the results into a simple lookup that maps each kanji character to either its found filename (without `.md`) or "not found".  Pass this map to `update-kanji-list` as part of the handoff at the end of step 5.

In `update-kanji-list`, add an **Optional input** field: `[kanji-file-map]` — a character → filename map produced by `kanji-headers`. When this map is present, skip the `Kaligrafia/Kanji/` search in Step 2 for any kanji already in the map. Only run the search for kanji not present in the map (e.g. newly seen kanji that `kanji-headers` marked "not found" and that `update-kanji-list` must decide to route to `Primitives/`).

**kanji-headers.md change — workflow step 2 (extract kanji):**

After each `Kaligrafia/Kanji/**/漢*` search, record the result in a per-run map:
```
kanji-file-map[漢] = "漢-kanji,china"   # found
kanji-file-map[電] = null               # not found
```

**kanji-headers.md change — workflow step 5 (handoff):**

Replace the current sentence "Run the `update-kanji-list` workflow on the same file" with:

> Run the `update-kanji-list` workflow on the same file, passing `kanji-file-map` as the `[kanji-file-map]` input.

**update-kanji-list.md change — Input section:**

Add:
> - `[kanji-file-map]` *(optional)* — map of `character → filename (no .md)` pre-computed by `kanji-headers`. When provided, skip the `Kaligrafia/Kanji/` search in Step 2 for characters present in the map.

**update-kanji-list.md change — Step 2, "Check if kanji file exists" paragraph:**

Add before the search instruction:
> If `[kanji-file-map]` was provided and contains an entry for this kanji character, use that entry directly — skip the `Kaligrafia/Kanji/` and `Kaligrafia/Primitives/` searches. A `null` entry means no Kanji file was found; still search `Kaligrafia/Primitives/` for possible routing.

---

### Change 2 — Fail-fast if source file doesn't exist (eliminates finding #2)

**File:** `update-kanji-list.md`

**Where:** Before "Processing order (per kanji)" — add a new **Pre-flight check** section at the top of the Processing order block.

**New section text:**

```
## Pre-flight check

Before processing any kanji, verify that `[file]` exists and is readable.
If the file cannot be found, stop immediately and report:

  ERROR: Source file "[file]" not found — aborting. No files were modified.

Do not proceed to Step 0 or any subsequent step.
```

This ensures N web fetches are not fired for a mistyped filename.

---

### Change 3 — Read KanjiList.md once before the loop (eliminates finding #3)

**File:** `update-kanji-list.md`

**Where:** Step 1 — "Update KanjiList.md"

**Current wording (implicit, per-kanji):**
> Read the full contents of `KanjiList.md` first. For each extracted kanji: …

**New wording:**

Split the step into two clearly separated phases:

> **Phase A — Read once (before the loop):** Read the full contents of `KanjiList.md` and hold it in memory as `kanjilist-content`. Also collect the full extracted kanji list from `[file]` and de-duplicate it.
>
> **Phase B — One pass per kanji:** For each kanji character, check `kanjilist-content` for an exact match. Collect all characters that are not present into `to-add` list.
>
> **Phase C — Single write:** After all kanji are checked, append every character in `to-add` to `KanjiList.md` in one write operation.

This replaces one read-per-kanji + one append-per-kanji with one read + one write total.

---

### Change 4 — Batch all web fetches before any file writing (eliminates finding #4)

**File:** `update-kanji-list.md`

**Where:** "Processing order (per kanji)" and Step 0.

**Current order:**

> For each kanji: Step 0 (fetch) → Step 1 → Step 2 → Step 3 → Step 4

This means: fetch kanji-1, write kanji-1 files, fetch kanji-2, write kanji-2 files, …

**New order:**

Split processing into two phases:

> **Phase I — All fetches first:**
> Run Step 0 for every kanji before any file writing. Store each result (mnemonic text, explanation text, or failure flag) in a per-kanji fetch-results map keyed by kanji character.
>
> **Phase II — All file operations:**
> For each kanji, execute Steps 1–4 using the pre-fetched data from fetch-results. No web fetches occur during this phase.

Update the "Processing order" block to reflect this:

```
Phase I — Fetch (all kanji, no file writes):
  Step 0 for kanji-1
  Step 0 for kanji-2
  …
  Step 0 for kanji-N

Phase II — Write (all kanji, using cached fetch data):
  For each kanji: Step 1 → Step 2 → Step 3 (using cached result) → Step 4

After all kanji:
  Step 5 — Consistency check
  Completion report
```

Update Step 0's opening line from:

> **This step runs first, before any file writing, for each kanji being processed.**

to:

> **This step runs for ALL kanji in Phase I, before any file writing begins. Results are cached in a fetch-results map and consumed during Phase II.**

Update Step 3's opening line from:

> **Runs after Step 2, only when Step 0 returned a valid Explanation text.**

to:

> **Runs after Step 2, only when the fetch-results map contains a valid Explanation text for this kanji.**

---

## Implementation notes

- Changes 2 and 3 are independent of each other and of Changes 1 and 4 — they can be written in any order.
- Change 1 requires edits to both files. The `kanji-file-map` is in-memory data passed at handoff time; no file on disk is created.
- Change 4 does not alter the content written to any file — only the timing of when fetches vs. writes occur. The completion report format is unchanged.
- All step numbers in the completion report remain the same.

---

## Files to edit

1. `.cowork/skills/kanji-headers.md` — Changes 1 (map compilation + handoff wording)
2. `.cowork/skills/update-kanji-list.md` — Changes 1 (optional input + Step 2 skip), 2 (pre-flight), 3 (Step 1 phase split), 4 (processing order + Step 0/3 wording)
