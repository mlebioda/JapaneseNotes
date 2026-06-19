#!/usr/bin/env python3
"""
Tests for ics-export.py — ICS calendar export for grammar reviews.

TDD: these tests are written before the script exists.
Run: python3 -m pytest test_ics_export.py -v
  or: python3 test_ics_export.py
"""

import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

# Import ics-export.py despite the hyphen in filename
_script_dir = Path(__file__).parent
_script_path = _script_dir / "ics-export.py"

ics = None
if _script_path.exists():
    _spec = importlib.util.spec_from_file_location("ics_export", _script_path)
    ics = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(ics)


def _require_module(test_self):
    """Skip a test if the ics-export module is not available."""
    if ics is None:
        test_self.skipTest("ics-export.py does not exist yet (TDD: write script first)")


def _make_state(grammar_points: dict) -> dict:
    """Helper to build a minimal grammar-state.json structure."""
    return {"grammar_points": grammar_points}


def _write_json(path: str, data) -> None:
    """Write JSON data to a file."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


# ---------------------------------------------------------------------------
# 1. TestFold
# ---------------------------------------------------------------------------
class TestFold(unittest.TestCase):
    """RFC 5545 line folding: max 75 octets per line."""

    def test_short_line_unchanged(self):
        """A line shorter than 75 octets passes through unchanged."""
        _require_module(self)
        line = "SUMMARY:Short line"
        self.assertEqual(ics.fold(line), line)

    def test_exactly_75_octets_unchanged(self):
        """A line of exactly 75 octets is not folded."""
        _require_module(self)
        line = "X" * 75
        self.assertEqual(len(line.encode("utf-8")), 75)
        self.assertEqual(ics.fold(line), line)

    def test_long_ascii_folded(self):
        """A long ASCII line is folded at 75-octet boundaries."""
        _require_module(self)
        line = "DESCRIPTION:" + "A" * 200
        folded = ics.fold(line)
        parts = folded.split("\r\n")
        # First part: max 75 octets
        self.assertLessEqual(len(parts[0].encode("utf-8")), 75)
        # Continuation parts start with SPACE and are max 75 octets each
        for part in parts[1:]:
            self.assertTrue(part.startswith(" "), f"Continuation line must start with SPACE: {part!r}")
            self.assertLessEqual(len(part.encode("utf-8")), 75)

    def test_long_utf8_no_mid_char_split(self):
        """A long line with multi-byte UTF-8 chars folds without splitting mid-character."""
        _require_module(self)
        # Each Japanese char is 3 bytes in UTF-8
        line = "DESCRIPTION:" + "文法" * 50  # 300 bytes of kanji
        folded = ics.fold(line)
        parts = folded.split("\r\n")
        for part in parts:
            # Each part must be valid UTF-8 (no truncated bytes)
            try:
                part.encode("utf-8").decode("utf-8")
            except UnicodeDecodeError:
                self.fail(f"Fold produced invalid UTF-8: {part!r}")
            self.assertLessEqual(len(part.encode("utf-8")), 75)

    def test_continuation_lines_start_with_space(self):
        """All continuation lines (after the first) start with a single SPACE character."""
        _require_module(self)
        line = "SUMMARY:" + "B" * 200
        folded = ics.fold(line)
        parts = folded.split("\r\n")
        self.assertGreater(len(parts), 1, "Line should have been folded")
        for part in parts[1:]:
            self.assertTrue(part[0] == " ", f"Expected SPACE prefix, got: {part[0]!r}")
            # The second character should NOT be a space (only one space prefix)
            if len(part) > 1:
                self.assertNotEqual(part[1], " ", "Should be single SPACE prefix, not double")


# ---------------------------------------------------------------------------
# 2. TestBuildVevent
# ---------------------------------------------------------------------------
class TestBuildVevent(unittest.TestCase):
    """VEVENT block construction."""

    def test_correct_fields(self):
        """VEVENT contains DTSTART, DTEND, SUMMARY, DESCRIPTION, UID."""
        _require_module(self)
        lines = ics.build_vevent(
            dtstart="20260620",
            dtend="20260621",
            summary="Japanese Grammar Review — 3 point(s)",
            description="Point A\\nPoint B\\nPoint C",
            uid="20260620-session-abcd1234@japanese-notes",
        )
        joined = "\r\n".join(lines)
        self.assertIn("DTSTART;VALUE=DATE:20260620", joined)
        self.assertIn("DTEND;VALUE=DATE:20260621", joined)
        self.assertIn("SUMMARY:Japanese Grammar Review — 3 point(s)", joined)
        self.assertIn("DESCRIPTION:Point A\\nPoint B\\nPoint C", joined)
        self.assertIn("UID:20260620-session-abcd1234@japanese-notes", joined)

    def test_begin_end_wrapping(self):
        """VEVENT is wrapped with BEGIN:VEVENT and END:VEVENT."""
        _require_module(self)
        lines = ics.build_vevent(
            dtstart="20260620",
            dtend="20260621",
            summary="Test",
            description="Desc",
            uid="test-uid@japanese-notes",
        )
        self.assertEqual(lines[0], "BEGIN:VEVENT")
        self.assertEqual(lines[-1], "END:VEVENT")

    def test_japanese_description(self):
        """DESCRIPTION with Japanese text is accepted (multi-byte UTF-8)."""
        _require_module(self)
        lines = ics.build_vevent(
            dtstart="20260620",
            dtend="20260621",
            summary="Review",
            description="文法の練習\\n動詞の活用",
            uid="test-jp@japanese-notes",
        )
        joined = "\r\n".join(lines)
        self.assertIn("DESCRIPTION:文法の練習", joined)


# ---------------------------------------------------------------------------
# 3. TestBuildVcalendar
# ---------------------------------------------------------------------------
class TestBuildVcalendar(unittest.TestCase):
    """VCALENDAR wrapping."""

    def test_header_fields(self):
        """VCALENDAR contains VERSION, PRODID, CALSCALE."""
        _require_module(self)
        lines = ics.build_vcalendar([])
        joined = "\r\n".join(lines)
        self.assertIn("VERSION:2.0", joined)
        self.assertIn("PRODID:", joined)
        self.assertIn("CALSCALE:GREGORIAN", joined)

    def test_wrapping_multiple_events(self):
        """Multiple VEVENT blocks are wrapped correctly."""
        _require_module(self)
        event1 = ics.build_vevent("20260620", "20260621", "S1", "D1", "u1@jn")
        event2 = ics.build_vevent("20260622", "20260623", "S2", "D2", "u2@jn")
        lines = ics.build_vcalendar([event1, event2])
        self.assertEqual(lines[0], "BEGIN:VCALENDAR")
        self.assertEqual(lines[-1], "END:VCALENDAR")
        # Both events should be present
        joined = "\r\n".join(lines)
        self.assertIn("DTSTART;VALUE=DATE:20260620", joined)
        self.assertIn("DTSTART;VALUE=DATE:20260622", joined)
        # Count BEGIN:VEVENT occurrences
        self.assertEqual(joined.count("BEGIN:VEVENT"), 2)


# ---------------------------------------------------------------------------
# 4. TestLoadSessionPoints
# ---------------------------------------------------------------------------
class TestLoadSessionPoints(unittest.TestCase):
    """load_session_points: filter by keys, group by next_review date."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.state_path = os.path.join(self.tmpdir, "grammar-state.json")
        state = _make_state({
            "key-A": {
                "grammar_header": "Point A",
                "next_review": "2026-06-20",
                "interval_days": 3,
            },
            "key-B": {
                "grammar_header": "Point B",
                "next_review": "2026-06-20",
                "interval_days": 5,
            },
            "key-C": {
                "grammar_header": "Point C",
                "next_review": "2026-06-25",
                "interval_days": 7,
            },
            "key-D": {
                "grammar_header": "Point D",
                "next_review": "2026-06-22",
                "interval_days": 2,
            },
        })
        _write_json(self.state_path, state)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_only_matching_keys(self):
        """Only requested keys appear in result."""
        _require_module(self)
        result = ics.load_session_points(self.state_path, ["key-A", "key-C"])
        # Flatten all headers across all dates
        all_headers = []
        for headers in result.values():
            all_headers.extend(headers)
        self.assertIn("Point A", all_headers)
        self.assertIn("Point C", all_headers)
        self.assertNotIn("Point B", all_headers)
        self.assertNotIn("Point D", all_headers)

    def test_missing_keys_skipped(self):
        """Keys not in state are silently skipped."""
        _require_module(self)
        result = ics.load_session_points(self.state_path, ["key-A", "nonexistent-key"])
        all_headers = []
        for headers in result.values():
            all_headers.extend(headers)
        self.assertEqual(len(all_headers), 1)
        self.assertIn("Point A", all_headers)

    def test_grouped_by_date(self):
        """Points are grouped by their next_review date."""
        _require_module(self)
        result = ics.load_session_points(self.state_path, ["key-A", "key-B", "key-C"])
        # key-A and key-B both have next_review 2026-06-20
        self.assertIn("2026-06-20", result)
        self.assertEqual(len(result["2026-06-20"]), 2)
        # key-C has next_review 2026-06-25
        self.assertIn("2026-06-25", result)
        self.assertEqual(len(result["2026-06-25"]), 1)


# ---------------------------------------------------------------------------
# 5. TestLoadFullPoints
# ---------------------------------------------------------------------------
class TestLoadFullPoints(unittest.TestCase):
    """load_full_points: filter to future dates, group by date."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.state_path = os.path.join(self.tmpdir, "grammar-state.json")
        state = _make_state({
            "future-1": {
                "grammar_header": "Future Point 1",
                "next_review": "2026-06-25",
            },
            "future-2": {
                "grammar_header": "Future Point 2",
                "next_review": "2026-07-01",
            },
            "today": {
                "grammar_header": "Today Point",
                "next_review": "2026-06-19",
            },
            "overdue": {
                "grammar_header": "Overdue Point",
                "next_review": "2026-06-10",
            },
            "no-review": {
                "grammar_header": "No Review Date",
                # no next_review field
            },
        })
        _write_json(self.state_path, state)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_only_future_dates(self):
        """Only entries with next_review >= today appear."""
        _require_module(self)
        result = ics.load_full_points(self.state_path, "2026-06-19")
        all_headers = []
        for headers in result.values():
            all_headers.extend(headers)
        self.assertIn("Future Point 1", all_headers)
        self.assertIn("Future Point 2", all_headers)
        self.assertIn("Today Point", all_headers)

    def test_overdue_excluded(self):
        """Entries with next_review < today are excluded."""
        _require_module(self)
        result = ics.load_full_points(self.state_path, "2026-06-19")
        all_headers = []
        for headers in result.values():
            all_headers.extend(headers)
        self.assertNotIn("Overdue Point", all_headers)

    def test_missing_next_review_skipped(self):
        """Entries without a next_review field are skipped."""
        _require_module(self)
        result = ics.load_full_points(self.state_path, "2026-06-19")
        all_headers = []
        for headers in result.values():
            all_headers.extend(headers)
        self.assertNotIn("No Review Date", all_headers)


# ---------------------------------------------------------------------------
# 6. TestLoadHolidays
# ---------------------------------------------------------------------------
class TestLoadHolidays(unittest.TestCase):
    """load_holidays: filter to future dates, sorted."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_future_holidays_returned(self):
        """Future holidays are returned in sorted order."""
        _require_module(self)
        holidays_path = os.path.join(self.tmpdir, "holidays.json")
        _write_json(holidays_path, ["2026-07-04", "2026-12-25", "2026-06-25"])
        result = ics.load_holidays(holidays_path, "2026-06-19")
        self.assertEqual(result, ["2026-06-25", "2026-07-04", "2026-12-25"])

    def test_past_holidays_excluded(self):
        """Past holidays are excluded."""
        _require_module(self)
        holidays_path = os.path.join(self.tmpdir, "holidays.json")
        _write_json(holidays_path, ["2026-01-01", "2026-06-10", "2026-07-04"])
        result = ics.load_holidays(holidays_path, "2026-06-19")
        self.assertEqual(result, ["2026-07-04"])

    def test_missing_file_returns_empty(self):
        """Missing holidays file returns an empty list."""
        _require_module(self)
        nonexistent = os.path.join(self.tmpdir, "no-such-file.json")
        result = ics.load_holidays(nonexistent, "2026-06-19")
        self.assertEqual(result, [])


# ---------------------------------------------------------------------------
# 7. TestSessionMode
# ---------------------------------------------------------------------------
class TestSessionMode(unittest.TestCase):
    """End-to-end session mode via subprocess."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.state_path = os.path.join(self.tmpdir, "grammar-state.json")
        self.output_path = os.path.join(self.tmpdir, "output.ics")
        state = _make_state({
            "key-A": {
                "grammar_header": "Point A",
                "next_review": "2026-06-20",
            },
            "key-B": {
                "grammar_header": "Point B",
                "next_review": "2026-06-20",
            },
            "key-C": {
                "grammar_header": "Point C",
                "next_review": "2026-06-25",
            },
        })
        _write_json(self.state_path, state)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_session_mode_e2e(self):
        """Pipe keys via stdin, verify .ics file has correct events."""
        script = str(_script_dir / "ics-export.py")
        keys = json.dumps(["key-A", "key-B", "key-C"])
        result = subprocess.run(
            [
                sys.executable, script,
                "--mode", "session",
                "--state", self.state_path,
                "--output", self.output_path,
            ],
            input=keys,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, f"stderr: {result.stderr}")
        self.assertTrue(os.path.exists(self.output_path))

        with open(self.output_path, "rb") as f:
            content = f.read().decode("utf-8")

        # Should have VCALENDAR wrapping
        self.assertIn("BEGIN:VCALENDAR", content)
        self.assertIn("END:VCALENDAR", content)
        # Should have 2 VEVENTs (grouped by date: 2 keys on 06-20, 1 key on 06-25)
        self.assertEqual(content.count("BEGIN:VEVENT"), 2)
        # Check SUMMARY contains em dash and point count
        self.assertIn("Japanese Grammar Review —", content)

    def test_session_mode_today_flag_ignored(self):
        """--today is accepted but ignored in session mode (all keys exported)."""
        script = str(_script_dir / "ics-export.py")
        keys = json.dumps(["key-C"])  # next_review = 2026-06-25
        result = subprocess.run(
            [
                sys.executable, script,
                "--mode", "session",
                "--state", self.state_path,
                "--output", self.output_path,
                "--today", "2026-07-01",  # after key-C's date, but should be ignored
            ],
            input=keys,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, f"stderr: {result.stderr}")
        with open(self.output_path, "rb") as f:
            content = f.read().decode("utf-8")
        # key-C should still be exported even though --today is after its review date
        self.assertEqual(content.count("BEGIN:VEVENT"), 1)


# ---------------------------------------------------------------------------
# 8. TestFullMode
# ---------------------------------------------------------------------------
class TestFullMode(unittest.TestCase):
    """End-to-end full mode via subprocess."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.state_path = os.path.join(self.tmpdir, "grammar-state.json")
        self.holidays_path = os.path.join(self.tmpdir, "holidays.json")
        self.output_path = os.path.join(self.tmpdir, "output.ics")
        state = _make_state({
            "future-1": {
                "grammar_header": "Future Point 1",
                "next_review": "2026-06-25",
            },
            "future-2": {
                "grammar_header": "Future Point 2",
                "next_review": "2026-07-01",
            },
            "overdue": {
                "grammar_header": "Overdue",
                "next_review": "2026-06-10",
            },
        })
        _write_json(self.state_path, state)
        _write_json(self.holidays_path, ["2026-06-28", "2026-01-01"])

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_full_mode_e2e(self):
        """Full mode exports review + holiday events, only future dates."""
        script = str(_script_dir / "ics-export.py")
        result = subprocess.run(
            [
                sys.executable, script,
                "--mode", "full",
                "--state", self.state_path,
                "--holidays", self.holidays_path,
                "--output", self.output_path,
                "--today", "2026-06-19",
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, f"stderr: {result.stderr}")
        self.assertTrue(os.path.exists(self.output_path))

        with open(self.output_path, "rb") as f:
            content = f.read().decode("utf-8")

        # 2 review events (future-1 on 06-25, future-2 on 07-01) + 1 holiday (06-28)
        # overdue (06-10) excluded, past holiday (01-01) excluded
        self.assertEqual(content.count("BEGIN:VEVENT"), 3)
        self.assertIn("Holiday — No Review", content)
        self.assertNotIn("Overdue", content)

    def test_full_mode_missing_state_no_exit(self):
        """Full mode with missing state file: no exit 1, just empty review events."""
        script = str(_script_dir / "ics-export.py")
        nonexistent_state = os.path.join(self.tmpdir, "no-state.json")
        result = subprocess.run(
            [
                sys.executable, script,
                "--mode", "full",
                "--state", nonexistent_state,
                "--holidays", self.holidays_path,
                "--output", self.output_path,
                "--today", "2026-06-19",
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, f"stderr: {result.stderr}")
        with open(self.output_path, "rb") as f:
            content = f.read().decode("utf-8")
        # Only holiday event (06-28), no review events
        self.assertEqual(content.count("BEGIN:VEVENT"), 1)
        self.assertIn("Holiday", content)


# ---------------------------------------------------------------------------
# 9. TestOutputFormat
# ---------------------------------------------------------------------------
class TestOutputFormat(unittest.TestCase):
    """Output file format: CRLF line endings, VCALENDAR wrapping."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.state_path = os.path.join(self.tmpdir, "grammar-state.json")
        self.output_path = os.path.join(self.tmpdir, "output.ics")
        state = _make_state({
            "key-A": {
                "grammar_header": "Point A",
                "next_review": "2026-06-20",
            },
        })
        _write_json(self.state_path, state)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_crlf_line_endings(self):
        """Output file uses CRLF (\\r\\n) line endings throughout."""
        script = str(_script_dir / "ics-export.py")
        result = subprocess.run(
            [
                sys.executable, script,
                "--mode", "session",
                "--state", self.state_path,
                "--output", self.output_path,
            ],
            input=json.dumps(["key-A"]),
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, f"stderr: {result.stderr}")

        with open(self.output_path, "rb") as f:
            raw = f.read()

        # Every line ending should be CRLF
        # Remove all \r\n, then check no stray \n remains
        stripped = raw.replace(b"\r\n", b"")
        self.assertNotIn(b"\n", stripped, "Found bare LF without preceding CR")
        self.assertNotIn(b"\r", stripped, "Found bare CR without following LF")

    def test_starts_with_begin_vcalendar(self):
        """Output starts with BEGIN:VCALENDAR."""
        script = str(_script_dir / "ics-export.py")
        result = subprocess.run(
            [
                sys.executable, script,
                "--mode", "session",
                "--state", self.state_path,
                "--output", self.output_path,
            ],
            input=json.dumps(["key-A"]),
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)

        with open(self.output_path, "rb") as f:
            raw = f.read()
        self.assertTrue(raw.startswith(b"BEGIN:VCALENDAR\r\n"))

    def test_ends_with_end_vcalendar(self):
        """Output ends with END:VCALENDAR followed by CRLF."""
        script = str(_script_dir / "ics-export.py")
        result = subprocess.run(
            [
                sys.executable, script,
                "--mode", "session",
                "--state", self.state_path,
                "--output", self.output_path,
            ],
            input=json.dumps(["key-A"]),
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)

        with open(self.output_path, "rb") as f:
            raw = f.read()
        self.assertTrue(raw.endswith(b"END:VCALENDAR\r\n"))


# ---------------------------------------------------------------------------
# 10. TestErrorHandling
# ---------------------------------------------------------------------------
class TestErrorHandling(unittest.TestCase):
    """Error conditions that should exit 1."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_missing_state_session_exits_1(self):
        """Session mode with missing state file exits 1."""
        script = str(_script_dir / "ics-export.py")
        nonexistent = os.path.join(self.tmpdir, "no-state.json")
        output = os.path.join(self.tmpdir, "output.ics")
        result = subprocess.run(
            [
                sys.executable, script,
                "--mode", "session",
                "--state", nonexistent,
                "--output", output,
            ],
            input=json.dumps(["key-A"]),
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 1)
        self.assertTrue(len(result.stderr) > 0, "Should print error to stderr")

    def test_empty_stdin_exits_1(self):
        """Session mode with empty stdin exits 1."""
        script = str(_script_dir / "ics-export.py")
        state_path = os.path.join(self.tmpdir, "grammar-state.json")
        _write_json(state_path, _make_state({}))
        output = os.path.join(self.tmpdir, "output.ics")
        result = subprocess.run(
            [
                sys.executable, script,
                "--mode", "session",
                "--state", state_path,
                "--output", output,
            ],
            input="",
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("No keys provided", result.stderr)

    def test_malformed_stdin_json_exits_1(self):
        """Session mode with malformed JSON on stdin exits 1."""
        script = str(_script_dir / "ics-export.py")
        state_path = os.path.join(self.tmpdir, "grammar-state.json")
        _write_json(state_path, _make_state({}))
        output = os.path.join(self.tmpdir, "output.ics")
        result = subprocess.run(
            [
                sys.executable, script,
                "--mode", "session",
                "--state", state_path,
                "--output", output,
            ],
            input="this is not valid json {{{",
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 1)
        self.assertTrue(len(result.stderr) > 0)

    def test_malformed_state_session_exits_1(self):
        """Session mode with malformed state JSON exits 1 (not graceful -- session needs state)."""
        script = str(_script_dir / "ics-export.py")
        state_path = os.path.join(self.tmpdir, "grammar-state.json")
        with open(state_path, "w") as f:
            f.write("not valid json {{{")
        output = os.path.join(self.tmpdir, "output.ics")
        result = subprocess.run(
            [
                sys.executable, script,
                "--mode", "session",
                "--state", state_path,
                "--output", output,
            ],
            input=json.dumps(["key-A"]),
            capture_output=True,
            text=True,
        )
        # Session mode requires valid state -- exit 1
        self.assertEqual(result.returncode, 1)

    def test_malformed_state_full_graceful(self):
        """Full mode with malformed state: graceful degradation, warning, NOT exit 1."""
        script = str(_script_dir / "ics-export.py")
        state_path = os.path.join(self.tmpdir, "grammar-state.json")
        with open(state_path, "w") as f:
            f.write("not valid json {{{")
        output = os.path.join(self.tmpdir, "output.ics")
        result = subprocess.run(
            [
                sys.executable, script,
                "--mode", "full",
                "--state", state_path,
                "--output", output,
                "--today", "2026-06-19",
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, f"stderr: {result.stderr}")
        self.assertIn("Warning", result.stderr)
        # Should produce valid empty ICS
        self.assertTrue(os.path.exists(output))

    def test_malformed_holidays_full_graceful(self):
        """Full mode with malformed holidays: graceful degradation, warning, NOT exit 1."""
        script = str(_script_dir / "ics-export.py")
        state_path = os.path.join(self.tmpdir, "grammar-state.json")
        _write_json(state_path, _make_state({}))
        holidays_path = os.path.join(self.tmpdir, "holidays.json")
        with open(holidays_path, "w") as f:
            f.write("not valid json {{{")
        output = os.path.join(self.tmpdir, "output.ics")
        result = subprocess.run(
            [
                sys.executable, script,
                "--mode", "full",
                "--state", state_path,
                "--holidays", holidays_path,
                "--output", output,
                "--today", "2026-06-19",
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, f"stderr: {result.stderr}")
        self.assertIn("Warning", result.stderr)


# ---------------------------------------------------------------------------
# 11. TestEmptyInputs
# ---------------------------------------------------------------------------
class TestEmptyInputs(unittest.TestCase):
    """Empty but valid inputs produce valid empty ICS files."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_session_no_matching_keys(self):
        """Session mode: keys provided but none match state -- valid ICS with 0 events."""
        script = str(_script_dir / "ics-export.py")
        state_path = os.path.join(self.tmpdir, "grammar-state.json")
        _write_json(state_path, _make_state({
            "existing-key": {
                "grammar_header": "Existing",
                "next_review": "2026-06-20",
            },
        }))
        output = os.path.join(self.tmpdir, "output.ics")
        result = subprocess.run(
            [
                sys.executable, script,
                "--mode", "session",
                "--state", state_path,
                "--output", output,
            ],
            input=json.dumps(["no-match-1", "no-match-2"]),
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, f"stderr: {result.stderr}")

        with open(output, "rb") as f:
            content = f.read().decode("utf-8")
        self.assertIn("BEGIN:VCALENDAR", content)
        self.assertIn("END:VCALENDAR", content)
        self.assertEqual(content.count("BEGIN:VEVENT"), 0)

    def test_full_mode_empty_state(self):
        """Full mode: empty grammar_points -- valid ICS with 0 review events."""
        script = str(_script_dir / "ics-export.py")
        state_path = os.path.join(self.tmpdir, "grammar-state.json")
        _write_json(state_path, _make_state({}))
        holidays_path = os.path.join(self.tmpdir, "empty-holidays.json")
        _write_json(holidays_path, [])
        output = os.path.join(self.tmpdir, "output.ics")
        result = subprocess.run(
            [
                sys.executable, script,
                "--mode", "full",
                "--state", state_path,
                "--holidays", holidays_path,
                "--output", output,
                "--today", "2026-06-19",
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, f"stderr: {result.stderr}")

        with open(output, "rb") as f:
            content = f.read().decode("utf-8")
        self.assertIn("BEGIN:VCALENDAR", content)
        self.assertIn("END:VCALENDAR", content)
        self.assertEqual(content.count("BEGIN:VEVENT"), 0)

    def test_full_mode_all_overdue(self):
        """Full mode: all points overdue -- valid ICS with 0 review events."""
        script = str(_script_dir / "ics-export.py")
        state_path = os.path.join(self.tmpdir, "grammar-state.json")
        _write_json(state_path, _make_state({
            "old-1": {
                "grammar_header": "Old Point",
                "next_review": "2026-01-01",
            },
        }))
        holidays_path = os.path.join(self.tmpdir, "empty-holidays.json")
        _write_json(holidays_path, [])
        output = os.path.join(self.tmpdir, "output.ics")
        result = subprocess.run(
            [
                sys.executable, script,
                "--mode", "full",
                "--state", state_path,
                "--holidays", holidays_path,
                "--output", output,
                "--today", "2026-06-19",
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, f"stderr: {result.stderr}")

        with open(output, "rb") as f:
            content = f.read().decode("utf-8")
        self.assertEqual(content.count("BEGIN:VEVENT"), 0)


if __name__ == "__main__":
    unittest.main()
