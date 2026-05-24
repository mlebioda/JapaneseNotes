#!/usr/bin/env python3
"""
grammar-process.py — Mechanical pre/post-processing for grammar-index/grammar/ files.

Implements update-grammar skill steps 1 and 9.

Usage:
    python3 grammar-process.py <file> [<file> ...]           # step 1 only
    python3 grammar-process.py --set-proofread <file> ...    # steps 1 + 9
    python3 grammar-process.py --dry-run <file> ...          # preview without writing

Step 1  Remove #w / #wc / #wp tag prefixes from content lines.
Step 9  Replace proofread: false → proofread: true in frontmatter.
        Only applied with --set-proofread (run after LLM review is complete).
"""

import re
import sys
from pathlib import Path

TAG_RE = re.compile(r'^#w[cp]? ')
PROOFREAD_RE = re.compile(r'^(proofread:\s*)false\s*$', re.MULTILINE)


def process_file(path, set_proofread=False, dry_run=False):
    content = Path(path).read_text(encoding='utf-8')
    original = content

    tags_removed = 0
    proofread_set = False

    lines = content.splitlines(keepends=True)
    new_lines = []
    for line in lines:
        stripped = TAG_RE.sub('', line)
        if stripped != line:
            tags_removed += 1
        new_lines.append(stripped)
    content = ''.join(new_lines)

    if set_proofread:
        new_content, count = PROOFREAD_RE.subn(r'\g<1>true', content)
        if count:
            content = new_content
            proofread_set = True

    changed = content != original
    if changed and not dry_run:
        Path(path).write_text(content, encoding='utf-8')

    return tags_removed, proofread_set, changed


def main():
    args = sys.argv[1:]
    dry_run = '--dry-run' in args
    set_proofread = '--set-proofread' in args
    files = [a for a in args if not a.startswith('--')]

    if not files:
        print(__doc__)
        sys.exit(0)

    for path in files:
        tags, proofread, changed = process_file(path, set_proofread, dry_run)
        status = 'DRY' if dry_run else ('updated' if changed else 'no changes')
        parts = []
        if tags:
            parts.append(f"tags removed: {tags}")
        if proofread:
            parts.append("proofread: true")
        detail = f" ({', '.join(parts)})" if parts else ''
        print(f"{path}: {status}{detail}")


if __name__ == '__main__':
    main()
