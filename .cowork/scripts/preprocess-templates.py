#!/usr/bin/env python3
"""
preprocess-templates.py

Applies all alias-table label renames to the # Summary section of a lesson file.
Reads label-aliases.json from ../skills/references/label-aliases.json (relative to this script).
Lines above # Summary are copied verbatim. <!--ID:--> lines are never touched.
Uses atomic write (os.replace) to avoid partial writes.

Usage:
    python preprocess-templates.py <lesson-file-path>
"""

import json
import os
import sys
import tempfile


def is_ascii_only(s):
    """Return True if all characters in s are ASCII (no Japanese/CJK)."""
    try:
        s.encode("ascii")
        return True
    except UnicodeEncodeError:
        return False


def load_aliases(script_dir):
    aliases_path = os.path.join(script_dir, "..", "skills", "references", "label-aliases.json")
    aliases_path = os.path.normpath(aliases_path)
    if not os.path.isfile(aliases_path):
        print(f"ERROR: label-aliases.json not found at: {aliases_path}", file=sys.stderr)
        sys.exit(1)
    with open(aliases_path, "r", encoding="utf-8") as f:
        return json.load(f)


def try_lookup(label_with_colon, aliases):
    """
    Look up label_with_colon in aliases.
    Case-sensitive first. If no match and key is ASCII-only, retry with .lower().
    Returns the canonical label (with colon) or None.
    """
    # Exact match
    if label_with_colon in aliases:
        return aliases[label_with_colon]
    # Case-insensitive retry only for ASCII keys
    if is_ascii_only(label_with_colon):
        lower_key = label_with_colon.lower()
        for variant, canonical in aliases.items():
            if is_ascii_only(variant) and variant.lower() == lower_key:
                return canonical
    return None


def process_line(line, aliases, replacement_counts):
    """
    Process a single line from below # Summary.
    - Lines starting with <!-- are returned verbatim.
    - Otherwise: try to match the label portion to an alias; replace if found.
    Returns the (possibly modified) line.
    """
    stripped = line.rstrip("\n")

    # Never touch <!--ID:--> or any HTML comment lines
    if stripped.lstrip().startswith("<!--"):
        return line

    # Try to extract a label: text before the first ':'
    colon_pos = stripped.find(":")
    if colon_pos < 0:
        return line  # No colon at all — not a label line

    label_text = stripped[:colon_pos].strip()
    if not label_text:
        return line  # Empty label

    label_with_colon = label_text + ":"
    canonical = try_lookup(label_with_colon, aliases)
    if canonical is None:
        return line  # No alias match

    # Build the replacement: canonical label + rest of line after the original label+colon
    rest = stripped[colon_pos + 1:]  # everything after the ':'
    new_line = canonical + rest + "\n"

    if new_line != line:
        canonical_key = canonical
        replacement_counts[canonical_key] = replacement_counts.get(canonical_key, 0) + 1

    return new_line


def main():
    if len(sys.argv) != 2:
        print("Usage: python preprocess-templates.py <lesson-file-path>", file=sys.stderr)
        sys.exit(1)

    target_path = sys.argv[1]
    if not os.path.isfile(target_path):
        print(f"ERROR: File not found: {target_path}", file=sys.stderr)
        sys.exit(1)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    aliases = load_aliases(script_dir)

    with open(target_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Find # Summary line
    summary_idx = None
    for i, line in enumerate(lines):
        if line.rstrip("\n") == "# Summary":
            summary_idx = i
            break

    if summary_idx is None:
        print("ERROR: '# Summary' heading not found in file. Aborting without writing.", file=sys.stderr)
        sys.exit(1)

    replacement_counts = {}
    output_lines = []

    for i, line in enumerate(lines):
        if i <= summary_idx:
            # Lines up to and including # Summary: copy verbatim
            output_lines.append(line)
        else:
            output_lines.append(process_line(line, aliases, replacement_counts))

    # Atomic write: write to temp file in same directory, then os.replace
    target_dir = os.path.dirname(os.path.abspath(target_path))
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=target_dir, delete=False, suffix=".tmp"
    ) as tmp:
        tmp_path = tmp.name
        tmp.writelines(output_lines)

    os.replace(tmp_path, target_path)

    # Print summary
    total_changed = sum(replacement_counts.values())
    if total_changed == 0:
        print("preprocess-templates: no label renames needed.")
    else:
        print(f"preprocess-templates: {total_changed} label(s) renamed.")
        for canonical, count in sorted(replacement_counts.items()):
            print(f"  {count}x → {canonical}")


if __name__ == "__main__":
    main()
