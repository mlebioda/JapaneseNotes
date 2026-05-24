---
name: feedback-extract-grammar-efficiency
description: User feedback on extract-grammar taking too long — act sooner, plan less in advance, grep exact bytes before computing slugs
metadata:
  type: feedback
---

Don't pre-plan all slugs, file contents, and topic mappings in the reasoning layer before creating any files. Start creating files immediately and classify topics as you go.

**Why:** In UN5GL6 session, computing all 19 slugs + contents + topic maps upfront consumed thousands of tokens before a single file was written. User explicitly called this out.

**How to apply:**
- Create the first grammar file as soon as classification is confirmed
- Compute slugs one at a time as each file is written, not all at once
- For headings with Polish/non-ASCII characters, grep the exact bytes from the file before computing the slug — do not rely on reading the heading from awk output (encoding differences cause typos). The `wsiąć` → `wsiąić` slug bug was caused by this.
- Lessons with a `## Grammar` section that mirrors `## 文法` + `## Vocabulary` require a targeted Python script for wikilink insertion (only process from `## 文法` onwards). Note this early rather than solving it silently deep in reasoning.
