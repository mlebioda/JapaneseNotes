#!/usr/bin/env python3
"""
Tests for holiday-cascade.py — FIFO-sweep holiday redistribution logic.

Run: python3 -m pytest test_holiday_cascade.py -v
  or: python3 test_holiday_cascade.py

Calendar anchor used throughout (matches test_load_control.py's own anchor):
2026-06-18 is a Thursday. Derived from that: 2026-06-20/27 and 07-04/11/18/25
and 06-20 etc. are Saturdays. This is verified consistent with the plan's own
worked example (holiday 14-27 Sept 2026 -> Oct 3, 2026 is a Saturday).
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

# Import holiday-cascade.py despite the hyphen in filename
_script_dir = Path(__file__).parent
_spec = importlib.util.spec_from_file_location(
    "holiday_cascade", _script_dir / "holiday-cascade.py"
)
hc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(hc)

# Same import for load-control.py, needed to build Config objects directly.
_lc_spec = importlib.util.spec_from_file_location(
    "load_control", _script_dir / "load-control.py"
)
lc = importlib.util.module_from_spec(_lc_spec)
_lc_spec.loader.exec_module(lc)


def make_entry(next_review, **kwargs):
    """Helper to build a grammar_points entry dict."""
    e = {
        "lesson_file": "JPLessons/Udemy/N4/Grammar/UN4GL5.md",
        "grammar_header": "Test Point",
        "last_reviewed": "2026-06-01",
        "next_review": next_review,
        "interval_days": 5,
        "ease": 2.5,
        "streak": 2,
        "total_reviews": 3,
        "last_score": 3,
        "weak_points": [],
    }
    e.update(kwargs)
    return e


def make_batch(prefix, date_str, count):
    """Helper: N grammar_points entries all sharing one next_review date."""
    return {f"{prefix}-{i}": make_entry(date_str) for i in range(count)}


def dates_range(start: date, end: date):
    """Inclusive list of date objects from start to end."""
    days = (end - start).days
    return [start + timedelta(days=i) for i in range(days + 1)]


class TestHolidayContentNextDayEmpty(unittest.TestCase):
    """Case 1: holiday day has content, next day empty -> lands there, sweep ends."""

    def test_lands_next_day(self):
        holiday = date(2026, 6, 23)  # Tuesday
        config = lc.Config(holidays={holiday})
        gp = make_batch("h1", "2026-06-23", 3)

        shifted, originals = hc.compute_shifts(gp, holiday, config)

        self.assertEqual(len(shifted), 3)
        for key in gp:
            self.assertEqual(shifted[key], date(2026, 6, 24))


class TestTwoStepQueueDrain(unittest.TestCase):
    """Case 2: holiday day has content, next day occupied, day after empty ->
    two-step queue drain."""

    def test_two_step_drain(self):
        holiday = date(2026, 6, 23)  # Tuesday
        config = lc.Config(holidays={holiday})
        gp = {}
        gp.update(make_batch("a", "2026-06-23", 2))   # batch A on the holiday
        gp.update(make_batch("b", "2026-06-24", 3))   # batch B, unblocked day

        shifted, originals = hc.compute_shifts(gp, holiday, config)

        for key in ("a-0", "a-1"):
            self.assertEqual(shifted[key], date(2026, 6, 24))
        for key in ("b-0", "b-1", "b-2"):
            self.assertEqual(shifted[key], date(2026, 6, 25))


class TestLongQueueDrain(unittest.TestCase):
    """Case 3: long run of occupied days after the holiday -> queue drains
    over many days before emptying."""

    def test_chain_drains_over_several_days(self):
        holiday = date(2026, 6, 23)  # Tuesday
        config = lc.Config(holidays={holiday})
        gp = {}
        gp.update(make_batch("a", "2026-06-23", 1))  # on the holiday
        gp.update(make_batch("b", "2026-06-24", 1))  # Wed, unblocked, own content
        gp.update(make_batch("c", "2026-06-25", 1))  # Thu, unblocked, own content
        gp.update(make_batch("d", "2026-06-26", 1))  # Fri, unblocked, own content
        # 2026-06-27 is Saturday (blocked, no content needed there)

        shifted, originals = hc.compute_shifts(gp, holiday, config)

        self.assertEqual(shifted["a-0"], date(2026, 6, 24))
        self.assertEqual(shifted["b-0"], date(2026, 6, 25))
        self.assertEqual(shifted["c-0"], date(2026, 6, 26))
        self.assertEqual(shifted["d-0"], date(2026, 6, 28))  # skips Sat 06-27


class TestBatchAtomicity(unittest.TestCase):
    """Case 4: all content on one blocked day moves together as a single
    batch (not split)."""

    def test_batch_not_split(self):
        holiday = date(2026, 6, 23)  # Tuesday
        config = lc.Config(holidays={holiday})
        gp = make_batch("h4", "2026-06-23", 4)

        shifted, originals = hc.compute_shifts(gp, holiday, config)

        landing_dates = set(shifted.values())
        # All 4 keys must land on the exact same date — batch never splits.
        self.assertEqual(len(landing_dates), 1)
        self.assertEqual(landing_dates.pop(), date(2026, 6, 24))


class TestLandingOnSaturdaySkipped(unittest.TestCase):
    """Case 5: landing day would be a Saturday -> skipped by the sweep."""

    def test_saturday_skipped(self):
        holiday = date(2026, 6, 19)  # Friday
        config = lc.Config(holidays={holiday})
        gp = make_batch("h5", "2026-06-19", 1)

        shifted, originals = hc.compute_shifts(gp, holiday, config)

        # 2026-06-20 is Saturday, blocked -> lands on Sunday 2026-06-21
        self.assertEqual(shifted["h5-0"], date(2026, 6, 21))


class TestLandingOnPreExistingHoliday(unittest.TestCase):
    """Case 6: landing day would be a pre-existing (not newly-added) holiday
    -> also skipped."""

    def test_preexisting_holiday_skipped(self):
        new_holiday = date(2026, 6, 23)   # Tuesday, newly added
        old_holiday = date(2026, 6, 24)   # Wednesday, pre-existing, unrelated
        config = lc.Config(holidays={new_holiday, old_holiday})
        gp = make_batch("h6", "2026-06-23", 1)

        # sweep_start comes from --new-dates only (the new holiday)
        shifted, originals = hc.compute_shifts(gp, new_holiday, config)

        # 06-24 is also blocked (pre-existing holiday) -> lands 06-25
        self.assertEqual(shifted["h6-0"], date(2026, 6, 25))


class TestHolidayEndsBeforeSaturday(unittest.TestCase):
    """Case 7: holiday ends immediately before a Saturday -> correct
    skip-over."""

    def test_skip_over_holiday_then_saturday(self):
        holiday_days = {date(2026, 6, 17), date(2026, 6, 18), date(2026, 6, 19)}
        config = lc.Config(holidays=set(holiday_days))
        sweep_start = date(2026, 6, 17)  # Wednesday
        gp = make_batch("h7", "2026-06-17", 1)

        shifted, originals = hc.compute_shifts(gp, sweep_start, config)

        # 06-17,18,19 holiday; 06-20 Saturday; lands 06-21 (Sunday)
        self.assertEqual(shifted["h7-0"], date(2026, 6, 21))


class TestMultiDayRange(unittest.TestCase):
    """Case 8: multi-day range -> content from both days queues in
    chronological order, lands on consecutive first-available days after
    the range."""

    def test_range_content_queues_in_order(self):
        holiday_days = {date(2026, 6, 17), date(2026, 6, 18)}
        config = lc.Config(holidays=set(holiday_days))
        sweep_start = date(2026, 6, 17)  # Wednesday
        gp = {}
        gp.update(make_batch("r1", "2026-06-17", 2))
        gp.update(make_batch("r2", "2026-06-18", 3))

        shifted, originals = hc.compute_shifts(gp, sweep_start, config)

        for key in ("r1-0", "r1-1"):
            self.assertEqual(shifted[key], date(2026, 6, 19))  # Friday
        for key in ("r2-0", "r2-1", "r2-2"):
            # 06-20 is Saturday, blocked -> lands 06-21 (Sunday)
            self.assertEqual(shifted[key], date(2026, 6, 21))


class TestTwoSeparateRanges(unittest.TestCase):
    """Case 9: two separate ranges added in one call -> resolved correctly
    by the single sweep, no special-casing needed."""

    def test_two_independent_ranges(self):
        range1 = {date(2026, 6, 17), date(2026, 6, 18)}
        range2 = {date(2026, 7, 13), date(2026, 7, 14)}
        config = lc.Config(holidays=set(range1 | range2))
        sweep_start = date(2026, 6, 17)  # min of all new dates
        gp = {}
        gp.update(make_batch("r1a", "2026-06-17", 1))
        gp.update(make_batch("r1b", "2026-06-18", 1))
        gp.update(make_batch("r2a", "2026-07-13", 1))
        gp.update(make_batch("r2b", "2026-07-14", 1))

        shifted, originals = hc.compute_shifts(gp, sweep_start, config)

        self.assertEqual(shifted["r1a-0"], date(2026, 6, 19))
        self.assertEqual(shifted["r1b-0"], date(2026, 6, 21))  # skips Sat 06-20
        self.assertEqual(shifted["r2a-0"], date(2026, 7, 15))
        self.assertEqual(shifted["r2b-0"], date(2026, 7, 16))


class TestDisplacementTailIntersectsSecondRange(unittest.TestCase):
    """Case 10: one range's displacement tail reaches far enough to
    intersect a second range -> still resolves correctly with no
    double-shifting."""

    def test_tail_intersects_second_range(self):
        # Range 1: single-day holiday 06-17, with backlog on 06-18 and 06-19
        # pushing a displacement tail toward 06-21 (Sunday).
        # Range 2: a second new holiday exactly on 06-21, intersecting the tail.
        range1 = {date(2026, 6, 17)}
        range2 = {date(2026, 6, 21)}
        config = lc.Config(holidays=set(range1 | range2))
        sweep_start = date(2026, 6, 17)  # Wednesday
        gp = {}
        gp.update(make_batch("a", "2026-06-17", 1))
        gp.update(make_batch("b", "2026-06-18", 1))
        gp.update(make_batch("c", "2026-06-19", 1))

        shifted, originals = hc.compute_shifts(gp, sweep_start, config)

        self.assertEqual(shifted["a-0"], date(2026, 6, 18))
        self.assertEqual(shifted["b-0"], date(2026, 6, 19))
        # Without range2, c would land 06-21 (Sun). With 06-21 also blocked
        # (range 2), 06-20 (Sat) also blocked -> lands 06-22 (Mon).
        self.assertEqual(shifted["c-0"], date(2026, 6, 22))
        # No key appears twice / no double shifting: exactly 3 shifted keys.
        self.assertEqual(len(shifted), 3)


class TestLongHolidaySpanningSaturdays(unittest.TestCase):
    """Case 11: long holiday spanning one or more Saturdays -> the in-range
    Saturdays don't need separate handling, they just extend the blocked
    stretch the sweep passes over."""

    def test_saturdays_inside_range_are_absorbed(self):
        start = date(2026, 6, 17)  # Wednesday
        end = date(2026, 6, 29)    # Monday — spans Saturdays 06-20 and 06-27
        holiday_days = set(dates_range(start, end))
        config = lc.Config(holidays=holiday_days)
        gp = make_batch("h11", "2026-06-17", 1)

        shifted, originals = hc.compute_shifts(gp, start, config)

        # First unblocked day after the whole stretch (06-30, Tuesday)
        self.assertEqual(shifted["h11-0"], date(2026, 6, 30))


class TestOnlyNextReviewChanges(unittest.TestCase):
    """Case 12: only next_review changes on any shifted entry -- all other
    fields are left untouched. Verified at the CLI/file level, mirroring
    merge_and_write()'s guarantee in load-control.py."""

    def test_other_fields_untouched_after_write(self):
        script = str(_script_dir / "holiday-cascade.py")
        holiday = "2026-06-23"
        entry = make_entry(
            holiday, interval_days=6, ease=2.35, streak=4,
            total_reviews=4, last_score=4, weak_points=["te-form"],
            lesson_file="grammar-index/grammar/some-point.md",
            grammar_header="Some Point",
        )
        state = {"grammar_points": {"k1": entry}}
        rules = {"holidays_file": None}  # filled in below

        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = os.path.join(tmpdir, "state.json")
            holidays_path = os.path.join(tmpdir, "holidays.json")
            rules_path = os.path.join(tmpdir, "rules.json")

            with open(state_path, "w") as f:
                json.dump(state, f)
            with open(holidays_path, "w") as f:
                json.dump([holiday], f)
            with open(rules_path, "w") as f:
                json.dump({"holidays_file": holidays_path}, f)

            result = subprocess.run(
                [
                    sys.executable, script,
                    "--state", state_path,
                    "--rules", rules_path,
                    "--new-dates", holiday,
                ],
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

            with open(state_path) as f:
                written = json.load(f)

            out = written["grammar_points"]["k1"]
            self.assertNotEqual(out["next_review"], holiday)
            self.assertEqual(out["interval_days"], 6)
            self.assertEqual(out["ease"], 2.35)
            self.assertEqual(out["streak"], 4)
            self.assertEqual(out["total_reviews"], 4)
            self.assertEqual(out["last_score"], 4)
            self.assertEqual(out["weak_points"], ["te-form"])
            self.assertEqual(
                out["lesson_file"], "grammar-index/grammar/some-point.md"
            )
            self.assertEqual(out["grammar_header"], "Some Point")


class TestNoCollisionsNoOp(unittest.TestCase):
    """Case 13: no collisions at all -> no-op, 0 shifted, file unchanged."""

    def test_no_collisions_file_unchanged(self):
        script = str(_script_dir / "holiday-cascade.py")
        holiday = "2026-06-23"
        # Only content strictly before the holiday -- out of scope entirely.
        entry = make_entry("2026-06-01")
        state = {"grammar_points": {"k1": entry}}

        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = os.path.join(tmpdir, "state.json")
            holidays_path = os.path.join(tmpdir, "holidays.json")
            rules_path = os.path.join(tmpdir, "rules.json")

            with open(state_path, "w") as f:
                json.dump(state, f)
            with open(holidays_path, "w") as f:
                json.dump([holiday], f)
            with open(rules_path, "w") as f:
                json.dump({"holidays_file": holidays_path}, f)

            before = Path(state_path).read_text()

            result = subprocess.run(
                [
                    sys.executable, script,
                    "--state", state_path,
                    "--rules", rules_path,
                    "--new-dates", holiday,
                ],
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("0 topic(s) shifted", result.stdout)

            after = Path(state_path).read_text()
            self.assertEqual(before, after)


class TestSafetyBoundExceeded(unittest.TestCase):
    """Case 14: queue never empties within 365 days of sweep_start (data
    anomaly) -> error out instead of looping forever."""

    def test_raises_on_never_ending_block(self):
        sweep_start = date(2026, 6, 17)
        # Block every day from sweep_start for 400 days straight -- the
        # queue can never drain within the 365-day safety bound.
        holiday_days = set(dates_range(sweep_start, sweep_start + timedelta(days=400)))
        config = lc.Config(holidays=holiday_days)
        gp = make_batch("stuck", "2026-06-17", 1)

        with self.assertRaises(hc.CascadeSafetyError):
            hc.compute_shifts(gp, sweep_start, config)

    def test_cli_exits_1_on_safety_bound(self):
        script = str(_script_dir / "holiday-cascade.py")
        sweep_start = date(2026, 6, 17)
        holiday_days = [
            d.isoformat()
            for d in dates_range(sweep_start, sweep_start + timedelta(days=400))
        ]
        gp = {"stuck-0": make_entry("2026-06-17")}
        state = {"grammar_points": gp}

        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = os.path.join(tmpdir, "state.json")
            holidays_path = os.path.join(tmpdir, "holidays.json")
            rules_path = os.path.join(tmpdir, "rules.json")

            with open(state_path, "w") as f:
                json.dump(state, f)
            with open(holidays_path, "w") as f:
                json.dump(holiday_days, f)
            with open(rules_path, "w") as f:
                json.dump({"holidays_file": holidays_path}, f)

            result = subprocess.run(
                [
                    sys.executable, script,
                    "--state", state_path,
                    "--rules", rules_path,
                    "--new-dates", "2026-06-17",
                ],
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("Safety bound exceeded", result.stderr)


class TestUnaffectedDayStaysUnchanged(unittest.TestCase):
    """Case 15: a day has its own original content, is not blocked, and the
    queue is empty when the sweep reaches it -> stays completely
    unchanged."""

    def test_unrelated_content_not_shifted(self):
        # Holiday itself has no content; the only content is on an unblocked
        # day reached afterward with nothing ahead of it in the queue.
        holiday = date(2026, 6, 19)  # Friday, no content here
        config = lc.Config(holidays={holiday})
        sweep_start = holiday
        gp = make_batch("e", "2026-06-21", 2)  # Sunday, unrelated content

        shifted, originals = hc.compute_shifts(gp, sweep_start, config)

        # Nothing should be reported as shifted -- it lands on its own date.
        self.assertEqual(shifted, {})
        # But it was inspected (in scope, >= sweep_start) and recorded.
        self.assertEqual(originals["e-0"], date(2026, 6, 21))


class TestContentBeforeSweepStartUntouched(unittest.TestCase):
    """Case 16: content scheduled before sweep_start -> completely
    untouched, even if it sits on some older, unrelated holiday date
    elsewhere in the file."""

    def test_pre_sweep_start_content_ignored(self):
        new_holiday = date(2026, 6, 23)  # Tuesday
        old_unrelated_holiday = date(2026, 6, 20)  # Saturday, already blocked anyway
        config = lc.Config(holidays={new_holiday, old_unrelated_holiday})
        gp = {}
        gp["old"] = make_entry("2026-06-20")  # before sweep_start, on a blocked day
        gp.update(make_batch("cur", "2026-06-23", 1))  # in-scope content

        shifted, originals = hc.compute_shifts(gp, new_holiday, config)

        # The pre-sweep_start entry must never even appear in originals.
        self.assertNotIn("old", originals)
        self.assertNotIn("old", shifted)
        # The in-scope entry resolves normally.
        self.assertEqual(shifted["cur-0"], date(2026, 6, 24))


class TestWorkedExampleFromPlan(unittest.TestCase):
    """Integration test replicating the plan's own hand-verified worked
    example: holiday 14-27 Sept 2026, content on Sept 14/16/20/28/29/30."""

    def test_full_worked_example(self):
        start = date(2026, 9, 14)
        end = date(2026, 9, 27)
        holiday_days = set(dates_range(start, end))
        config = lc.Config(holidays=holiday_days)

        gp = {}
        gp.update(make_batch("d14", "2026-09-14", 5))
        gp.update(make_batch("d16", "2026-09-16", 2))
        gp.update(make_batch("d20", "2026-09-20", 4))
        gp.update(make_batch("d28", "2026-09-28", 6))
        gp.update(make_batch("d29", "2026-09-29", 1))
        gp.update(make_batch("d30", "2026-09-30", 1))

        shifted, originals = hc.compute_shifts(gp, start, config)

        for i in range(5):
            self.assertEqual(shifted[f"d14-{i}"], date(2026, 9, 28))
        for i in range(2):
            self.assertEqual(shifted[f"d16-{i}"], date(2026, 9, 29))
        for i in range(4):
            self.assertEqual(shifted[f"d20-{i}"], date(2026, 9, 30))
        for i in range(6):
            self.assertEqual(shifted[f"d28-{i}"], date(2026, 10, 1))
        self.assertEqual(shifted["d29-0"], date(2026, 10, 2))
        # 2026-10-03 is a Saturday -- skipped -> lands 10-04
        self.assertEqual(shifted["d30-0"], date(2026, 10, 4))


class TestDryRunDoesNotWrite(unittest.TestCase):
    """--dry-run prints intended shifts but never writes the state file."""

    def test_dry_run_leaves_file_unchanged(self):
        script = str(_script_dir / "holiday-cascade.py")
        holiday = "2026-06-23"
        entry = make_entry(holiday)
        state = {"grammar_points": {"k1": entry}}

        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = os.path.join(tmpdir, "state.json")
            holidays_path = os.path.join(tmpdir, "holidays.json")
            rules_path = os.path.join(tmpdir, "rules.json")

            with open(state_path, "w") as f:
                json.dump(state, f)
            with open(holidays_path, "w") as f:
                json.dump([holiday], f)
            with open(rules_path, "w") as f:
                json.dump({"holidays_file": holidays_path}, f)

            before = Path(state_path).read_text()

            result = subprocess.run(
                [
                    sys.executable, script,
                    "--state", state_path,
                    "--rules", rules_path,
                    "--new-dates", holiday,
                    "--dry-run",
                ],
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("1 topic(s) shifted.", result.stdout)

            after = Path(state_path).read_text()
            self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
