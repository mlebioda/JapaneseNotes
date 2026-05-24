#!/usr/bin/env python3
"""
furigana-convert.py — Convert trailing furigana to inline format in markdown files.

Trailing format:  日本語（よみ1、よみ2）
Inline format:    日本(にほん)語(ご)

Usage:
    python3 furigana-convert.py <file> [<file> ...]  # convert files in-place
    python3 furigana-convert.py --dry-run <file> ... # print changes without writing

Rules (matching update-grammar skill step 3):
- Detects trailing （r1、r2） or (r1, r2) reading lists at the end of the Japanese portion
- Matches readings to maximal CJK runs left-to-right
- Skips lines already in inline format (no trailing list)
- Skips lines inside ## Structure / ### Structure sections
- Logs a warning if reading count != kanji-group count; leaves line unchanged
- Lines with no kanji: skipped
"""

import re
import sys
from pathlib import Path

CJK_RE = re.compile(r'[一-鿿]+')

# Patterns for trailing reading list (fullwidth or ASCII parens)
TRAILING_FW = re.compile(r'（([^）]+)）([ \t]*-.*)?$')
TRAILING_AS = re.compile(r'\(([^)]+)\)([ \t]*-.*)?$')


def find_kanji_groups(text):
    return [(m.start(), m.end(), m.group()) for m in CJK_RE.finditer(text)]


def convert_line(line, in_structure=False):
    """Return (new_line, warning_or_None). new_line == line if no change."""
    if in_structure:
        return line, None

    m = TRAILING_FW.search(line) or TRAILING_AS.search(line)
    if not m:
        return line, None

    reading_str = m.group(1)
    readings = [r.strip() for r in re.split(r'[、,]', reading_str)]
    suffix = m.group(2) or ''
    prefix = line[:m.start()]

    groups = find_kanji_groups(prefix)
    if not groups:
        return line, None

    if len(groups) != len(readings):
        return line, (
            f"reading count mismatch: {repr(line.strip())} "
            f"(kanji groups={len(groups)}, readings={len(readings)})"
        )

    parts = []
    last = 0
    for i, (start, end, kanji) in enumerate(groups):
        parts.append(prefix[last:start])
        parts.append(f"{kanji}({readings[i]})")
        last = end
    parts.append(prefix[last:])
    parts.append(suffix)
    return ''.join(parts), None


def convert_file(path, dry_run=False):
    text = Path(path).read_text(encoding='utf-8')
    lines = text.splitlines(keepends=True)

    new_lines = []
    changed = False
    warnings = []
    converted = 0
    in_structure = False

    for line in lines:
        stripped = line.rstrip('\n')
        if re.match(r'^#{2,3} Structure', stripped):
            in_structure = True
        elif re.match(r'^## ', stripped) and not re.match(r'^## Structure', stripped):
            in_structure = False

        new_stripped, warn = convert_line(stripped, in_structure)
        if warn:
            warnings.append(warn)
        if new_stripped != stripped:
            changed = True
            converted += 1
        new_lines.append(new_stripped + ('\n' if line.endswith('\n') else ''))

    if changed and not dry_run:
        Path(path).write_text(''.join(new_lines), encoding='utf-8')

    return converted, warnings, changed


def main():
    args = sys.argv[1:]
    dry_run = '--dry-run' in args
    files = [a for a in args if not a.startswith('--')]

    if not files:
        print(__doc__)
        sys.exit(0)

    for path in files:
        converted, warnings, changed = convert_file(path, dry_run)
        status = 'DRY' if dry_run else ('updated' if changed else 'no changes')
        print(f"{path}: {status} (furigana converted: {converted})")
        for w in warnings:
            print(f"  [WARN] {w}")


if __name__ == '__main__':
    main()
