# ICS Export Extraction

## Goal

Extract the duplicated inline ICS generation code from `practice-grammar.md` (lines 672-738) and `manage-holidays.md` (lines 174-269) into a single standalone Python script `.cowork/scripts/ics-export.py`. Both skills will then call the script via shell invocation instead of embedding Python blocks. This eliminates the duplicated `fold()` function and VCALENDAR construction logic, makes the ICS generation independently testable, and follows the same CLI pattern established by `load-control.py`.

## Approach

Create a single script with two modes (`session` and `full`) selected via `--mode`. Session mode reads grammar point keys from stdin and exports only those points; full mode exports all future review dates plus holiday events. All ICS-building logic is decomposed into small testable functions. The skill files are updated to replace their inline Python blocks with shell invocations that pipe data into the script.

Key trade-off: using stdin for session keys (rather than a `--keys` argument) avoids shell argument length limits when many grammar points are practiced in a single session. This matches the pattern used by `load-control.py`.

## Steps

### 1. Create `.cowork/scripts/ics-export.py`

CLI interface (argparse):
- `--mode session|full` (required)
- `--state <path>` (default: `.cowork/progress/grammar-state.json`)
- `--holidays <path>` (default: `.cowork/progress/holidays.json`, used in full mode only)
- `--output <path>` (required -- output .ics file path)
- `--today <ISO date>` (optional, for testing -- defaults to `date.today()`). Used in full mode only to filter future dates. Ignored in session mode (session mode exports all requested keys regardless of date).
- stdin: JSON array of grammar point keys (session mode only; ignored in full mode)

Note on output filenames: the skill files control the filename pattern (including timestamp). Use `datetime.now().strftime("%Y%m%dT%H%M%S")` for the timestamp to avoid same-day collisions — `date.today()` always produces `T000000`.

Testable functions to implement:

| Function | Purpose |
|---|---|
| `fold(line)` | RFC 5545 line folding (max 75 octets per line). Identical logic to current inline version, but with correct continuation-line prefix (SPACE character). |
| `build_vevent(dtstart, dtend, summary, description, uid)` | Returns list of ICS content lines for one VEVENT block. |
| `build_vcalendar(events)` | Wraps a list of VEVENT line-lists in VCALENDAR header/footer. Returns flat list of lines. |
| `load_session_points(state_path, keys)` | Reads grammar-state.json, accesses `["grammar_points"]` dict, filters to entries matching `keys`, returns dict of `{date_str: [grammar_header, ...]}`. |
| `load_full_points(state_path, today)` | Reads grammar-state.json, accesses `["grammar_points"]` dict, filters entries where `next_review >= today`, returns dict of `{date_str: [grammar_header, ...]}`. |
| `load_holidays(holidays_path, today)` | Reads holidays.json, returns sorted list of holiday date strings >= today. |
| `write_ics(path, lines)` | Applies `fold()` to each line, joins with CRLF, writes to file. |

Session mode flow:
1. Read JSON array of keys from stdin
2. Call `load_session_points()` to get `{date: [headers]}` grouped by `next_review`
3. Build one VEVENT per date using `build_vevent()`
4. Wrap in VCALENDAR, fold, write with CRLF

Full mode flow:
1. Call `load_full_points()` to get `{date: [headers]}` for all future reviews
2. Build review VEVENTs (one per date)
3. Call `load_holidays()` to get future holiday dates
4. Build holiday VEVENTs (one per date)
5. Wrap all in VCALENDAR, fold, write with CRLF

VEVENT field formats (preserving current behavior):

| Field | Session mode | Full mode (review) | Full mode (holiday) |
|---|---|---|---|
| SUMMARY | `Japanese Grammar Review — N point(s)` | `Japanese Grammar Review — N point(s)` | `Holiday — No Review` |
| DESCRIPTION | `\\n`-joined grammar headers | `\\n`-joined grammar headers | `Holiday — no grammar reviews scheduled.` |
| UID | `<YYYYMMDD>-<session_ts>-<8char-uuid>@japanese-notes` | `<YYYYMMDD>-full-export-<8char-uuid>@japanese-notes` | `<YYYYMMDD>-holiday-<8char-uuid>@japanese-notes` |
| DTSTART | `DTSTART;VALUE=DATE:YYYYMMDD` | same | same |
| DTEND | `DTEND;VALUE=DATE:YYYYMMDD+1` | same | same |

Note on SUMMARY separator: The current code uses `--` (ASCII double dash) in manage-holidays.md and `—` (Unicode em dash U+2014) in practice-grammar.md. Standardize on `—` (Unicode em dash U+2014) for both modes — it renders better in calendar apps.

Error handling:
- Missing state file in session mode: print error to stderr, exit 1
- Missing state file in full mode: treat as empty (no review events), print warning to stderr
- Missing holidays file in full mode: treat as empty (no holiday events), no warning
- Empty stdin in session mode: print "No keys provided" to stderr, exit 1
- Malformed JSON on stdin (session mode): print error to stderr, exit 1
- Malformed state file: print warning to stderr, treat as empty (matches load-control.py graceful degradation pattern)
- Malformed holidays file (full mode): print warning to stderr, treat as empty (no holiday events)
- stdout: print summary line (e.g. "Written N event(s) to <path>")

### 2. Create `.cowork/scripts/test_ics_export.py`

Test classes following the pattern from `test_load_control.py`:

| Test class | What it covers |
|---|---|
| `TestFold` | Short line unchanged; exactly 75 octets unchanged; long ASCII line folded at 75 octets; long UTF-8 line folded without mid-character split; continuation lines start with SPACE |
| `TestBuildVevent` | Correct DTSTART/DTEND/SUMMARY/DESCRIPTION/UID fields; BEGIN/END wrapping; DESCRIPTION with Japanese text (multi-byte UTF-8) folds correctly |
| `TestBuildVcalendar` | VCALENDAR header (VERSION, PRODID, CALSCALE); correct wrapping of multiple events |
| `TestLoadSessionPoints` | Only requested keys appear; keys not in state are silently skipped; grouping by date is correct |
| `TestLoadFullPoints` | Only future dates appear; overdue (next_review < today) excluded; entries without next_review skipped |
| `TestLoadHolidays` | Future holidays returned; past holidays excluded; missing file returns empty list |
| `TestSessionMode` | End-to-end via subprocess: pipe keys, verify .ics output contains correct events |
| `TestFullMode` | End-to-end via subprocess: verify review + holiday events, only future dates |
| `TestOutputFormat` | CRLF line endings throughout; starts with BEGIN:VCALENDAR; ends with END:VCALENDAR followed by CRLF |
| `TestErrorHandling` | Missing state file (session mode) exits 1; empty stdin exits 1; malformed JSON exits 1 |
| `TestEmptyInputs` | Session mode with no matching keys: valid .ics with zero events; full mode with empty state: valid .ics with zero events |

### 3. Update `practice-grammar.md` -- replace inline Python block

Replace lines 672-738 (the `python` fenced code block) with a shell invocation:

```
Run the following shell command (substitute SESSION_IDS with the actual JSON array of grammar point keys from this session). Use `datetime.now().strftime("%Y%m%dT%H%M%S")` for SESSION_TS to avoid same-day filename collisions:

\`\`\`bash
echo '<SESSION_IDS_JSON_ARRAY>' | python3 .cowork/scripts/ics-export.py \
  --mode session \
  --state .cowork/progress/grammar-state.json \
  --output "<VAULT_ROOT>/japanese-grammar-review-<SESSION_TS>.ics"
\`\`\`

Note: `--today` is not passed in session mode (it is ignored — session mode exports all requested keys regardless of date).
```

Keep the surrounding context lines (660-671 rules, 740-741 confirmation message) intact. The confirmation line (740) stays as-is since the script prints the same summary to stdout.

File paths involved: `.cowork/skills/practice-grammar.md` lines 670-738

### 4. Update `manage-holidays.md` -- replace inline Python block

Replace lines 172-269 (the "Use the following Python code" paragraph plus the fenced code block) with:

```
Run the following shell command (VAULT_ROOT and SESSION_TS are substituted by Claude at runtime). Use `datetime.now().strftime("%Y%m%dT%H%M%S")` for SESSION_TS:

\`\`\`bash
python3 .cowork/scripts/ics-export.py \
  --mode full \
  --state .cowork/progress/grammar-state.json \
  --holidays .cowork/progress/holidays.json \
  --output "<VAULT_ROOT>/japanese-grammar-full-calendar-<SESSION_TS>.ics" \
  --today <TODAY_ISO>
\`\`\`
```

Keep the surrounding steps (1-5 above the code, step 7 Report below) intact.

File paths involved: `.cowork/skills/manage-holidays.md` lines 172-269

### 5. Run tests

Execute `python3 -m pytest .cowork/scripts/test_ics_export.py -v` to verify all tests pass.

### 6. Verify skill invocations

Manually trace through both skill files to confirm:
- The shell command templates reference the correct script path
- The argument names match the script's argparse definitions
- stdin piping is correct for session mode
- Full mode does not read stdin

## Risks

- **SUMMARY separator inconsistency**: The two inline blocks currently use different separators (`--` vs ` -- `). Standardizing to ` -- ` changes the calendar event text for one mode. Low risk -- cosmetic only, no downstream parsing depends on this.
- **UUID determinism in tests**: The script uses `uuid.uuid4()` for UIDs. Tests that verify exact UID format need to use regex matching rather than exact string comparison.
- **fold() behavior edge case**: The current `errors="ignore"` approach in `fold()` could theoretically drop bytes on malformed UTF-8 input. This is carried over from the existing code and is acceptable for grammar header strings which are always valid UTF-8.
- **No risk to plugin data**: This change does not touch lesson files, `# Summary` sections, `<!--ID:-->` lines, or `TARGET DECK` lines. The script only reads `grammar-state.json` and `holidays.json`, and writes a new `.ics` file.
