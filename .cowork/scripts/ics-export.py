#!/usr/bin/env python3
"""
ICS calendar export for Japanese grammar reviews.

Two modes:
  session — reads grammar point keys from stdin, exports those points' next_review dates
  full    — exports all future review dates + holiday events

Usage:
  echo '["key-A","key-B"]' | python3 ics-export.py --mode session --state state.json --output out.ics
  python3 ics-export.py --mode full --state state.json --holidays holidays.json --output out.ics --today 2026-06-19
"""

import argparse
import json
import sys
import uuid
from datetime import date, datetime, timedelta
from pathlib import Path


# ---------------------------------------------------------------------------
# RFC 5545 line folding
# ---------------------------------------------------------------------------

def fold(line: str) -> str:
    """RFC 5545 line folding: max 75 octets per line, SPACE continuation prefix.

    Encodes the line as UTF-8, splits at 75-octet boundaries (first line) and
    74-octet boundaries (continuation lines, reserving 1 octet for the SPACE
    prefix), ensuring no multi-byte character is split mid-sequence.
    """
    encoded = line.encode("utf-8")
    if len(encoded) <= 75:
        return line

    parts = []
    # First line: up to 75 octets
    first_limit = 75
    cut = first_limit
    # Don't split in the middle of a multi-byte UTF-8 character
    while cut > 0 and (encoded[cut] & 0xC0) == 0x80:
        cut -= 1
    parts.append(encoded[:cut].decode("utf-8", errors="ignore"))
    remaining = encoded[cut:]

    # Continuation lines: SPACE prefix (1 octet) + up to 74 octets of content
    cont_limit = 74
    while len(remaining) > 0:
        cut = min(cont_limit, len(remaining))
        if cut < len(remaining):
            while cut > 0 and (remaining[cut] & 0xC0) == 0x80:
                cut -= 1
        chunk = remaining[:cut].decode("utf-8", errors="ignore")
        parts.append(" " + chunk)
        remaining = remaining[cut:]

    return "\r\n".join(parts)


# ---------------------------------------------------------------------------
# VEVENT / VCALENDAR builders
# ---------------------------------------------------------------------------

def build_vevent(dtstart: str, dtend: str, summary: str, description: str, uid: str) -> list:
    """Build ICS content lines for one VEVENT block.

    Args:
        dtstart: YYYYMMDD date string
        dtend: YYYYMMDD date string (typically dtstart + 1 day)
        summary: event summary text
        description: event description (literal \\n for ICS line breaks)
        uid: unique identifier for the event

    Returns:
        List of unfolded ICS content lines.
    """
    return [
        "BEGIN:VEVENT",
        f"DTSTART;VALUE=DATE:{dtstart}",
        f"DTEND;VALUE=DATE:{dtend}",
        f"SUMMARY:{summary}",
        f"DESCRIPTION:{description}",
        f"UID:{uid}",
        "END:VEVENT",
    ]


def build_vcalendar(events: list) -> list:
    """Wrap VEVENT line-lists in a VCALENDAR header/footer.

    Args:
        events: list of VEVENT line-lists (each from build_vevent)

    Returns:
        Flat list of ICS content lines for the complete calendar.
    """
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Japanese Grammar Review//EN",
        "CALSCALE:GREGORIAN",
    ]
    for event in events:
        lines.extend(event)
    lines.append("END:VCALENDAR")
    return lines


# ---------------------------------------------------------------------------
# Data loaders
# ---------------------------------------------------------------------------

def load_session_points(state_path: str, keys: list) -> dict:
    """Read grammar-state.json, filter to entries matching keys, group by next_review.

    Args:
        state_path: path to grammar-state.json
        keys: list of grammar point keys to include

    Returns:
        Dict of {date_str: [grammar_header, ...]}
    """
    with open(state_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    grammar_points = data.get("grammar_points", {})
    grouped = {}
    for key in keys:
        entry = grammar_points.get(key)
        if entry is None:
            continue
        review_date = entry.get("next_review")
        header = entry.get("grammar_header", key)
        if review_date is None:
            continue
        grouped.setdefault(review_date, []).append(header)
    return grouped


def load_full_points(state_path: str, today: str) -> dict:
    """Read grammar-state.json, filter to next_review >= today, group by date.

    Args:
        state_path: path to grammar-state.json
        today: ISO date string (YYYY-MM-DD) for the cutoff

    Returns:
        Dict of {date_str: [grammar_header, ...]}
    """
    with open(state_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    grammar_points = data.get("grammar_points", {})
    grouped = {}
    for key, entry in grammar_points.items():
        review_date = entry.get("next_review")
        if review_date is None:
            continue
        if review_date < today:
            continue
        header = entry.get("grammar_header", key)
        grouped.setdefault(review_date, []).append(header)
    return grouped


def load_holidays(holidays_path: str, today: str) -> list:
    """Read holidays.json, return sorted list of holiday dates >= today.

    Args:
        holidays_path: path to holidays.json (JSON array of ISO date strings)
        today: ISO date string (YYYY-MM-DD) for the cutoff

    Returns:
        Sorted list of future holiday date strings. Empty list if file missing.
    """
    try:
        with open(holidays_path, "r", encoding="utf-8") as f:
            holidays = json.load(f)
    except FileNotFoundError:
        return []

    return sorted(d for d in holidays if d >= today)


# ---------------------------------------------------------------------------
# ICS file writer
# ---------------------------------------------------------------------------

def write_ics(path: str, lines: list) -> None:
    """Fold each line and write to file with CRLF line endings.

    Args:
        path: output file path
        lines: list of unfolded ICS content lines
    """
    folded_lines = [fold(line) for line in lines]
    content = "\r\n".join(folded_lines) + "\r\n"
    with open(path, "wb") as f:
        f.write(content.encode("utf-8"))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _next_day(yyyymmdd: str) -> str:
    """Return the day after a YYYYMMDD date string, also as YYYYMMDD."""
    d = datetime.strptime(yyyymmdd, "%Y%m%d").date()
    return (d + timedelta(days=1)).strftime("%Y%m%d")


def _iso_to_yyyymmdd(iso_date: str) -> str:
    """Convert YYYY-MM-DD to YYYYMMDD."""
    return iso_date.replace("-", "")


def _uid_fragment() -> str:
    """Return an 8-character UUID fragment."""
    return uuid.uuid4().hex[:8]


# ---------------------------------------------------------------------------
# Main / CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="ICS calendar export for grammar reviews")
    parser.add_argument("--mode", required=True, choices=["session", "full"],
                        help="Export mode: session (stdin keys) or full (all future)")
    parser.add_argument("--state", default=".cowork/progress/grammar-state.json",
                        help="Path to grammar-state.json")
    parser.add_argument("--holidays", default=".cowork/progress/holidays.json",
                        help="Path to holidays.json (full mode only)")
    parser.add_argument("--output", required=True,
                        help="Output .ics file path")
    parser.add_argument("--today", default=None,
                        help="ISO date for today (YYYY-MM-DD), defaults to actual today. "
                             "Used in full mode only; ignored in session mode.")
    args = parser.parse_args()

    if args.mode == "session":
        _run_session(args)
    else:
        _run_full(args)


def _run_session(args):
    """Session mode: read keys from stdin, export their review dates."""
    # Read stdin
    stdin_data = sys.stdin.read().strip()
    if not stdin_data:
        print("No keys provided", file=sys.stderr)
        sys.exit(1)

    try:
        keys = json.loads(stdin_data)
    except json.JSONDecodeError as e:
        print(f"Error: malformed JSON on stdin: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(keys, list) or len(keys) == 0:
        print("No keys provided", file=sys.stderr)
        sys.exit(1)

    # Load state — session mode requires valid state
    if not Path(args.state).exists():
        print(f"Error: state file not found: {args.state}", file=sys.stderr)
        sys.exit(1)

    try:
        grouped = load_session_points(args.state, keys)
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print(f"Error: malformed state file: {e}", file=sys.stderr)
        sys.exit(1)

    # Build timestamp for UIDs
    session_ts = datetime.now().strftime("%Y%m%dT%H%M%S")

    # Build events
    events = []
    for review_date, headers in sorted(grouped.items()):
        dtstart = _iso_to_yyyymmdd(review_date)
        dtend = _next_day(dtstart)
        n = len(headers)
        summary = f"Japanese Grammar Review — {n} point(s)"
        description = "\\n".join(headers)
        uid = f"{dtstart}-{session_ts}-{_uid_fragment()}@japanese-notes"
        events.append(build_vevent(dtstart, dtend, summary, description, uid))

    # Build calendar and write
    cal_lines = build_vcalendar(events)
    write_ics(args.output, cal_lines)

    n_events = len(events)
    print(f"Written {n_events} event(s) to {args.output}")


def _run_full(args):
    """Full mode: export all future review dates + holidays."""
    today_str = args.today or date.today().isoformat()

    # Load state — full mode is graceful on missing/malformed state
    grouped = {}
    if not Path(args.state).exists():
        print(f"Warning: state file not found: {args.state}", file=sys.stderr)
    else:
        try:
            grouped = load_full_points(args.state, today_str)
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            print(f"Warning: malformed state file, treating as empty: {e}", file=sys.stderr)

    # Build review events
    events = []
    for review_date, headers in sorted(grouped.items()):
        dtstart = _iso_to_yyyymmdd(review_date)
        dtend = _next_day(dtstart)
        n = len(headers)
        summary = f"Japanese Grammar Review — {n} point(s)"
        description = "\\n".join(headers)
        uid = f"{dtstart}-full-export-{_uid_fragment()}@japanese-notes"
        events.append(build_vevent(dtstart, dtend, summary, description, uid))

    # Load holidays — graceful on missing/malformed
    holidays = []
    try:
        holidays = load_holidays(args.holidays, today_str)
    except (json.JSONDecodeError, TypeError) as e:
        print(f"Warning: malformed holidays file, treating as empty: {e}", file=sys.stderr)

    # Build holiday events
    for holiday_date in holidays:
        dtstart = _iso_to_yyyymmdd(holiday_date)
        dtend = _next_day(dtstart)
        summary = "Holiday — No Review"
        description = "Holiday — no grammar reviews scheduled."
        uid = f"{dtstart}-holiday-{_uid_fragment()}@japanese-notes"
        events.append(build_vevent(dtstart, dtend, summary, description, uid))

    # Build calendar and write
    cal_lines = build_vcalendar(events)
    write_ics(args.output, cal_lines)

    n_events = len(events)
    print(f"Written {n_events} event(s) to {args.output}")


if __name__ == "__main__":
    main()
