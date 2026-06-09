#!/usr/bin/env python3
"""
kanji-links.py — Generate kanji-trainer.org <a href> lines for a given text.

Usage:
    python3 .cowork/scripts/kanji-links.py "<source_text>"

The caller is responsible for stripping furigana from source_text before
passing it. This script only scans for CJK Unified Ideographs (U+4E00–U+9FFF).

Output:
    One line per unique kanji (first-occurrence order), e.g.:
        <a href="https://kanji-trainer.org/Mnemonic_phrase/Mnemonic_食.html">食</a>

Exit codes:
    0 — success (including when no kanji are found; output will be empty)
    1 — wrong number of arguments
"""

import sys


def extract_kanji_links(text: str) -> list[str]:
    """Return a list of <a href> lines, one per unique CJK character (U+4E00-U+9FFF),
    in first-occurrence order."""
    seen: set[str] = set()
    links: list[str] = []
    for ch in text:
        code = ord(ch)
        if 0x4E00 <= code <= 0x9FFF and ch not in seen:
            seen.add(ch)
            links.append(
                f'<a href="https://kanji-trainer.org/Mnemonic_phrase/Mnemonic_{ch}.html">{ch}</a>'
            )
    return links


def main() -> None:
    if len(sys.argv) != 2:
        print(
            "Usage: python3 kanji-links.py \"<source_text>\"",
            file=sys.stderr,
        )
        sys.exit(1)

    source_text = sys.argv[1]
    for line in extract_kanji_links(source_text):
        print(line)


if __name__ == "__main__":
    main()
