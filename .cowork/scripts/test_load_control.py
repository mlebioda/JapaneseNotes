#!/usr/bin/env python3
"""
Tests for load-control.py — SRS date placement logic.

Run: python3 -m pytest test_load_control.py -v
  or: python3 test_load_control.py
"""

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

# Import load-control.py despite the hyphen in filename
_script_dir = Path(__file__).parent
_spec = importlib.util.spec_from_file_location(
    "load_control", _script_dir / "load-control.py"
)
lc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lc)


def make_topic(key, interval_days=5, score=3, **kwargs):
    """Helper to build a topic dict."""
    t = {
        "key": key,
        "lesson_file": "JPLessons/Udemy/N4/Grammar/UN4GL5.md",
        "grammar_header": f"Header for {key}",
        "last_reviewed": "2026-06-18",
        "score": score,
        "interval_days": interval_days,
        "ease": 2.5,
        "streak": 2,
        "total_reviews": 3,
        "weak_points": [],
    }
    t.update(kwargs)
    return t


class TestBasicPlacement(unittest.TestCase):
    """Topic lands on a day with room — no shift."""

    def test_basic_no_shift(self):
        today = date(2026, 6, 18)  # Thursday
        topics = [make_topic("t1", interval_days=3, score=3)]
        # 2026-06-21 is Sunday — not blocked, no existing load
        results = lc.place_topics(topics, {}, today)
        self.assertEqual(len(results), 1)
        placed = results[0][1]
        self.assertEqual(placed, date(2026, 6, 21))
        # No shift
        self.assertIsNone(results[0][2])


class TestSaturdaySkip(unittest.TestCase):
    """Raw date is Saturday — shifted to next valid day."""

    def test_saturday_skipped(self):
        # 2026-06-18 is Thursday. interval=2 → candidate 2026-06-20 = Saturday
        today = date(2026, 6, 18)
        topics = [make_topic("t1", interval_days=2, score=3)]
        results = lc.place_topics(topics, {}, today)
        placed = results[0][1]
        # Should skip Saturday, land on Sunday 2026-06-21
        self.assertEqual(placed, date(2026, 6, 21))
        self.assertIsNotNone(results[0][2])  # shifted


class TestDailyCap(unittest.TestCase):
    """Day has 10 topics — shifted forward."""

    def test_daily_cap_shifts(self):
        today = date(2026, 6, 18)
        # Pre-fill 2026-06-21 (Sunday) with 10 existing topics
        gp = {}
        for i in range(10):
            gp[f"existing-{i}"] = {
                "next_review": "2026-06-21",
                "last_score": 3,
            }
        topics = [make_topic("t1", interval_days=3, score=3)]
        # candidate = 2026-06-21, but that's full
        results = lc.place_topics(topics, gp, today)
        placed = results[0][1]
        # Should be shifted past 2026-06-21
        self.assertGreater(placed, date(2026, 6, 21))
        self.assertNotEqual(placed.weekday(), 5)  # not Saturday


class TestWeakCap(unittest.TestCase):
    """Day has 4 weak topics (score 1 or 2), new weak topic — shifted forward."""

    def test_weak_cap_shifts_weak_topic(self):
        today = date(2026, 6, 18)
        # Pre-fill 2026-06-21 with 4 weak entries (last_score=2, total < 10)
        gp = {}
        for i in range(4):
            gp[f"weak-{i}"] = {
                "next_review": "2026-06-21",
                "last_score": 2,
            }
        topics = [make_topic("t1", interval_days=3, score=2)]
        results = lc.place_topics(topics, gp, today)
        placed = results[0][1]
        # Weak cap hit, should shift
        self.assertGreater(placed, date(2026, 6, 21))


class TestWeakCapNotAppliedToStrong(unittest.TestCase):
    """Day has 4 weak topics, score-3 topic — placed (total < 10)."""

    def test_strong_topic_placed_despite_weak_cap(self):
        today = date(2026, 6, 18)
        gp = {}
        for i in range(4):
            gp[f"weak-{i}"] = {
                "next_review": "2026-06-21",
                "last_score": 2,
            }
        topics = [make_topic("t1", interval_days=3, score=3)]
        results = lc.place_topics(topics, gp, today)
        placed = results[0][1]
        # Total is 4 < 10, and score=3 is not weak, so placed
        self.assertEqual(placed, date(2026, 6, 21))


class TestPriorityOrdering(unittest.TestCase):
    """Score-1 topics placed before score-3 — weak slots filled first."""

    def test_weak_placed_first(self):
        today = date(2026, 6, 18)
        # 3 weak slots available on 2026-06-21
        gp = {
            "existing-weak": {
                "next_review": "2026-06-21",
                "last_score": 1,
            }
        }
        # Submit: one score-3, one score-1, both aiming at 2026-06-21
        topics = [
            make_topic("strong", interval_days=3, score=3),
            make_topic("weak", interval_days=3, score=1),
        ]
        results = lc.place_topics(topics, gp, today)

        # Results are ordered by score (sorted): weak first, then strong
        placed_keys = [(r[0]["key"], r[1]) for r in results]
        # The weak topic (score=1) should be placed first in processing order
        self.assertEqual(placed_keys[0][0], "weak")


class TestFallback(unittest.TestCase):
    """All days in 30-day window are full — picks earliest least-loaded non-Saturday."""

    def test_fallback_to_least_loaded(self):
        today = date(2026, 6, 18)
        gp = {}
        # Fill every day in the next 30 days with DAILY_CAP topics
        for offset in range(1, 35):
            d = today + timedelta(days=offset)
            if d.weekday() == 5:  # skip Saturdays (blocked anyway)
                continue
            d_str = d.isoformat()
            for i in range(lc.DAILY_CAP):
                gp[f"fill-{d_str}-{i}"] = {
                    "next_review": d_str,
                    "last_score": 3,
                }

        # But leave one day with only 9 topics (least loaded)
        least_loaded_date = today + timedelta(days=5)
        # If it's Saturday, pick next day
        while least_loaded_date.weekday() == 5:
            least_loaded_date += timedelta(days=1)
        least_loaded_str = least_loaded_date.isoformat()
        # Remove one entry from that day
        key_to_remove = f"fill-{least_loaded_str}-9"
        if key_to_remove in gp:
            del gp[key_to_remove]

        topics = [make_topic("t1", interval_days=3, score=3)]
        results = lc.place_topics(topics, gp, today)
        placed = results[0][1]
        # Should fallback to the least-loaded day
        self.assertEqual(placed, least_loaded_date)


class TestIntervalDaysPreserved(unittest.TestCase):
    """Shifted topic keeps original SM-2 interval_days, only next_review changes."""

    def test_interval_preserved_on_shift(self):
        today = date(2026, 6, 18)
        topics = [make_topic("t1", interval_days=2, score=3)]
        # candidate=Saturday, will shift
        results = lc.place_topics(topics, {}, today)
        topic_out = results[0][0]
        # interval_days should remain 2
        self.assertEqual(topic_out["interval_days"], 2)
        # But next_review (placed date) should not be Saturday
        self.assertNotEqual(results[0][1].weekday(), 5)


class TestMultipleTopicsSameSession(unittest.TestCase):
    """Second topic sees first topic's placement."""

    def test_second_sees_first(self):
        today = date(2026, 6, 18)
        # Both topics aim at same date, daily cap = 10
        # Fill existing to 9
        gp = {}
        target = date(2026, 6, 21)
        target_str = target.isoformat()
        for i in range(9):
            gp[f"existing-{i}"] = {
                "next_review": target_str,
                "last_score": 3,
            }

        topics = [
            make_topic("t1", interval_days=3, score=3),
            make_topic("t2", interval_days=3, score=3),
        ]
        results = lc.place_topics(topics, gp, today)

        dates = [r[1] for r in results]
        # First should land on 2026-06-21 (slot 10 of 10)
        # Second should be shifted (cap reached)
        self.assertEqual(dates[0], target)
        self.assertGreater(dates[1], target)


class TestSaturdayPlusFullSunday(unittest.TestCase):
    """Raw date Saturday, Sunday also full — searches further."""

    def test_saturday_and_full_sunday(self):
        today = date(2026, 6, 18)
        # candidate = 2026-06-20 (Saturday)
        # Sunday 2026-06-21 is full
        gp = {}
        for i in range(lc.DAILY_CAP):
            gp[f"sun-{i}"] = {
                "next_review": "2026-06-21",
                "last_score": 3,
            }

        topics = [make_topic("t1", interval_days=2, score=3)]
        results = lc.place_topics(topics, gp, today)
        placed = results[0][1]
        # Should skip Saturday (blocked) and Sunday (full) → Monday 2026-06-22
        self.assertEqual(placed, date(2026, 6, 22))


class TestExistingJSONPreserved(unittest.TestCase):
    """Topics not in session input remain unchanged in JSON."""

    def test_existing_entries_preserved(self):
        today = date(2026, 6, 18)
        existing_entry = {
            "lesson_file": "JPLessons/test.md",
            "grammar_header": "Existing",
            "next_review": "2026-06-25",
            "interval_days": 7,
            "ease": 2.5,
            "streak": 3,
            "total_reviews": 3,
            "last_score": 4,
            "weak_points": [],
        }
        gp = {"existing::point": existing_entry.copy()}
        state_data = {"grammar_points": gp}

        topics = [make_topic("new::point", interval_days=3, score=3)]
        results = lc.place_topics(topics, gp, today)

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            tmp_path = Path(f.name)

        try:
            lc.merge_and_write(results, gp, tmp_path, state_data)
            with open(tmp_path) as f:
                written = json.load(f)

            # Existing entry should still be there
            self.assertIn("existing::point", written["grammar_points"])
            self.assertEqual(
                written["grammar_points"]["existing::point"]["ease"], 2.5
            )
            # New entry should also be there
            self.assertIn("new::point", written["grammar_points"])
        finally:
            tmp_path.unlink(missing_ok=True)


class TestMinimumCandidateDate(unittest.TestCase):
    """interval_days=0 → candidate becomes today+1, never today."""

    def test_zero_interval_uses_tomorrow(self):
        today = date(2026, 6, 18)  # Thursday
        topics = [make_topic("t1", interval_days=0, score=3)]
        results = lc.place_topics(topics, {}, today)
        placed = results[0][1]
        # Should be at least tomorrow
        self.assertGreaterEqual(placed, today + timedelta(days=1))


class TestCountIncludesToday(unittest.TestCase):
    """Topics already on today in JSON are counted correctly."""

    def test_today_entries_counted(self):
        today = date(2026, 6, 18)
        # Fill today with entries — they should be counted
        gp = {}
        for i in range(lc.DAILY_CAP):
            gp[f"today-{i}"] = {
                "next_review": today.isoformat(),
                "last_score": 3,
            }

        counts = lc.build_day_counts(gp, today)
        self.assertEqual(counts[today.isoformat()]["total"], lc.DAILY_CAP)


class TestErrorHandling(unittest.TestCase):
    """Malformed input → exit 1, missing state file → creates empty."""

    def test_malformed_json_exits_1(self):
        script = str(_script_dir / "load-control.py")
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            tmp_state = f.name
            json.dump({"grammar_points": {}}, f)

        try:
            result = subprocess.run(
                [sys.executable, script, "--state", tmp_state],
                input="not valid json",
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("Error", result.stderr)
        finally:
            os.unlink(tmp_state)

    def test_missing_state_creates_empty(self):
        script = str(_script_dir / "load-control.py")
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = os.path.join(tmpdir, "nonexistent.json")
            topic = make_topic("t1", interval_days=3, score=3)
            result = subprocess.run(
                [
                    sys.executable, script,
                    "--state", state_path,
                    "--today", "2026-06-18",
                ],
                input=json.dumps([topic]),
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0)
            # State file should now exist
            self.assertTrue(os.path.exists(state_path))
            with open(state_path) as f:
                data = json.load(f)
            self.assertIn("t1", data["grammar_points"])

    def test_empty_stdin_exits_1(self):
        script = str(_script_dir / "load-control.py")
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            tmp_state = f.name
            json.dump({"grammar_points": {}}, f)

        try:
            result = subprocess.run(
                [sys.executable, script, "--state", tmp_state],
                input="",
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 1)
        finally:
            os.unlink(tmp_state)

    def test_missing_key_field_exits_1(self):
        script = str(_script_dir / "load-control.py")
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            tmp_state = f.name
            json.dump({"grammar_points": {}}, f)

        try:
            result = subprocess.run(
                [sys.executable, script, "--state", tmp_state],
                input=json.dumps([{"score": 3}]),  # no 'key' field
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("missing 'key'", result.stderr)
        finally:
            os.unlink(tmp_state)


class TestIsBlocked(unittest.TestCase):
    """Verify Saturday detection."""

    def test_saturday_blocked(self):
        # 2026-06-20 is Saturday
        self.assertTrue(lc.is_blocked(date(2026, 6, 20)))

    def test_sunday_not_blocked(self):
        self.assertFalse(lc.is_blocked(date(2026, 6, 21)))

    def test_friday_not_blocked(self):
        self.assertFalse(lc.is_blocked(date(2026, 6, 19)))


class TestLoadRules(unittest.TestCase):
    """Tests for load_rules(): file loading, defaults, and error handling."""

    def test_valid_rules_file(self):
        """A complete JSON rules file loads all values into Config."""
        rules = {
            "DAILY_CAP": 8,
            "WEAK_CAP": 2,
            "BLOCKED_WEEKDAY": 6,
            "SEARCH_WINDOW": 14,
            "holidays_file": ".cowork/progress/my-holidays.json",
        }
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(rules, f)
            tmp_path = f.name

        try:
            config = lc.load_rules(tmp_path)
            self.assertEqual(config.daily_cap, 8)
            self.assertEqual(config.weak_cap, 2)
            self.assertEqual(config.blocked_weekday, 6)
            self.assertEqual(config.search_window, 14)
            self.assertEqual(config.holidays_file, ".cowork/progress/my-holidays.json")
        finally:
            os.unlink(tmp_path)

    def test_missing_file_returns_defaults_with_warning(self):
        """Missing rules file returns Config() defaults and prints warning to stderr."""
        import io
        from contextlib import redirect_stderr

        nonexistent = os.path.join(tempfile.gettempdir(), "no-such-rules-file.json")
        # Ensure it doesn't exist
        if os.path.exists(nonexistent):
            os.unlink(nonexistent)

        captured = io.StringIO()
        with redirect_stderr(captured):
            config = lc.load_rules(nonexistent)

        defaults = lc.Config()
        self.assertEqual(config.daily_cap, defaults.daily_cap)
        self.assertEqual(config.weak_cap, defaults.weak_cap)
        self.assertEqual(config.blocked_weekday, defaults.blocked_weekday)
        self.assertEqual(config.search_window, defaults.search_window)
        self.assertEqual(config.holidays_file, defaults.holidays_file)
        self.assertIn("Warning", captured.getvalue())

    def test_malformed_json_exits_1(self):
        """Malformed JSON in rules file causes sys.exit(1)."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            f.write("this is not valid json {{{")
            tmp_path = f.name

        try:
            with self.assertRaises(SystemExit) as cm:
                lc.load_rules(tmp_path)
            self.assertEqual(cm.exception.code, 1)
        finally:
            os.unlink(tmp_path)

    def test_missing_key_uses_default(self):
        """JSON with only DAILY_CAP — other keys use Config() defaults."""
        rules = {"DAILY_CAP": 15}
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(rules, f)
            tmp_path = f.name

        try:
            config = lc.load_rules(tmp_path)
            defaults = lc.Config()
            # DAILY_CAP was overridden
            self.assertEqual(config.daily_cap, 15)
            # All other keys should be defaults
            self.assertEqual(config.weak_cap, defaults.weak_cap)
            self.assertEqual(config.blocked_weekday, defaults.blocked_weekday)
            self.assertEqual(config.search_window, defaults.search_window)
            self.assertEqual(config.holidays_file, defaults.holidays_file)
        finally:
            os.unlink(tmp_path)


class TestSummaryLineSaturdayShift(unittest.TestCase):
    """Summary line includes ', Saturday' label when raw date is a Saturday."""

    def test_saturday_shift_label(self):
        today = date(2026, 6, 18)  # Thursday
        config = lc.Config()       # blocked_weekday=5 (Saturday)
        # interval=2 → candidate = 2026-06-20 (Saturday) → shifted
        topics = [make_topic("sat-topic", interval_days=2, score=3)]
        results = lc.place_topics(topics, {}, today, config)

        # Confirm the topic was shifted from Saturday
        self.assertIsNotNone(results[0][2])  # raw_date present = shifted
        self.assertEqual(results[0][2], date(2026, 6, 20))  # the Saturday

        # Now call merge_and_write and inspect summary lines
        gp = {}
        state_data = {"grammar_points": gp}
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            tmp_path = Path(f.name)

        try:
            summary = lc.merge_and_write(results, gp, tmp_path, state_data, config)
            self.assertEqual(len(summary), 1)
            self.assertIn("(shifted from 2026-06-20, Saturday)", summary[0])
        finally:
            tmp_path.unlink(missing_ok=True)


class TestSummaryLineHolidayShift(unittest.TestCase):
    """Summary line includes ', holiday' label when raw date is a holiday."""

    def test_holiday_shift_label(self):
        today = date(2026, 6, 18)  # Thursday
        # 2026-06-21 is Sunday — not blocked by weekday, but we mark it as holiday
        holiday_date = date(2026, 6, 21)
        config = lc.Config(holidays={holiday_date})

        # interval=3 → candidate = 2026-06-21 (Sunday, our holiday)
        # is_blocked() blocks holidays, so the topic shifts forward.
        # Capacity fill ensures the shift is recorded as coming from the holiday date.
        gp = {}
        for i in range(lc.DAILY_CAP):
            gp[f"fill-{i}"] = {
                "next_review": "2026-06-21",
                "last_score": 3,
            }

        topics = [make_topic("hol-topic", interval_days=3, score=3)]
        results = lc.place_topics(topics, gp, today, config)

        # The raw_date should be the holiday (2026-06-21) and it was shifted
        self.assertIsNotNone(results[0][2])
        self.assertEqual(results[0][2], holiday_date)

        # Now call merge_and_write — the label should say ', holiday'
        state_data = {"grammar_points": gp}
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            tmp_path = Path(f.name)

        try:
            summary = lc.merge_and_write(results, gp, tmp_path, state_data, config)
            self.assertEqual(len(summary), 1)
            self.assertIn("(shifted from 2026-06-21, holiday)", summary[0])
        finally:
            tmp_path.unlink(missing_ok=True)


class TestSummaryLineCapacityOnlyShift(unittest.TestCase):
    """Summary line has NO trailing label when shift is due to capacity only."""

    def test_capacity_shift_no_label(self):
        today = date(2026, 6, 18)  # Thursday
        config = lc.Config()
        # interval=3 → candidate = 2026-06-21 (Sunday — not Saturday, not holiday)
        # Fill Sunday to capacity so the topic shifts
        gp = {}
        for i in range(lc.DAILY_CAP):
            gp[f"fill-{i}"] = {
                "next_review": "2026-06-21",
                "last_score": 3,
            }

        topics = [make_topic("cap-topic", interval_days=3, score=3)]
        results = lc.place_topics(topics, gp, today, config)

        # The topic was shifted from Sunday (not Sat, not holiday)
        self.assertIsNotNone(results[0][2])
        self.assertEqual(results[0][2], date(2026, 6, 21))  # Sunday

        # merge_and_write should produce label WITHOUT ', Saturday' or ', holiday'
        state_data = {"grammar_points": gp}
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            tmp_path = Path(f.name)

        try:
            summary = lc.merge_and_write(results, gp, tmp_path, state_data, config)
            self.assertEqual(len(summary), 1)
            self.assertIn("(shifted from 2026-06-21)", summary[0])
            self.assertNotIn("Saturday", summary[0])
            self.assertNotIn("holiday", summary[0])
        finally:
            tmp_path.unlink(missing_ok=True)


class TestHolidayBlocked(unittest.TestCase):
    """A date in the holidays set returns is_blocked = True."""

    def test_holiday_date_is_blocked(self):
        # 2026-07-04 is Saturday, pick a non-Saturday holiday to isolate the test
        # 2026-12-25 is Friday
        holiday = date(2026, 12, 25)
        config = lc.Config(holidays={holiday})
        self.assertTrue(lc.is_blocked(holiday, config))

    def test_weekday_holiday_is_blocked(self):
        # 2026-06-23 is Tuesday — not blocked by weekday, but marked holiday
        holiday = date(2026, 6, 23)
        config = lc.Config(holidays={holiday})
        self.assertTrue(lc.is_blocked(holiday, config))


class TestNonHolidayNotBlocked(unittest.TestCase):
    """A regular weekday not in the holidays set returns is_blocked = False."""

    def test_regular_weekday_not_blocked(self):
        # 2026-06-23 is Tuesday — not Saturday, not in holidays
        config = lc.Config(holidays=set())
        self.assertFalse(lc.is_blocked(date(2026, 6, 23), config))

    def test_weekday_with_other_holidays_not_blocked(self):
        # 2026-06-23 is Tuesday, holidays contain other dates but not this one
        config = lc.Config(holidays={date(2026, 12, 25), date(2026, 1, 1)})
        self.assertFalse(lc.is_blocked(date(2026, 6, 23), config))


class TestSaturdayPlusHoliday(unittest.TestCase):
    """Saturday that is also a holiday — still blocked, no double-counting issue."""

    def test_saturday_and_holiday_still_blocked(self):
        # 2026-07-04 is Saturday
        saturday_holiday = date(2026, 7, 4)
        config = lc.Config(holidays={saturday_holiday})
        self.assertTrue(lc.is_blocked(saturday_holiday, config))

    def test_saturday_holiday_in_placement_skips(self):
        # Topic candidate lands on Saturday that is also a holiday — skipped once
        today = date(2026, 7, 2)  # Thursday
        saturday_holiday = date(2026, 7, 4)  # Saturday + holiday
        config = lc.Config(holidays={saturday_holiday})
        topics = [make_topic("t1", interval_days=2, score=3)]
        # candidate = 2026-07-04 (Saturday + holiday) → should skip to Sunday 2026-07-05
        results = lc.place_topics(topics, {}, today, config)
        placed = results[0][1]
        self.assertEqual(placed, date(2026, 7, 5))  # Sunday


class TestHolidaySkipInPlacement(unittest.TestCase):
    """Topic candidate falls on a holiday, gets shifted forward."""

    def test_placement_skips_holiday(self):
        today = date(2026, 6, 18)  # Thursday
        # Mark 2026-06-21 (Sunday) as holiday
        holiday = date(2026, 6, 21)
        config = lc.Config(holidays={holiday})

        # interval=3 → candidate = 2026-06-21 (holiday) → should skip to Monday 2026-06-22
        topics = [make_topic("t1", interval_days=3, score=3)]
        results = lc.place_topics(topics, {}, today, config)
        placed = results[0][1]
        self.assertEqual(placed, date(2026, 6, 22))
        # raw_date recorded as the holiday
        self.assertEqual(results[0][2], holiday)


class TestConsecutiveHolidays(unittest.TestCase):
    """Consecutive holidays (e.g. Dec 31 + Jan 1) — topic skips both."""

    def test_skips_consecutive_holidays(self):
        today = date(2026, 12, 29)  # Tuesday
        # Mark Dec 31 (Thursday) and Jan 1 (Friday) as holidays
        holidays = {date(2026, 12, 31), date(2027, 1, 1)}
        config = lc.Config(holidays=holidays)

        # interval=2 → candidate = 2026-12-31 (Thu, holiday) → Jan 1 (Fri, holiday)
        # → Jan 2 (Sat, blocked weekday) → lands on Jan 3 (Sun)
        topics = [make_topic("t1", interval_days=2, score=3)]
        results = lc.place_topics(topics, {}, today, config)
        placed = results[0][1]
        self.assertEqual(placed, date(2027, 1, 3))

    def test_skips_holiday_plus_saturday(self):
        # Holiday on Friday, Saturday follows — both blocked, land on Sunday
        today = date(2026, 6, 16)  # Tuesday
        holiday_friday = date(2026, 6, 19)  # Friday = holiday
        config = lc.Config(holidays={holiday_friday})

        # interval=3 → candidate = 2026-06-19 (Friday, holiday) → Saturday (blocked) → Sunday 2026-06-21
        topics = [make_topic("t1", interval_days=3, score=3)]
        results = lc.place_topics(topics, {}, today, config)
        placed = results[0][1]
        self.assertEqual(placed, date(2026, 6, 21))


class TestEmptyHolidaysFile(unittest.TestCase):
    """Empty holidays file — no dates blocked beyond the regular weekday."""

    def test_empty_array_returns_empty_set(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump([], f)
            tmp_path = f.name

        try:
            holidays = lc.load_holidays(tmp_path)
            self.assertEqual(holidays, set())
        finally:
            os.unlink(tmp_path)

    def test_empty_holidays_no_extra_blocking(self):
        """With an empty holidays file, only Saturday is blocked."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump([], f)
            tmp_path = f.name

        try:
            holidays = lc.load_holidays(tmp_path)
            config = lc.Config(holidays=holidays)
            # Wednesday 2026-06-24 should NOT be blocked
            self.assertFalse(lc.is_blocked(date(2026, 6, 24), config))
            # Saturday 2026-06-20 should still be blocked
            self.assertTrue(lc.is_blocked(date(2026, 6, 20), config))
        finally:
            os.unlink(tmp_path)


class TestMissingHolidaysFile(unittest.TestCase):
    """Missing holidays file — treated as empty, no error."""

    def test_missing_file_returns_empty_set(self):
        nonexistent = os.path.join(tempfile.gettempdir(), "no-such-holidays.json")
        if os.path.exists(nonexistent):
            os.unlink(nonexistent)

        holidays = lc.load_holidays(nonexistent)
        self.assertEqual(holidays, set())

    def test_missing_file_no_exception(self):
        """Calling load_holidays on a missing file does not raise any exception."""
        nonexistent = os.path.join(tempfile.gettempdir(), "definitely-missing-holidays.json")
        if os.path.exists(nonexistent):
            os.unlink(nonexistent)

        # Should not raise
        try:
            lc.load_holidays(nonexistent)
        except Exception as e:
            self.fail(f"load_holidays raised {type(e).__name__}: {e}")


class TestMalformedHolidaysFile(unittest.TestCase):
    """Malformed holidays file — graceful degradation, empty set returned."""

    def test_invalid_json_returns_empty_set(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            f.write("this is not valid json {{{")
            tmp_path = f.name

        try:
            holidays = lc.load_holidays(tmp_path)
            self.assertEqual(holidays, set())
        finally:
            os.unlink(tmp_path)

    def test_non_array_json_returns_empty_set(self):
        """JSON file contains an object instead of an array."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump({"not": "an array"}, f)
            tmp_path = f.name

        try:
            holidays = lc.load_holidays(tmp_path)
            self.assertEqual(holidays, set())
        finally:
            os.unlink(tmp_path)

    def test_mixed_valid_invalid_entries(self):
        """Array with some valid dates and some invalid entries — valid ones kept, invalid skipped."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(["2026-12-25", "not-a-date", 42, "2027-01-01"], f)
            tmp_path = f.name

        try:
            holidays = lc.load_holidays(tmp_path)
            self.assertEqual(len(holidays), 2)
            self.assertIn(date(2026, 12, 25), holidays)
            self.assertIn(date(2027, 1, 1), holidays)
        finally:
            os.unlink(tmp_path)


class TestMergeWriteOnlyChangesDate(unittest.TestCase):
    """merge_and_write should only update next_review — never overwrite SM-2 fields."""

    def test_interval_days_not_overwritten_by_input(self):
        """Existing entry has interval_days=6. Input sends interval_days=1.
        After merge_and_write, persisted interval_days must remain 6."""
        today = date(2026, 6, 18)
        existing_entry = {
            "lesson_file": "JPLessons/Udemy/N4/Grammar/UN4GL5.md",
            "grammar_header": "いこうけい Group 1",
            "last_reviewed": "2026-06-14",
            "next_review": "2026-06-20",
            "interval_days": 6,
            "ease": 2.35,
            "streak": 4,
            "total_reviews": 4,
            "last_score": 4,
            "weak_points": [],
        }
        gp = {"UN4GL5::ikoukei-group-1": existing_entry.copy()}
        state_data = {"grammar_points": gp}

        topics = [make_topic(
            "UN4GL5::ikoukei-group-1",
            interval_days=1, score=4,
            ease=2.35, streak=4, total_reviews=4,
        )]
        results = lc.place_topics(topics, gp, today)

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            tmp_path = Path(f.name)

        try:
            lc.merge_and_write(results, gp, tmp_path, state_data)
            with open(tmp_path) as f:
                written = json.load(f)

            entry = written["grammar_points"]["UN4GL5::ikoukei-group-1"]
            # next_review should have changed (placed by load control)
            self.assertNotEqual(entry["next_review"], "2026-06-20")
            # interval_days must NOT be overwritten — should remain 6
            self.assertEqual(entry["interval_days"], 6)
            # ease must NOT be overwritten
            self.assertEqual(entry["ease"], 2.35)
        finally:
            tmp_path.unlink(missing_ok=True)

    def test_sm2_fields_preserved_for_new_session_topic(self):
        """Even for normal sessions, existing SM-2 fields should not be
        corrupted if the input happens to differ from state."""
        today = date(2026, 6, 18)
        existing_entry = {
            "lesson_file": "JPLessons/test.md",
            "grammar_header": "Test Point",
            "last_reviewed": "2026-06-15",
            "next_review": "2026-06-18",
            "interval_days": 4,
            "ease": 2.5,
            "streak": 2,
            "total_reviews": 3,
            "last_score": 3,
            "weak_points": [],
        }
        gp = {"test::point": existing_entry.copy()}
        state_data = {"grammar_points": gp}

        topics = [make_topic(
            "test::point",
            interval_days=10, score=3,
            ease=2.5, streak=3, total_reviews=4,
        )]
        results = lc.place_topics(topics, gp, today)

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            tmp_path = Path(f.name)

        try:
            lc.merge_and_write(results, gp, tmp_path, state_data)
            with open(tmp_path) as f:
                written = json.load(f)

            entry = written["grammar_points"]["test::point"]
            # next_review should be updated by load control
            self.assertNotEqual(entry["next_review"], "2026-06-18")
            # SM-2 fields should come from EXISTING state, not input
            self.assertEqual(entry["interval_days"], 4)
            self.assertEqual(entry["streak"], 2)
            self.assertEqual(entry["total_reviews"], 3)
        finally:
            tmp_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
