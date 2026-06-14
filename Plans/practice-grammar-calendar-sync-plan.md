# Practice Grammar — Calendar Sync Fixes

## Goal

The `## Calendar sync` section added to `.cowork/skills/practice-grammar.md` contains ten issues ranging from RFC 5545 compliance bugs to a hardcoded session path that will break on any other machine. This plan fixes all ten, incorporates the user's design decision for issue #6 (timestamped filenames instead of overwrite), and updates `instructions.md` to resolve the resulting vault-root policy conflict and registry entry gap.

## Approach

All fixes are applied directly to two files: `practice-grammar.md` (Calendar sync section, session summary template, and step 10 wording) and `.cowork/instructions.md` (vault-root policy exception and skill registry entry). The Python script embedded in the skill is rewritten in place with all six code-level fixes applied together. No new files are created in `.cowork/`; the plan itself lands only in `Plans/`.

## Steps

### 1. Fix DTEND (critical bug — RFC 5545 §3.6.1)

File: `.cowork/skills/practice-grammar.md` — the `by_date` loop inside the Python script.

`DTEND` for an all-day event must be the **exclusive** end date — the day after `DTSTART`. The current script sets both to the same `dtstr`, which makes zero-duration events that many calendar clients silently discard or render incorrectly.

Replace the `DTEND` line generation:

Current:
```python
f"DTEND;VALUE=DATE:{dtstr}",
```

Fixed — import `timedelta` and compute end date before the loop:

```python
from datetime import date, timedelta
```

Then inside the loop, derive end from the parsed date:

```python
dt_date = date.fromisoformat(d)          # uses the same parsed date as step 4
dt_end  = (dt_date + timedelta(days=1)).strftime("%Y%m%d")
...
f"DTEND;VALUE=DATE:{dt_end}",
```

### 2. Add RFC 5545 line-length folding (critical bug — RFC 5545 §3.1)

RFC 5545 requires that no content line exceed 75 octets (bytes, not characters). Long DESCRIPTION lines will cause import failures in strict clients (Apple Calendar, Google Calendar import).

Add a `fold()` helper before the `lines = [...]` block:

```python
def fold(line: str) -> str:
    """Fold a single ICS content line to max 75 octets per RFC 5545 §3.1."""
    encoded = line.encode("utf-8")
    if len(encoded) <= 75:
        return line
    out = []
    while len(encoded) > 75:
        # Split at 75-byte boundary, careful not to break a multi-byte character
        chunk = encoded[:75].decode("utf-8", errors="ignore")
        # Walk back if the last byte is a continuation byte
        while len(chunk.encode("utf-8")) > 75:
            chunk = chunk[:-1]
        out.append(chunk)
        encoded = b" " + encoded[len(chunk.encode("utf-8")):]
    out.append(encoded.decode("utf-8"))
    return "\r\n".join(out)
```

Apply it when writing the file — wrap every line through `fold()`:

```python
with open(ics_path, "w", encoding="utf-8") as f:
    f.write("\r\n".join(fold(l) for l in lines) + "\r\n")
```

### 3. Replace hardcoded session path with stable vault root (moderate)

File: `.cowork/skills/practice-grammar.md` — the Python script preamble.

Current hardcoded paths:
```python
json_path = "/sessions/stoic-jolly-noether/mnt/ObsidianJP/.cowork/progress/grammar-state.json"
ics_path  = "/sessions/stoic-jolly-noether/mnt/ObsidianJP/japanese-grammar-review.ics"
```

Replace with the stable vault root. Add a note that Claude must translate to the active session mount path at runtime:

```python
# NOTE: Replace VAULT_ROOT with the active session mount path for this vault.
# Stable vault root (macOS): /Users/michallebioda/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianJP
VAULT_ROOT = "/Users/michallebioda/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianJP"
json_path  = f"{VAULT_ROOT}/.cowork/progress/grammar-state.json"
# ics_path is set below after the timestamp is computed (see issue #6)
```

### 4. Replace fragile `d.replace("-","")` with `date.fromisoformat()` (moderate)

Current:
```python
dtstr = d.replace("-", "")
```

This silently produces garbage if `next_review` has a time component or unexpected format. Replace with:

```python
dt_date = date.fromisoformat(d[:10])   # safe: slices to YYYY-MM-DD even if time is appended
dtstr   = dt_date.strftime("%Y%m%d")
```

This also provides the `dt_date` object needed for the DTEND fix in step 1.

### 5. Resolve vault-root policy conflict in `instructions.md` (moderate)

File: `.cowork/instructions.md` — `## General rules — always follow` section.

Current rule:
```
- Never create files directly in the vault root (`/ObsidianJP/`) unless explicitly asked
```

Append a documented exception immediately after that bullet:

```
- Never create files directly in the vault root (`/ObsidianJP/`) unless explicitly asked
  - Approved exception: `.ics` calendar files written by the practice-grammar skill (`japanese-grammar-review-<timestamp>.ics`). These are intentionally placed at the vault root for easy drag-and-drop calendar import.
```

### 6. Write timestamped file per session instead of overwriting (design decision)

File: `.cowork/skills/practice-grammar.md` — Calendar sync section prose and Python script.

Remove all mention of overwriting. Each session writes a new file:

Filename pattern: `japanese-grammar-review-<ISO-timestamp>.ics`
where `<ISO-timestamp>` = `date.today().strftime("%Y%m%dT%H%M%S")` computed once before the loop.

Update the VAULT_ROOT block and ics_path assignment:

```python
session_ts = date.today().strftime("%Y%m%dT%H%M%S")
ics_path   = f"{VAULT_ROOT}/japanese-grammar-review-{session_ts}.ics"
```

Update the prose at the top of `## Calendar sync`:

Current:
> After every session, write `japanese-grammar-review.ics` at the vault root (`/ObsidianJP/japanese-grammar-review.ics`). This is the only file Claude writes outside `.cowork/progress/`.
> ...
> Always overwrite the file completely (not append) — the file contains only this session's new events.

Replace with:

> After every session, write a new timestamped file `japanese-grammar-review-<YYYYMMDDTHHMMSS>.ics` at the vault root. Each session file is self-contained — only the grammar points practiced this session are included. The user imports the new file after each session; old files are left untouched and do not need to be deleted. This is the only file Claude writes outside `.cowork/progress/`.

Remove the "Always overwrite" bullet from the Rules list.

### 7. Make UIDs unique across sessions (minor)

File: `.cowork/skills/practice-grammar.md` — UID line in the Python script.

Current UID uses only the date and a fixed suffix, so two sessions on the same day reviewing the same grammar point would generate a duplicate UID:

```python
f"UID:{dtstr}-japanese-grammar-session-{date.today().isoformat()}@japanese-notes",
```

Add `import uuid` at the top of the script imports. Replace the UID line:

```python
f"UID:{dtstr}-{session_ts}-{str(uuid.uuid4())[:8]}@japanese-notes",
```

`session_ts` is already computed for the filename (step 6) — reuse it here. The UUID fragment adds collision resistance within the same timestamp second.

### 8. Remove stray `a` typo on line 382 (minor)

File: `.cowork/skills/practice-grammar.md` — the line immediately after the closing ```` ``` ```` of the Python code block.

Current (line 382):
```
a1. 
After running, print a one-line confirmation: `Calendar updated — N event(s) written to japanese-grammar-review.ics`.
```

Replace with (remove the `a` and the orphaned `1. ` prefix, update the filename reference to match the new pattern):
```
After running, print a one-line confirmation: `Calendar updated — N event(s) written to japanese-grammar-review-<timestamp>.ics`.
```

### 9. Update session summary template to mention the calendar file (minor)

File: `.cowork/skills/practice-grammar.md` — `## Session summary` section.

Current closing line of the summary block:
```
Next review dates written to grammar-state.json.
```

Replace with:
```
Next review dates written to grammar-state.json. Calendar file: japanese-grammar-review-<timestamp>.ics written to vault root.
```

### 10. Update `instructions.md` skill registry entry for practice-grammar (minor)

File: `.cowork/instructions.md` — `## Available skills` section, `practice-grammar` bullet.

Current:
```
- practice-grammar — interactive grammar drill for a lesson file; reads only `# 文法` + `# Vocabulary` (grammar topics) and `# ごい` + `# ひょうげん` (vocab pool). Writes results to `.cowork/progress/grammar-state.json` (SM-2 lite). Trigger: "let's practice <lesson>"
```

Replace with:
```
- practice-grammar — interactive grammar drill for a lesson file; reads only `# 文法` + `# Vocabulary` (grammar topics) and `# ごい` + `# ひょうげん` (vocab pool). Writes results to `.cowork/progress/grammar-state.json` (SM-2 lite) and generates a timestamped `.ics` calendar file (`japanese-grammar-review-<timestamp>.ics`) at the vault root for easy calendar import. Trigger: "let's practice <lesson>"
```

## Complete fixed Python script (reference)

The implementer should replace the entire script block in `## Calendar sync` with the following. This is the canonical fixed version incorporating all six code-level changes (steps 1–4, 6, 7):

```python
import json
import uuid
from datetime import date, timedelta
from collections import defaultdict

# NOTE: Replace VAULT_ROOT with the active session mount path for this vault.
# Stable vault root (macOS): /Users/michallebioda/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianJP
VAULT_ROOT = "/Users/michallebioda/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianJP"
json_path  = f"{VAULT_ROOT}/.cowork/progress/grammar-state.json"
session_ts = date.today().strftime("%Y%m%dT%H%M%S")
ics_path   = f"{VAULT_ROOT}/japanese-grammar-review-{session_ts}.ics"

session_ids = [...]  # list of grammar point IDs practiced this session

with open(json_path) as f:
    gp = json.load(f)["grammar_points"]

by_date = defaultdict(list)
for gid in session_ids:
    entry = gp.get(gid)
    if entry:
        d = entry.get("next_review", "")
        if d:
            by_date[d].append(entry.get("grammar_header", gid))

def fold(line: str) -> str:
    """Fold a single ICS content line to max 75 octets per RFC 5545 §3.1."""
    encoded = line.encode("utf-8")
    if len(encoded) <= 75:
        return line
    out = []
    while len(encoded) > 75:
        chunk = encoded[:75].decode("utf-8", errors="ignore")
        while len(chunk.encode("utf-8")) > 75:
            chunk = chunk[:-1]
        out.append(chunk)
        encoded = b" " + encoded[len(chunk.encode("utf-8")):]
    out.append(encoded.decode("utf-8"))
    return "\r\n".join(out)

lines = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//Japanese Grammar Review//EN",
    "CALSCALE:GREGORIAN",
]
for d in sorted(by_date):
    headers  = by_date[d]
    dt_date  = date.fromisoformat(d[:10])
    dtstr    = dt_date.strftime("%Y%m%d")
    dt_end   = (dt_date + timedelta(days=1)).strftime("%Y%m%d")
    lines += [
        "BEGIN:VEVENT",
        f"DTSTART;VALUE=DATE:{dtstr}",
        f"DTEND;VALUE=DATE:{dt_end}",
        f"SUMMARY:Japanese Grammar Review — {len(headers)} point(s)",
        "DESCRIPTION:" + "\\n".join(headers),
        f"UID:{dtstr}-{session_ts}-{str(uuid.uuid4())[:8]}@japanese-notes",
        "END:VEVENT",
    ]
lines.append("END:VCALENDAR")

with open(ics_path, "w", encoding="utf-8") as f:
    f.write("\r\n".join(fold(l) for l in lines) + "\r\n")
print(f"Written {len(by_date)} event(s) to {ics_path}")
```

## Risks

- The `instructions.md` vault-root policy exception (step 5) modifies a file in `.cowork/` — requires the user's explicit permission per project rules. The implementer must note this and wait for approval before touching `instructions.md`.
- The skill registry update in `instructions.md` (step 10) is in the same file — both changes should land in a single edit to avoid two passes over a protected file.
- The `fold()` helper splits on byte boundaries; if a grammar header contains very long kanji sequences, the split point could fall mid-character. The `errors="ignore"` + walk-back loop handles this but should be tested against a DESCRIPTION line with 20+ kanji headers.
- Step 9 embeds `<timestamp>` literally in the session summary template — make sure the implementer uses it as a placeholder label, not a literal string. The actual value is `session_ts` at runtime.
