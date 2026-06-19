# ICS Export Extraction -- Tasks

- [x] Create `.cowork/scripts/ics-export.py` with argparse CLI (`--mode session|full`, `--state`, `--holidays`, `--output`, `--today`)
- [x] Implement `fold(line)` -- RFC 5545 line folding (max 75 octets, SPACE continuation prefix)
- [x] Implement `build_vevent(dtstart, dtend, summary, description, uid)` -- returns VEVENT line list
- [x] Implement `build_vcalendar(events)` -- wraps events in VCALENDAR header/footer
- [x] Implement `load_session_points(state_path, keys)` -- filter state by keys, group by date
- [x] Implement `load_full_points(state_path, today)` -- filter state to future dates, group by date
- [x] Implement `load_holidays(holidays_path, today)` -- filter holidays to future dates
- [x] Implement `write_ics(path, lines)` -- fold + CRLF line endings
- [x] Implement `main()` -- argparse, mode dispatch, stdin reading, stdout summary
- [x] Create `.cowork/scripts/test_ics_export.py` with all test classes (TestFold, TestBuildVevent, TestBuildVcalendar, TestLoadSessionPoints, TestLoadFullPoints, TestLoadHolidays, TestSessionMode, TestFullMode, TestOutputFormat, TestErrorHandling, TestEmptyInputs)
- [x] Run tests -- verify all pass
- [x] Update `practice-grammar.md` -- replace inline Python block (lines 670-738) with shell invocation of `ics-export.py --mode session`. No `--today` flag. Use `datetime.now()` for SESSION_TS. Verify correct script path and arguments.
- [x] Update `manage-holidays.md` -- replace inline Python block (lines 172-269) with shell invocation of `ics-export.py --mode full`. Use `datetime.now()` for SESSION_TS. Remove stale "same fold() function" comment. Verify correct script path and arguments.
