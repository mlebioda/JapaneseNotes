#!/usr/bin/env python3
"""
Load control for practice-grammar SRS date placement.

Prevents review pile-ups by spreading topics across days after SM-2 computes
review dates. Applies only to TODAY/OVERDUE scope sessions.

Interface:
  - stdin: JSON array of fully computed topic updates from the current session
  - --state PATH: path to grammar-state.json (default: .cowork/progress/grammar-state.json)
  - --today DATE: override today's date (ISO format, for testing)
  - stdout: placement summary
  - exit 0 on success, 1 on error (errors to stderr)
"""

import argparse
import json
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path


# --- Config ---
@dataclass
class Config:
    """Bundle of load-control parameters. Defaults match the legacy constants."""
    daily_cap: int = 10
    weak_cap: int = 4
    blocked_weekday: int = 5       # Saturday (Monday=0)
    search_window: int = 30
    holidays: set[date] = field(default_factory=set)
    holidays_file: str = ".cowork/progress/holidays.json"


def load_rules(path) -> Config:
    """
    Read a load-control-rules JSON file and return a Config instance.

    Args:
        path: str or Path to the JSON rules file.

    Returns:
        Config with values from the file (falling back to Config() defaults
        for any missing key).

    On FileNotFoundError: prints warning to stderr, returns Config().
    On json.JSONDecodeError: prints error to stderr, sys.exit(1).
    """
    path = Path(path)
    defaults = Config()

    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(
            f"Warning: rules file not found: {path} — using defaults",
            file=sys.stderr,
        )
        return defaults
    except json.JSONDecodeError as e:
        print(
            f"Error: malformed rules file {path}: {e}",
            file=sys.stderr,
        )
        sys.exit(1)

    # Expected keys and their required types
    _int_keys = {
        "DAILY_CAP": "daily_cap",
        "WEAK_CAP": "weak_cap",
        "BLOCKED_WEEKDAY": "blocked_weekday",
        "SEARCH_WINDOW": "search_window",
    }
    _str_keys = {
        "holidays_file": "holidays_file",
    }

    kwargs = {}

    for json_key, attr_name in _int_keys.items():
        if json_key in data:
            val = data[json_key]
            if not isinstance(val, int) or isinstance(val, bool):
                print(
                    f"Warning: rules key '{json_key}' should be int, "
                    f"got {type(val).__name__} — using default",
                    file=sys.stderr,
                )
            else:
                kwargs[attr_name] = val

    for json_key, attr_name in _str_keys.items():
        if json_key in data:
            val = data[json_key]
            if not isinstance(val, str):
                print(
                    f"Warning: rules key '{json_key}' should be str, "
                    f"got {type(val).__name__} — using default",
                    file=sys.stderr,
                )
            else:
                kwargs[attr_name] = val

    return Config(**kwargs)


def load_holidays(path) -> set:
    """
    Read a holidays JSON file and return a set of date objects.

    Args:
        path: str or Path to a JSON file containing an array of ISO date
              strings, e.g. ["2026-07-04", "2026-12-25"].

    Returns:
        set[date] of parsed holiday dates.

    On FileNotFoundError: returns empty set (no holidays configured yet).
    On json.JSONDecodeError: prints warning to stderr, returns empty set.
    Invalid individual entries: skipped with warning to stderr.
    """
    path = Path(path)
    holidays: set[date] = set()

    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return holidays
    except json.JSONDecodeError as e:
        print(
            f"Warning: malformed holidays file {path}: {e} — using empty set",
            file=sys.stderr,
        )
        return holidays

    if not isinstance(data, list):
        print(
            f"Warning: holidays file {path} should contain a JSON array, "
            f"got {type(data).__name__} — using empty set",
            file=sys.stderr,
        )
        return holidays

    for i, entry in enumerate(data):
        if not isinstance(entry, str):
            print(
                f"Warning: holidays entry at index {i} should be a string, "
                f"got {type(entry).__name__} — skipping",
                file=sys.stderr,
            )
            continue
        try:
            holidays.add(date.fromisoformat(entry))
        except ValueError:
            print(
                f"Warning: holidays entry at index {i} is not a valid ISO date: "
                f"{entry!r} — skipping",
                file=sys.stderr,
            )

    return holidays


# --- Constants ---
DAILY_CAP = 10       # Max topics on any single day
WEAK_CAP = 4         # Max topics with score 1 or 2 on any single day
BLOCKED_WEEKDAY = 5  # Saturday (Monday=0, Saturday=5)
SEARCH_WINDOW = 30   # Max days to search forward before fallback


def is_blocked(d: date, config: Config | None = None) -> bool:
    """Return True if reviews should not be placed on this day."""
    if config is None:
        config = Config()
    return d.weekday() == config.blocked_weekday or d in config.holidays


def build_day_counts(grammar_points: dict, today: date) -> dict:
    """
    Build a dict of {date_str: {"total": N, "weak": N}} from existing
    next_review dates in grammar-state.json that are >= today.

    We count all existing scheduled reviews so the placement algorithm
    respects the current load.
    """
    counts = defaultdict(lambda: {"total": 0, "weak": 0})
    for entry in grammar_points.values():
        nr = entry.get("next_review", "")
        if not nr:
            continue
        try:
            review_date = date.fromisoformat(nr)
        except (ValueError, TypeError):
            continue
        if review_date >= today:
            counts[nr]["total"] += 1
            # We don't know the score of existing entries for weak counting,
            # so we only count weak for entries that have last_score 1 or 2
            last_score = entry.get("last_score")
            if last_score in (1, 2):
                counts[nr]["weak"] += 1
    return counts


def find_placement_date(
    candidate: date,
    is_weak: bool,
    day_counts: dict,
    today: date,
    config: Config | None = None,
) -> tuple:
    """
    Search from candidate forward to find a valid placement date.

    Returns (placed_date, shifted_from_original: bool).
    """
    if config is None:
        config = Config()

    original = candidate
    fallback_date = None
    fallback_total = float("inf")

    for offset in range(config.search_window):
        d = candidate + timedelta(days=offset)
        d_str = d.isoformat()
        counts = day_counts.get(d_str, {"total": 0, "weak": 0})

        # Track fallback: earliest non-blocked day with lowest total
        if not is_blocked(d, config):
            if counts["total"] < fallback_total:
                fallback_total = counts["total"]
                fallback_date = d

        # Skip blocked days
        if is_blocked(d, config):
            continue

        # Skip if daily cap reached
        if counts["total"] >= config.daily_cap:
            continue

        # Skip if weak cap reached and this is a weak topic
        if is_weak and counts["weak"] >= config.weak_cap:
            continue

        # Valid day found
        shifted = d != original
        return d, shifted

    # Fallback: earliest non-blocked day with lowest total in window
    if fallback_date is not None:
        shifted = fallback_date != original
        return fallback_date, shifted

    # Absolute fallback: next day after window that isn't blocked
    d = candidate + timedelta(days=config.search_window)
    while is_blocked(d, config):
        d += timedelta(days=1)
    return d, True


def place_topics(
    topics: list,
    grammar_points: dict,
    today: date,
    config: Config | None = None,
) -> list:
    """
    Place all session topics onto review dates respecting load control rules.

    Args:
        topics: list of dicts from stdin (each with key, interval_days, score, etc.)
        grammar_points: current grammar_points dict from state file
        today: today's date
        config: optional Config; defaults to Config() if None

    Returns:
        list of (topic_dict, placed_date, shifted_from) tuples
    """
    if config is None:
        config = Config()

    # Build initial day counts from existing state
    day_counts = build_day_counts(grammar_points, today)

    # Sort input by score: 1 -> 2 -> 3 -> 4 (weak topics placed first)
    sorted_topics = sorted(topics, key=lambda t: t.get("score", 3))

    results = []
    for topic in sorted_topics:
        interval = topic.get("interval_days", 1)
        score = topic.get("score", 3)
        is_weak = score in (1, 2)

        # Candidate: max(today + 1, today + interval_days)
        # Minimum is tomorrow — never place on today
        candidate = today + timedelta(days=max(1, interval))

        placed_date, shifted = find_placement_date(
            candidate, is_weak, day_counts, today, config
        )

        # Update in-memory counts
        d_str = placed_date.isoformat()
        if d_str not in day_counts:
            day_counts[d_str] = {"total": 0, "weak": 0}
        day_counts[d_str]["total"] += 1
        if is_weak:
            day_counts[d_str]["weak"] += 1

        raw_date = candidate
        results.append((topic, placed_date, raw_date if shifted else None))

    return results


def merge_and_write(
    results: list,
    grammar_points: dict,
    state_path: Path,
    state_data: dict,
    config: Config | None = None,
) -> list:
    """
    Merge placed topics into grammar_points and write to file.

    Args:
        results: list of (topic_dict, placed_date, raw_date_or_None) from place_topics()
        grammar_points: current grammar_points dict from state file
        state_path: path to write the updated state JSON
        state_data: full state dict (grammar_points will be updated in place)
        config: optional Config; defaults to Config() if None

    Returns list of summary lines.
    """
    if config is None:
        config = Config()

    summary_lines = []
    original_keys = set(grammar_points.keys())

    for topic, placed_date, raw_date in results:
        key = topic["key"]

        # Build the entry from all provided fields + computed next_review
        entry = {}
        # If existing entry, start with it
        if key in grammar_points:
            entry = grammar_points[key].copy()

        is_new = key not in original_keys
        if is_new:
            # New entry: copy all provided fields
            for field in (
                "lesson_file", "grammar_header", "last_reviewed", "score",
                "interval_days", "ease", "streak", "total_reviews",
                "weak_points", "last_score",
            ):
                if field in topic:
                    entry[field] = topic[field]
        else:
            # Existing entry: only update identity fields, never SM-2 fields
            for field in ("lesson_file", "grammar_header"):
                if field in topic:
                    entry[field] = topic[field]

        # Set the computed next_review
        entry["next_review"] = placed_date.isoformat()

        grammar_points[key] = entry

        # Build summary line
        if raw_date is not None:
            if raw_date.weekday() == config.blocked_weekday:
                reason = ", Saturday"
            elif raw_date in config.holidays:
                reason = ", holiday"
            else:
                reason = ""
            summary_lines.append(
                f"{key}: {placed_date.isoformat()} "
                f"(shifted from {raw_date.isoformat()}{reason})"
            )
        else:
            summary_lines.append(
                f"{key}: {placed_date.isoformat()} (no shift)"
            )

    state_data["grammar_points"] = grammar_points

    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state_data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    return summary_lines


def main():
    parser = argparse.ArgumentParser(
        description="SRS load control — place review dates to prevent pile-ups"
    )
    parser.add_argument(
        "--state",
        default=".cowork/progress/grammar-state.json",
        help="Path to grammar-state.json",
    )
    parser.add_argument(
        "--today",
        default=None,
        help="Override today's date (ISO YYYY-MM-DD format)",
    )
    parser.add_argument(
        "--rules",
        default=".cowork/progress/load-control-rules.json",
        help="Path to load-control-rules.json (default: .cowork/progress/load-control-rules.json)",
    )
    args = parser.parse_args()

    state_path = Path(args.state)
    config = load_rules(args.rules)

    # Load holidays and store in config
    config.holidays = load_holidays(config.holidays_file)

    # Parse today
    if args.today:
        try:
            today = date.fromisoformat(args.today)
        except ValueError:
            print(f"Error: invalid date format: {args.today}", file=sys.stderr)
            sys.exit(1)
    else:
        today = date.today()

    # Read stdin
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            print("Error: empty input on stdin", file=sys.stderr)
            sys.exit(1)
        topics = json.loads(raw)
        if not isinstance(topics, list):
            print("Error: input must be a JSON array", file=sys.stderr)
            sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: malformed JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    # Validate each topic has a key
    for i, topic in enumerate(topics):
        if not isinstance(topic, dict) or "key" not in topic:
            print(
                f"Error: topic at index {i} missing 'key' field",
                file=sys.stderr,
            )
            sys.exit(1)

    # Read state file
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

    # Place topics
    results = place_topics(topics, grammar_points, today, config)

    # Merge and write
    summary_lines = merge_and_write(results, grammar_points, state_path, state_data, config)

    # Print summary
    for line in summary_lines:
        print(line)


if __name__ == "__main__":
    main()
