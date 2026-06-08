#!/usr/bin/env python3
"""
fix_kanji_links.py

For each Kaligrafia-1 through Kaligrafia-5 file:
- Processes only content below "# Summary"
- Finds #wc / #wp card blocks (identified by having a "ほんやく:" line followed by
  conjugation/adjective form lines like "ます形:", "過去形:", etc.)
- Extracts kanji ONLY from the ほんやく: value (strips prefix and furigana)
- Rewrites the <a href="...">X</a> lines after the last form line to use only those kanji
- Does NOT touch anything above "# Summary"
- Does NOT touch <!--ID:--> lines
- Does NOT change form values
"""

import re
import os

VAULT_ROOT = "/Users/michallebioda/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianJP"

TARGET_FILES = [
    "JPLessons/Udemy/N4/Kaligrafia/Kaligrafia-1-Company.md",
    "JPLessons/Udemy/N4/Kaligrafia/Kaligrafia-2-Study.md",
    "JPLessons/Udemy/N4/Kaligrafia/Kaligrafia-3-Family.md",
    "JPLessons/Udemy/N4/Kaligrafia/Kaligrafia-4-Meal.md",
    "JPLessons/Udemy/N4/Kaligrafia/Kaligrafia-5-Shopping.md",
]

# Form line prefixes that indicate this is a #wc/#wp block
FORM_PREFIXES = (
    "ます形:",
    "て形:",
    "た形:",
    "ない形:",
    "なかった形:",
    "ば形",
    "可能形",
    "られる形",
    "出す形",
    "尊敬語",
    "お〜になる",
    "そう",
    "おう",
    "過去形:",
    "否定形:",
    "副詞形:",
)

KANJI_LINK_RE = re.compile(r'<a href="https://kanji-trainer\.org/Mnemonic_phrase/Mnemonic_(.+?)\.html">.+?</a>')

CJK_RANGE = re.compile(r'[一-鿿]')

# Furigana patterns to strip from ほんやく: value
FURIGANA_FULL = re.compile(r'（[^）]*）')   # full-width parens
FURIGANA_HALF = re.compile(r'\([^\)]*\)')   # half-width parens


def extract_kanji_from_honnyaku(honnyaku_line: str) -> list:
    """
    Given a raw "ほんやく: X（Y）" line:
    1. Strip the "ほんやく:" prefix
    2. Strip furigana (both full-width and half-width parens)
    3. Collect unique CJK kanji in left-to-right order
    """
    value = honnyaku_line.strip()
    # Strip the "ほんやく:" prefix
    if value.startswith("ほんやく:"):
        value = value[len("ほんやく:"):]
    value = value.strip()

    # Strip furigana
    value = FURIGANA_FULL.sub('', value)
    value = FURIGANA_HALF.sub('', value)

    # Collect unique CJK kanji in order
    seen = set()
    kanji_list = []
    for ch in value:
        if CJK_RANGE.match(ch) and ch not in seen:
            seen.add(ch)
            kanji_list.append(ch)

    return kanji_list


def build_kanji_links(kanji_list: list) -> list:
    """Build <a href="...">X</a> lines for each kanji."""
    lines = []
    for k in kanji_list:
        lines.append(f'<a href="https://kanji-trainer.org/Mnemonic_phrase/Mnemonic_{k}.html">{k}</a>')
    return lines


def is_form_line(line: str) -> bool:
    stripped = line.strip()
    return any(stripped.startswith(p) for p in FORM_PREFIXES)


def is_kanji_link_line(line: str) -> bool:
    return bool(KANJI_LINK_RE.match(line.strip()))


def process_file(filepath: str) -> bool:
    """
    Process a single file. Returns True if the file was modified.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.splitlines(keepends=True)

    # Find the # Summary line index
    summary_idx = None
    for i, line in enumerate(lines):
        if line.strip() == "# Summary":
            summary_idx = i
            break

    if summary_idx is None:
        print(f"  WARNING: No '# Summary' found in {filepath} — skipping.")
        return False

    # Safety check: no <!--ID:--> lines (should be 0 per our earlier check, but be safe)
    for line in lines:
        if "<!--ID:" in line:
            print(f"  ERROR: <!--ID:--> found in {filepath} — aborting to protect Anki sync anchors.")
            return False

    # We only process lines below summary_idx
    # Work on the "below summary" section as a list of lines
    above = lines[:summary_idx + 1]
    below = lines[summary_idx + 1:]

    modified = False

    # State machine to find #wc/#wp card blocks
    # A block is identified by: has a "ほんやく:" line AND has at least one form line
    # After the last form line, there may be consecutive <a ...> lines to replace

    i = 0
    while i < len(below):
        line = below[i]

        # Look for a ほんやく: line
        if line.strip().startswith("ほんやく:"):
            honnyaku_line = line.strip()
            honnyaku_idx = i

            # Scan forward to find form lines and the block of <a> links
            j = i + 1
            last_form_idx = None
            while j < len(below):
                l = below[j].strip()
                if is_form_line(below[j]):
                    last_form_idx = j
                    j += 1
                elif l == "" or l == "---" or (l.startswith("#") and not is_kanji_link_line(below[j])):
                    # End of block (blank line, separator, or new section)
                    break
                elif is_kanji_link_line(below[j]):
                    # Kanji link lines — skip for now, we'll replace them
                    j += 1
                else:
                    # Other content lines (e.g., the honnyaku line itself is already at i)
                    j += 1

            if last_form_idx is None:
                # No form lines found — not a #wc/#wp block, skip
                i += 1
                continue

            # Now find the consecutive <a> link block immediately after last_form_idx
            link_start = last_form_idx + 1
            link_end = link_start

            # Skip any non-link lines between last form and links (shouldn't happen but be safe)
            while link_end < len(below) and not is_kanji_link_line(below[link_end]):
                stripped = below[link_end].strip()
                if stripped == "" or stripped == "---":
                    break
                link_end += 1

            # Now consume consecutive link lines
            link_block_start = link_end
            link_block_end = link_end
            while link_block_end < len(below) and is_kanji_link_line(below[link_block_end]):
                link_block_end += 1

            # Extract correct kanji from ほんやく: line
            correct_kanji = extract_kanji_from_honnyaku(honnyaku_line)
            correct_links = build_kanji_links(correct_kanji)

            # Get existing link targets
            existing_links = [below[k].strip() for k in range(link_block_start, link_block_end)]

            # Build what we want
            # Preserve line endings from the context (use \n)
            new_link_lines = [lnk + "\n" for lnk in correct_links]

            if existing_links != correct_links:
                # Replace the link block
                below[link_block_start:link_block_end] = new_link_lines
                modified = True
                print(f"  Fixed block at line ~{summary_idx + 1 + honnyaku_idx + 1}:")
                print(f"    ほんやく: {honnyaku_line}")
                print(f"    Old links: {existing_links}")
                print(f"    New links: {correct_links}")
                # Jump past the newly inserted lines
                i = link_block_start + len(new_link_lines)
            else:
                i = link_block_end

            continue

        i += 1

    if modified:
        new_content = "".join(above + below)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  => Written: {filepath}")
    else:
        print(f"  => No changes needed: {filepath}")

    return modified


def main():
    total_modified = 0
    for rel_path in TARGET_FILES:
        filepath = os.path.join(VAULT_ROOT, rel_path)
        print(f"\nProcessing: {rel_path}")
        if not os.path.exists(filepath):
            print(f"  ERROR: File not found: {filepath}")
            continue
        changed = process_file(filepath)
        if changed:
            total_modified += 1

    print(f"\nDone. {total_modified}/{len(TARGET_FILES)} file(s) modified.")


if __name__ == "__main__":
    main()
