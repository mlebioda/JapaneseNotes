#!/usr/bin/env python3
"""
Holiday cascade — FIFO-sweep redistribution for grammar-state.json reviews
displaced by newly-added holiday dates.

This is a standalone replacement for the old "load-control.py-via---today-trick"
redistribution mechanism used by manage-holidays.md. That mechanism reused
load-control.py's cap-based place_topics()/find_placement_date() logic, which
is designed for day-to-day SRS scheduling and silently violates DAILY_CAP/
WEAK_CAP when its 30-day search window is already saturated: the fallback
dumps the displaced topic onto the least-crowded day in the window even if
that day is already at or over cap, with no warning. Unacceptable for holiday
redistribution specifically.

This script never touches load-control.py's cap-based placement logic. It
only reuses three read-only helpers via importlib (load_holidays, load_rules,
is_blocked) so the "what counts as a blocked day" definition stays a single
source of truth. load-control.py itself is not modified and continues to be
used, unchanged, for normal day-to-day SRS scheduling.

Algorithm — single-pass FIFO sweep, no caps, no score sorting
---------------------------------------------------------------
1. sweep_start = min(--new-dates). This is the ONLY valid source for
   sweep_start. holidays.json has no "added when" metadata, so scanning it
   for the earliest date would incorrectly pull in unrelated holidays added
   in earlier, separate operations. Entries with next_review < sweep_start
   are completely out of scope: never touched, never even inspected for
   blocking purposes.
2. "Blocked" = Saturday (weekday() == 5) OR present in the fully-merged
   holidays.json set (old holidays + all newly-added dates, since
   manage-holidays.md writes holidays.json before invoking this script).
   There is no cap of any kind — a day already holding a lot of content is
   never "blocked" by that fact alone.
3. Walk forward one calendar day at a time from sweep_start, maintaining a
   single FIFO queue of "batches" (a batch = every grammar-point key
   originally scheduled on one particular day, moved together as a unit,
   never split). For each day D in order:
     a. If D has original content (from the pre-mutation snapshot) -> enqueue
        it as one batch at the BACK of the queue. Do this before step b for
        the same D.
     b. If D is NOT blocked AND the queue is non-empty -> pop the batch at
        the FRONT of the queue and set next_review = D for every key in it.
     c. If D is blocked -> no assignment happens on D this step, regardless
        of queue state.
   Continue until the queue is empty (content is finite, so this terminates
   naturally), bounded by a 365-day safety cap shared by both the day-walk
   and the implicit queue-drain.
4. Because this is one single global sweep over the whole timeline (not
   independent per-source-day searches), multiple holiday ranges added in
   the same operation resolve correctly automatically.
5. Only next_review is ever written for a shifted key. Every other field
   (interval_days, ease, streak, last_score, total_reviews, weak_points,
   lesson_file, grammar_header, etc.) is left completely untouched —
   mirroring load-control.py's merge_and_write() guarantee.

Worked example (verified by hand, matches the plan's own trace exactly):
holiday 14-27 Sept 2026 (sweep_start = Sept 14). Original content: Sept 14
(5 items), Sept 16 (2), Sept 20 (4), Sept 28 (6), Sept 29 (some), Sept 30
(some).
  - Sept 14's batch -> lands Sept 28 (first unblocked day the sweep reaches
    with a non-empty queue).
  - Sept 16's batch -> lands Sept 29.
  - Sept 20's batch -> lands Sept 30.
  - Sept 28's *original* content (displaced when the sweep reached Sept 28
    and gave that slot to Sept 14's batch) -> lands Oct 1.
  - Sept 29's original content -> lands Oct 2.
  - Sept 30's original content -> Oct 3 is a Saturday (blocked, skipped) ->
    lands Oct 4.

Interface:
  --state PATH: path to grammar-state.json (default: .cowork/progress/grammar-state.json)
  --rules PATH: path to load-control-rules.json (default: .cowork/progress/load-control-rules.json)
  --new-dates DATES: required, comma-separated ISO dates added in THIS
    add-holiday operation. sweep_start = min(new_dates).
  --dry-run: print intended shifts without writing the state file.

No --holidays flag: the holidays file path is derived from --rules's
holidays_file key via load_rules(), matching load-control.py's own pattern.
No stdin input: this script operates on every entry in grammar-state.json
directly, not a per-session topic list.

stdout: one summary line per shifted key ("<key>: <old> -> <new> (sweep)"),
plus a final "N topic(s) shifted." (or "0 topic(s) shifted -- no
collisions.").
Exit 0 on success, 1 on error (malformed state file, 365-day safety bound
exceeded, etc. — errors to stderr).
"""

import argparse
import importlib.util
import json
import sys
from collections import defaultdict, deque
from datetime import date, timedelta
from pathlib import Path

# --- Import load_holidays / load_rules / is_blocked from load-control.py ---
# Same importlib.util pattern already used by test_load_control.py to import
# a hyphenated-filename script. load-control.py itself is never modified.
_script_dir = Path(__file__).parent
_spec = importlib.util.spec_from_file_location(
    "load_control", _script_dir / "load-control.py"
)
lc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lc)

MAX_SWEEP_DAYS = 365  # Shared bound for both the day-walk and the queue-drain.


class CascadeSafetyError(Exception):
    """Raised when the FIFO queue does not empty within MAX_SWEEP_DAYS."""


def parse_new_dates(raw: str) -> list:
    """
    Parse a comma-separated string of ISO dates into a sorted list of date
    objects. Exits 1 on any unparseable token or if the result is empty.
    """
    dates = []
    for token in raw.split(","):
        token = token.strip()
        if not token:
            continue
        try:
            dates.append(date.fromisoformat(token))
        except ValueError:
            print(
                f"Error: invalid date in --new-dates: {token!r}",
                file=sys.stderr,
            )
            sys.exit(1)

    if not dates:
        print("Error: --new-dates must contain at least one ISO date", file=sys.stderr)
        sys.exit(1)

    return sorted(dates)


def build_snapshot(grammar_points: dict, sweep_start: date) -> dict:
    """
    Build {date: [keys]} for every grammar_points entry whose next_review
    is on or after sweep_start.

    Entries with a missing or unparseable next_review are skipped — same
    try/except-continue pattern as load-control.py's build_day_counts().
    Entries with next_review strictly before sweep_start are out of scope
    and excluded here (they are never enqueued, never touched).
    """
    snapshot = defaultdict(list)
    for key, entry in grammar_points.items():
        nr = entry.get("next_review", "")
        if not nr:
            continue
        try:
            d = date.fromisoformat(nr)
        except (ValueError, TypeError):
            continue
        if d < sweep_start:
            continue
        snapshot[d].append(key)
    return dict(snapshot)


def run_sweep(snapshot: dict, sweep_start: date, config) -> tuple:
    """
    Run the single-pass FIFO sweep starting at sweep_start.

    Returns (assignments, originals):
      - assignments: {key: new_date} for every key that was ever popped off
        the queue (including keys whose new_date equals their original date
        — see case where a day's own content is enqueued and immediately
        dequeued the same day because the queue was empty).
      - originals: {key: original_date} for every key present in snapshot.

    Raises CascadeSafetyError if the queue is still non-empty MAX_SWEEP_DAYS
    past sweep_start.
    """
    originals = {}
    for d, keys in snapshot.items():
        for key in keys:
            originals[key] = d

    if not snapshot:
        return {}, originals

    last_content_date = max(snapshot.keys())

    queue = deque()
    assignments = {}

    d = sweep_start
    offset = 0
    while True:
        if offset > MAX_SWEEP_DAYS:
            pending = sum(len(batch) for batch in queue)
            raise CascadeSafetyError(
                f"Safety bound exceeded: {pending} item(s) still queued "
                f"{MAX_SWEEP_DAYS} days past sweep_start {sweep_start.isoformat()}"
            )

        # (a) Enqueue today's original content, if any, before dequeuing.
        if d in snapshot:
            queue.append(list(snapshot[d]))

        # (b) / (c) Dequeue the front batch only if today is not blocked.
        if queue and not lc.is_blocked(d, config):
            batch = queue.popleft()
            for key in batch:
                assignments[key] = d

        # Stop once the queue is empty and no more original content can
        # ever appear (we've reached/passed the last day with content).
        if not queue and d >= last_content_date:
            break

        d += timedelta(days=1)
        offset += 1

    return assignments, originals


def compute_shifts(grammar_points: dict, sweep_start: date, config) -> dict:
    """
    Convenience wrapper: build the snapshot, run the sweep, and return only
    the keys whose next_review actually changed ({key: new_date}).
    """
    snapshot = build_snapshot(grammar_points, sweep_start)
    assignments, originals = run_sweep(snapshot, sweep_start, config)
    return {k: v for k, v in assignments.items() if v != originals[k]}, originals


def main():
    parser = argparse.ArgumentParser(
        description="Holiday cascade — FIFO-sweep redistribution for holiday-blocked SRS reviews"
    )
    parser.add_argument(
        "--state",
        default=".cowork/progress/grammar-state.json",
        help="Path to grammar-state.json",
    )
    parser.add_argument(
        "--rules",
        default=".cowork/progress/load-control-rules.json",
        help="Path to load-control-rules.json",
    )
    parser.add_argument(
        "--new-dates",
        required=True,
        help="Comma-separated ISO dates added in this add-holiday operation",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print intended shifts without writing the state file",
    )
    args = parser.parse_args()

    new_dates = parse_new_dates(args.new_dates)
    sweep_start = new_dates[0]

    config = lc.load_rules(args.rules)
    config.holidays = lc.load_holidays(config.holidays_file)

    state_path = Path(args.state)
    if state_path.exists():
        try:
            with open(state_path, encoding="utf-8") as f:
                state_data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            print(f"Error reading state file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        state_data = {"grammar_points": {}}

    grammar_points = state_data.get("grammar_points", {})

    try:
        shifted, originals = compute_shifts(grammar_points, sweep_start, config)
    except CascadeSafetyError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if not shifted:
        print("0 topic(s) shifted -- no collisions.")
        sys.exit(0)

    for key in sorted(shifted, key=lambda k: (originals[k], k)):
        new_date = shifted[key]
        print(f"{key}: {originals[key].isoformat()} -> {new_date.isoformat()} (sweep)")
    print(f"{len(shifted)} topic(s) shifted.")

    if args.dry_run:
        sys.exit(0)

    for key, new_date in shifted.items():
        grammar_points[key]["next_review"] = new_date.isoformat()

    state_data["grammar_points"] = grammar_points
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state_data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    sys.exit(0)


if __name__ == "__main__":
    main()
