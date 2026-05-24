#!/usr/bin/env python3
"""
grammar-audit.py — Integrity check for grammar-index/grammar/ files.

Run from the vault root directory.

Checks:
  1. Orphans        — grammar files with no entry in any topic file
  2. Broken links   — topic file entries pointing to non-existent grammar files
  3. Slug mismatch  — topic_slug frontmatter doesn't match actual topic entries
  4. Missing ##Examples section
  5. proofread: false — status report (not an error)

Usage:
    python3 .claude/scripts/grammar-audit.py
    python3 .claude/scripts/grammar-audit.py --verbose
"""

import json
import re
import sys
from pathlib import Path

ENTRY_RE = re.compile(r'\[.+?\]\(/JapaneseNotes/grammar-index/grammar/([^)]+)\)')
TOPIC_SLUG_RE = re.compile(r'^topic_slug:\s*(.+)$', re.MULTILINE)
PROOFREAD_RE = re.compile(r'^proofread:\s*(true|false)', re.MULTILINE)
EXAMPLES_RE = re.compile(r'^## Examples', re.MULTILINE)
SUBTOPICS_RE = re.compile(r'^## Sub-topics', re.MULTILINE)
SUBTOPICS_RE = re.compile(r'^## Sub-topics', re.MULTILINE)


def parse_topic_slug(content):
    m = TOPIC_SLUG_RE.search(content)
    if not m:
        return set()
    val = m.group(1).strip()
    try:
        parsed = json.loads(val)
        return set(parsed) if isinstance(parsed, list) else {str(parsed)}
    except (json.JSONDecodeError, ValueError):
        stripped = val.strip('"').strip("'")
        return {stripped} if stripped else set()


def entries_in_topic(content):
    m = re.search(r'^## Entries\n(.+?)(?=^## |\Z)', content, re.MULTILINE | re.DOTALL)
    if not m:
        return []
    return ENTRY_RE.findall(m.group(1))


def main():
    verbose = '--verbose' in sys.argv

    grammar_dir = Path('grammar-index/grammar')
    topic_dir = Path('grammar-index')

    if not grammar_dir.exists():
        print("Error: grammar-index/grammar/ not found. Run from vault root.")
        sys.exit(1)

    grammar_files = {f.stem: f for f in sorted(grammar_dir.glob('*.md'))}
    topic_files = {
        f.stem: f for f in sorted(topic_dir.glob('*.md'))
        if f.name != 'index.md' and f.parent == topic_dir
    }

    # topic → set of grammar slugs it contains
    topic_to_slugs = {}
    for stem, path in topic_files.items():
        topic_to_slugs[stem] = set(entries_in_topic(path.read_text(encoding='utf-8')))

    # grammar slug → set of topics that reference it
    slug_to_topics = {slug: set() for slug in grammar_files}
    broken_links = []

    for topic_stem, slugs in topic_to_slugs.items():
        for slug in slugs:
            if slug in slug_to_topics:
                slug_to_topics[slug].add(topic_stem)
            else:
                broken_links.append((topic_stem, slug))

    orphans, mismatches, missing_examples, not_proofread = [], [], [], []

    for slug, path in grammar_files.items():
        content = path.read_text(encoding='utf-8')

        if not slug_to_topics[slug]:
            orphans.append(slug)

        declared = parse_topic_slug(content)
        actual = slug_to_topics[slug]
        if declared and declared != actual:
            mismatches.append((slug, declared, actual))

        is_container = bool(SUBTOPICS_RE.search(content))
        if not is_container and not EXAMPLES_RE.search(content):
            missing_examples.append(slug)

        m = PROOFREAD_RE.search(content)
        if m and m.group(1) == 'false':
            not_proofread.append(slug)

    total = len(grammar_files)
    errors = len(orphans) + len(broken_links) + len(mismatches) + len(missing_examples)

    print(f"grammar-audit — {total} file(s) checked\n")

    def section(label, items, fmt=None):
        mark = '✗' if items else '✓'
        print(f"  {mark}  {label}: {len(items)}")
        if verbose and items:
            for item in items:
                print(f"       → {fmt(item) if fmt else item}")

    section("Orphans (no topic entry)", orphans)
    section(
        "Broken topic links (entry → missing file)", broken_links,
        lambda x: f"{x[0]}.md → missing grammar/{x[1]}.md"
    )
    section(
        "topic_slug mismatches", mismatches,
        lambda x: f"{x[0]}.md  declared={sorted(x[1])}  actual={sorted(x[2])}"
    )
    section("Missing ## Examples", missing_examples)
    print()
    section(f"proofread: false (not yet reviewed)", not_proofread)

    print()
    if errors:
        status = f"{errors} issue(s) found."
        if not verbose:
            status += " Run with --verbose for details."
        print(f"  {status}")
    else:
        print("  All checks passed.")

    sys.exit(1 if errors else 0)


if __name__ == '__main__':
    main()
