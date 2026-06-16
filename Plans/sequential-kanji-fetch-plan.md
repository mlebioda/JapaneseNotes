# Sequential Kanji Fetch — Rate-Limit Prevention

## Goal

kanji-trainer.org returns HTTP 429 (Too Many Requests) when multiple fetch requests are made
concurrently. Both `kanji-file` and `kanji-headers` need explicit sequential-fetch rules so
Claude never issues parallel web requests to the site, regardless of how many kanji are
processed in a single run.

## Approach

Add a short, unambiguous rule to each skill at the exact point where fetches are initiated.
No structural changes to the workflow; wording only.

## Steps

### 1. `.cowork/skills/kanji-file.md` — Step B

In the `### Step B — Web fetch (conditional)` section, append the following note directly
after the paragraph that begins "Fetch the mnemonic page from:":

```
**Rate-limit rule**: Fetches to kanji-trainer.org must be done sequentially — one at a time.
Never issue parallel or concurrent requests to the site, even when `kanji-file` is called
for multiple kanji in a single run. Wait for the current fetch (and any resulting writes) to
complete before starting the next kanji.
```

Insert it between the code block showing the URL pattern and the "From the fetched HTML,
extract:" paragraph, so the section reads:

```
Fetch the mnemonic page from:

    https://kanji-trainer.org/Mnemonic_phrase/Mnemonic_X.html

where `X` is the Unicode code point of the kanji character in decimal (e.g. `近` → `36817`).

**Rate-limit rule**: Fetches to kanji-trainer.org must be done sequentially — one at a time.
Never issue parallel or concurrent requests to the site, even when `kanji-file` is called
for multiple kanji in a single run. Wait for the current fetch (and any resulting writes) to
complete before starting the next kanji.

From the fetched HTML, extract:
...
```

### 2. `.cowork/skills/kanji-headers.md` — Step 2

In **Step 2 — Ensure kanji reference files exist**, add the following rule at the end of the
step, after the "Cycle guard" paragraph and before the blank line that separates Step 2 from
Step 3:

```
**Sequential processing rule**: Process kanji one at a time. After calling `kanji-file` for
a kanji (step 3 or 4 above), wait for it to complete fully before moving to the next kanji
in the list. Never call `kanji-file` for multiple kanji in parallel. This prevents HTTP 429
rate-limit errors from kanji-trainer.org.
```

## Risks

- Text-only change; no logic or data paths altered.
- No `<!--ID:-->` lines, `TARGET DECK`, or `# Summary` sections are near the edit locations.
- Existing skill behaviour is unchanged — the rules clarify intent that was previously implicit.
