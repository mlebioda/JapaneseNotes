---
name: grammar-summary
description: >
  Extract grammar headers from all N5 Grammar lesson files and write a structured
  summary with backlinks and topic grouping to a destination file.
  Trigger: user says "grammar summary [filename]", "build grammar summary", or similar.
---

# Grammar Summary Skill

## Trigger

User provides a **destination filename** (e.g. `Gramatyka/Grammar-N5.md`).
If the user provides no path, save to `Gramatyka/<filename>.md`.

---

## Workflow

1. List all `.md` files (not `.bak`) in `JPLessons/Udemy/N5/Gramatyka/`
2. For each file: extract headers from the `文法` section (see **Extraction rules**)
3. Collect all results into a flat list with source metadata
4. Group by topic (see **Grouping rules**)
5. Write output to destination file (see **Output format**)
6. No confirmation needed — write directly

---

## Extraction rules

### Finding the 文法 section

Search for a line matching `^#+ 文法` (any heading level: `#`, `##`, `###`).
Collect all lines from that heading until the next heading of the **same or higher** level.

### Building the header tree

Within the 文法 section, collect every heading line (`##`, `###`, `####`, etc.).
Preserve the original heading level — they represent a hierarchy.

### Deciding what to include

For each heading, look at its body (content between it and the next heading of same/higher level):

- **Has own text content** (regular prose, tables, code blocks — not counting subheadings):
  → **Keep** the heading.
- **Has only subheadings, no own text**:
  → **Skip** this heading, promote its children up one level.

This means: if `### Proposing something to someone` contains both explanation text *and* `####` subheadings — keep it. If `### Verbs` contains only `#### 勉強 - learn`, `#### 住む - to live` etc. with no text of its own — skip it and surface the `####` headers directly.

### Backlink

Under every extracted heading (at its destination level), add a wikilink:
```
[[SourceFilename#Exact header text]]
```
where `SourceFilename` is the file's base name without `.md` extension.

---

## Output format

```markdown
# Topic Name

## Grammar Point
[[SourceFile#Grammar Point]]

### Subpoint
[[SourceFile#Subpoint]]

---

# Another Topic

## Grammar Point from different file
[[AnotherFile#Grammar Point]]
```

- Topics use `#` level
- Extracted headings keep their relative hierarchy but are shifted so the shallowest extracted heading becomes `##`
- Separate topics with `---`
- Within a topic, group entries from different source files under a brief `> From: [[SourceFile]]` quote line for readability

---

## Grouping rules

After collecting all extracted headers, analyze their content and group into **topics**.
Suggested topics (not exhaustive — use your judgment):

- **Verb forms** — て形, た形, ない形, ます形, dictionary form, ている, conjugation tables
- **Verb patterns** — ませんか, ましょう, てもいいです, てはいけません, なければなりません, なくてもいい, たりします, ながら, とき, てください, Vないでください
- **Particles** — は, が, を, に, へ, で, から, まで, よ, ね, か/も combinations
- **Adjectives** — い形容詞, な形容詞, forms, comparisons
- **Comparisons** — より, の方が, の中で一番, どちら
- **Counters** — 枚, 個, 名, 匹, 杯, 本, 冊, 台, 回, people/floor counters
- **Numbers & Time** — numbers, years, months, days, time, duration
- **Expressing thoughts** — と思います, と言います, でしょう, ことがあります
- **Location & Direction** — ここ/そこ/あそこ, PにNがあります, どうやって, directions
- **Giving & Receiving** — あげる, もらう, くれる, ください, 貸す, 借りる
- **Other expressions** — どうして, どんな, まだ/もう, いっしょに, 前に/後で, から (because)

A single grammar point may appear in **more than one topic** if it fits multiple categories.
Use your judgment — topics should be broad enough to be useful, not one-entry stubs.

---

## Notes

- Never modify source lesson files
- If the destination file already exists, overwrite it completely
- Files without a `文法` section: skip silently (do not include a placeholder entry)
- Preserve Japanese characters exactly — do not transliterate
