#!/usr/bin/env python3
"""
fill_extract.py — extract vocab lines and generate skeleton Summary block.

Usage:
    python3 fill_extract.py <lesson.md> <KanjiList.md>

What it does:
  - Extracts all #w / #wc / #wp lines from the lesson file
  - Deduplicates by Japanese field
  - Auto-applies #k tag via grep against KanjiList.md
  - Generates skeleton cards (blank conjugation / adjective fields for Claude to fill)
  - Appends the full # Summary block to the lesson file

Suru detection: if 'する' appears anywhere in the Japanese field → suru skeleton (no conjugation rows).
"""

import re
import sys

if len(sys.argv) < 3:
    print("Usage: fill_extract.py <lesson.md> <KanjiList.md>")
    sys.exit(1)

lesson_path = sys.argv[1]
kanji_path = sys.argv[2]

# --- Load kanji set ---
with open(kanji_path, encoding="utf-8") as f:
    kanji_set = set(line.strip() for line in f if line.strip())

def has_kanji(text):
    return any(c in kanji_set for c in text)

def strip_bold(s):
    return s.replace("**", "")

def is_suru(japanese):
    return "する" in japanese

def find_separator(rest):
    """
    Find the index of the ' - ' separator in a vocab line.
    Handles both ' - ' (space-dash-space) and 'X- ' (no leading space,
    e.g. after a closing bracket like ）or )).
    Returns (japanese, translation) or (None, None) if not found.
    """
    # Prefer ' - ' (standard)
    idx = rest.find(" - ")
    if idx >= 0:
        return rest[:idx].strip(), rest[idx + 3:].strip()
    # Fallback: dash preceded by a non-space char (e.g. ）- or )- )
    m = re.search(r"(\S)-\s+(.+)", rest)
    if m:
        japanese = rest[:m.start() + 1].strip()
        translation = m.group(2).strip()
        return japanese, translation
    return None, None

# --- Parse a single vocab line ---
def parse(raw_line):
    line = raw_line.strip()
    m = re.match(r"^(#w[cp]?)\s+(.+)", line)
    if not m:
        return None
    tag = m.group(1)
    rest = strip_bold(m.group(2))

    japanese, translation = find_separator(rest)
    if japanese is None:
        return None

    # Double-Japanese for #wc: e.g. "伝える（つた）- 伝える（つたえる）- Polish"
    if tag == "#wc":
        m2 = re.match(r"^([^\x00-\x7F].+?)\s+-\s+(.+)", translation)
        if m2:
            candidate = m2.group(1).strip()
            # Only accept if candidate looks Japanese (contains kana/kanji)
            if re.search(r"[぀-鿿]", candidate):
                japanese = candidate
                translation = m2.group(2).strip()

    # Strip ほんやく: prefix from translation field
    translation = re.sub(r"^ほんやく:\s*", "", translation)

    if not translation:
        return None

    return tag, japanese, translation


# --- Build skeleton card ---
def skeleton(tag, japanese, translation):
    k = "#k " if has_kanji(japanese) else ""
    header = f"{translation} {k}#card"

    if tag == "#w":
        return f"{header}\n{japanese}"

    if tag == "#wc":
        if is_suru(japanese):
            return f"{header}\nほんやく: {japanese}"
        return "\n".join([
            header,
            f"ほんやく: {japanese}",
            "て形: ",
            "た形: ",
            "ます形: ",
            "出す形 (start): ",
            "そう (looks): ",
            "お〜になる/special verb (honorific): ",
            "ない形: ",
            "なかった形: ",
            "あれる形 (passive/honorific): ",
            "使役形 (make/let): ",
            "ば形 (if): ",
            "可能形 (can): ",
            "おう形 (let's): ",
            "命令形 (imperative): ",
        ])

    if tag == "#wp":
        return "\n".join([
            header,
            f"ほんやく: {japanese}",
            "過去形: ",
            "否定形: ",
            "副詞形: ",
            "そう: ",
        ])


# --- Read lesson file ---
with open(lesson_path, encoding="utf-8") as f:
    content = f.read()

# Guard: abort if Rzeczowniki section already has content
if "Rzeczowniki:" in content:
    after = content.split("Rzeczowniki:", 1)[1].strip()
    if after and not after.startswith("---"):
        print("ERROR: Rzeczowniki section already filled. Aborting.")
        sys.exit(1)

# --- Pre-process: join multi-line vocab entries ---
# A #w/wc/wp line that has no ' - ' separator may continue on the next line
raw_lines = content.splitlines()
joined_lines = []
i = 0
while i < len(raw_lines):
    line = raw_lines[i]
    if re.match(r"^#w[cp]?\s+", line.strip()):
        stripped = strip_bold(line)
        j, _ = find_separator(stripped)
        if j is None and i + 1 < len(raw_lines):
            # Continuation: merge with next line
            line = line.rstrip() + raw_lines[i + 1]
            i += 1
    joined_lines.append(line)
    i += 1

# --- Extract cards ---
seen = set()
cards = []

for raw_line in joined_lines:
    result = parse(raw_line)
    if result is None:
        continue
    tag, japanese, translation = result
    if japanese in seen:
        continue
    seen.add(japanese)
    card = skeleton(tag, japanese, translation)
    if card:
        cards.append(card)

if not cards:
    print("No vocab lines found.")
    sys.exit(0)

# --- Build summary block ---
summary_block = (
    "\n# Summary\n\n"
    " ---\n\n\n"
    + "\n\n".join(cards)
    + "\n\n\n ---\n\n\n"
)

# Remove existing empty # Summary if present
content_trimmed = re.sub(r"\n# Summary\s*$", "", content.rstrip())

with open(lesson_path, "w", encoding="utf-8") as f:
    f.write(content_trimmed + "\n" + summary_block)

print(f"Done. {len(cards)} cards written.")
