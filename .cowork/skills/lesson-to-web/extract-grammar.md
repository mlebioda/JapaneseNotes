---
name: extract-grammar
description: >
  Extract grammar points from a lesson file's 文法 section into standalone
  published files under grammar-index/grammar/. Each grammar point becomes one file named
  <anchor-slug>.md, then each new file is classified into
  grammar-index/ topic files (creating new topic files when needed).
  Trigger: "extract grammar from <lesson>".
---

# Extract Grammar Skill

## Trigger

User says:

- "extract grammar from UN5GL14"
- "extract grammar from <lesson code>"

---

## Workflow

## Shared files

Load `.cowork/skills/lesson-to-web/_conventions.md` before starting.

---

### 1. Find the target lesson file

Resolve the lesson code to its full path under `JPLessons/Udemy/N<level>/Gramatyka/`.
The level is the digit in the code (e.g. `UN5GL14` → `N5`). Match by filename prefix;
ignore any trailing words in the filename.

### 2. Read up to `# Summary` only

Never read past the `# Summary` line. Use:

```bash
awk '/^# Summary$/{exit} {print}' "$LESSON_FILE"
```

Pass only this slice to all subsequent parsing steps.

### 3. Locate target sections

Find the following sections in the pre-Summary slice. Process only these two — ignore all other top-level headings.

**`# 文法`** — grammar section.
- Match `^# 文法` (heading level 1). Collect everything from that heading until the next same-level heading.
- If found at a level other than 1 (e.g. `## 文法`), ask the user: "Found `## 文法` at heading level 2 — should I treat this as the grammar section?"
- If no `文法` section exists at any level, skip grammar extraction and log: `[SKIP] <lesson-code>: no 文法 section found`

**`# Vocabulary`** — vocabulary section.
- Match `^# Vocabulary` (heading level 1). Collect everything from that heading until the next same-level heading.
- If found at a level other than 1 (e.g. `## Vocabulary`), ask the user: "Found `## Vocabulary` at heading level 2 — should I treat this as the vocabulary section?"
- If no `Vocabulary` section exists, skip vocabulary extraction silently (it is optional — do not log).

### 4. Collect all headings

Collect **every** heading found in both target sections — do not skip any. For each heading record:
- `heading` — the exact heading text (preserve kanji, kana, punctuation, spaces)
- `body` — everything below the heading until the next same-level heading
- `has_prose` — whether the body contains any prose/examples beyond sub-headings and `#w` lines
- `has_subheadings` — whether the body contains further headings
- `source` — `文法` or `Vocabulary` (which section the heading came from)

### 4b. Classify headings — ask the user

Before creating any files, present every heading to the user with a brief description
of its content and ask for classification. Do not auto-skip or auto-classify anything.

**Format — print this table and wait for user input:**

```
Headings found in <lesson-code>:

  [文法]
  1. ## Numbers              [no prose, has sub-headings: Only numbers, People, Floors]
  2. #### Only numbers       [reference table: number lists 0–万]
  3. #### 同じ - same        [has Structure + Examples]

  [Vocabulary]
  4. ## こんな, そんな, あんな  [3 example lines, no sub-headings]  → subdir: Adjectives?
  5. ### 出来る（できる)       [verb, 2 structures + examples]     → subdir: Verbs?

Classify each (grammar / container / skip).
For Vocabulary items, confirm or change the suggested subdir.
If the suggested subdir doesn't fit, type: new:<dirname> or other
```

**Subdir suggestions for Vocabulary headings** — derive from content, not from `#w`/`#wc`/`#wp` tags:
- Heading or body describes verb conjugation, verb usage, or verb structures → suggest `Verbs`
- Heading or body describes adjective forms or adjective usage → suggest `Adjectives`
- Heading or body describes nouns, expressions, pronouns, set phrases → suggest `Nouns`
- Unclear or mixed → suggest `Nouns` and note the ambiguity in the table

If the user types `new:<dirname>`, create the new subdir under `grammar-index/grammar/vocabulary/`.
If the user types `other`, place the file under `grammar-index/grammar/vocabulary/Other/`.

**Classifications:**

- **grammar** — extract as a standalone grammar file. Used when the heading has
  prose, structure, or examples that explain a pattern.
- **container** — the heading has no content of its own but groups sub-headings.
  Creates a container file that links to its promoted sub-files. Sub-headings are
  classified separately.
- **skip** — do not extract. Used for pure vocabulary lists or headings that are
  not grammar patterns.

**After the user responds**, proceed with steps 5–11 using only the classified
headings, processing each heading sequentially: complete steps 5 → 7 → 8 for one
heading fully before moving to the next. Do not batch slug computation or file
content planning across multiple headings before creating the first file.
Carry the classification forward:
- `grammar` from `文法` → `grammar-index/grammar/<slug>.md` (normal flow, steps 5–11)
- `grammar` from `Vocabulary` → `grammar-index/grammar/vocabulary/<subdir>/<slug>.md` (vocabulary file format, step 7b)
- `container` → step 7 creates a container file; step 8 inserts wikilink in lesson
- `skip` → no file created, no wikilink inserted

### 5. Normalise the slug

Apply these steps in order to the heading text:

1. **Transliterate kana to romaji** using standard Hepburn romanization (table below).
   Apply compound kana before single kana (e.g. `きゃ→kya` before `き→ki`).
   Special rules: `っ` doubles the following consonant (`っか→kka`, `っぱ→ppa`); lone `っ` at end → `t`.
   `ん` before b/m/p → `m` (`しんぶん→shimbun`); elsewhere → `n`.
   `ー` (long vowel mark) → drop.
   Kanji are **not** transliterated — they are stripped in step 3.
2. **Lowercase** all characters.
3. **Strip all remaining non-ASCII** characters (kanji, `〜`, `・`, `（`, `）`, `「`, `」`, etc.).
4. **Strip punctuation except `-`** (removes `.`, `,`, `!`, `?`, `(`, `)`, `/`, `'`, etc.).
5. **Replace one or more spaces with a single `-`**.
6. **Strip leading and trailing `-`**.
7. **Collapse consecutive `-`** to a single `-`.
8. If the result is empty (heading was entirely kanji with no Latin or kana), use the
   heading's position index: `point-1`, `point-2`, etc.

**Kana romanization table:**

| Kana | Romaji | Kana | Romaji | Kana | Romaji | Kana | Romaji |
|------|--------|------|--------|------|--------|------|--------|
| あ/ア | a | い/イ | i | う/ウ | u | え/エ | e | お/オ | o |
| か/カ | ka | き/キ | ki | く/ク | ku | け/ケ | ke | こ/コ | ko |
| が/ガ | ga | ぎ/ギ | gi | ぐ/グ | gu | げ/ゲ | ge | ご/ゴ | go |
| さ/サ | sa | し/シ | shi | す/ス | su | せ/セ | se | そ/ソ | so |
| ざ/ザ | za | じ/ジ | ji | ず/ズ | zu | ぜ/ゼ | ze | ぞ/ゾ | zo |
| た/タ | ta | ち/チ | chi | つ/ツ | tsu | て/テ | te | と/ト | to |
| だ/ダ | da | ぢ/ヂ | ji | づ/ヅ | zu | で/デ | de | ど/ド | do |
| な/ナ | na | に/ニ | ni | ぬ/ヌ | nu | ね/ネ | ne | の/ノ | no |
| は/ハ | ha | ひ/ヒ | hi | ふ/フ | fu | へ/ヘ | he | ほ/ホ | ho |
| ば/バ | ba | び/ビ | bi | ぶ/ブ | bu | べ/ベ | be | ぼ/ボ | bo |
| ぱ/パ | pa | ぴ/ピ | pi | ぷ/プ | pu | ぺ/ペ | pe | ぽ/ポ | po |
| ま/マ | ma | み/ミ | mi | む/ム | mu | め/メ | me | も/モ | mo |
| や/ヤ | ya | ゆ/ユ | yu | よ/ヨ | yo | | | | |
| ら/ラ | ra | り/リ | ri | る/ル | ru | れ/レ | re | ろ/ロ | ro |
| わ/ワ | wa | を/ヲ | wo | ん/ン | n | っ/ッ | (double) | ー | (drop) |

Compound kana (apply before single): きゃ/キャ→kya, きゅ/キュ→kyu, きょ/キョ→kyo, しゃ/シャ→sha, しゅ/シュ→shu, しょ/ショ→sho, ちゃ/チャ→cha, ちゅ/チュ→chu, ちょ/チョ→cho, にゃ/ニャ→nya, にゅ/ニュ→nyu, にょ/ニョ→nyo, ひゃ/ヒャ→hya, ひゅ/ヒュ→hyu, ひょ/ヒョ→hyo, みゃ/ミャ→mya, みゅ/ミュ→myu, みょ/ミョ→myo, りゃ/リャ→rya, りゅ/リュ→ryu, りょ/リョ→ryo, ぎゃ/ギャ→gya, ぎゅ/ギュ→gyu, ぎょ/ギョ→gyo, じゃ/ジャ→ja, じゅ/ジュ→ju, じょ/ジョ→jo, びゃ/ビャ→bya, びゅ/ビュ→byu, びょ/ビョ→byo, ぴゃ/ピャ→pya, ぴゅ/ピュ→pyu, ぴょ/ピョ→pyo.

Examples:
- `Particle が vs は` → transliterate: `Particle ga vs ha` → lowercase → `particle ga vs ha` → collapse spaces → `particle-ga-vs-ha`
- `Vないでください` → transliterate: `Vnaidekudasai` → lowercase → `vnaidekudasai`
- `V + て-form (request)` → transliterate: `V + te-form (request)` → lowercase → strip punctuation → `v  te-form request` → collapse → `v-te-form-request`
- `がんばって！Let's do our best` → transliterate: `ganbatte！Lets do our best` → lowercase → strip punctuation → `ganbatte lets do our best` → collapse → `ganbatte-lets-do-our-best`
- `同じ` (kanji only, no kana) → transliterate: `同じ` (じ→ji → `同ji`) → strip non-ASCII: `ji` → `ji`
- `目` (kanji only, no kana) → transliterate: no kana → strip non-ASCII: `` → empty → use `point-1`

Note: Latin letters in the heading (e.g. `V`, `N`, `Adj`) are kept as-is through the lowercasing step.

The full output filename is: `grammar-index/grammar/<anchor-slug>.md`

Example: lesson `UN5GL14`, heading `Vないでください`, slug `point-1` →
`grammar-index/grammar/point-1.md`

Better example: lesson `UN5GL14`, heading `V (plain form) + N (noun modifier)` →
slug `v-plain-form-n-noun-modifier` → `grammar-index/grammar/v-plain-form-n-noun-modifier.md`

### 6. Idempotency check

Before creating each file, check the target path based on source:
- `文法` heading → `grammar-index/grammar/<slug>.md`
- `Vocabulary` heading → `grammar-index/grammar/vocabulary/<subdir>/<slug>.md`

If the target path already exists, ask the user:
```
<target-path> already exists. What should I do?
  1. Skip — keep the existing file
  2. Overwrite — replace with new content
  3. Rename — use a different slug (you provide)
```
Wait for the user's choice before proceeding.

### 7. Create the standalone grammar file

Populate the file with the agreed format:

```
---
lesson: <lesson-code>
pattern: <exact heading text>
topic_slug: ""
level: <N5 | N4 | N3 | N2 | N1>
proofread: false
---

# <exact heading text>

> [One-line English gloss of what the pattern expresses — derive from body text]

## Use Cases

[Optional — explanation of when/how to use the pattern, in English. Omit the section if the gloss line already covers it fully.]

## Structure

[Formation rule — extract or derive from body text; e.g. "Verb (ない-form) + でください"]

## Examples

[Example sentences extracted from the lesson file body — required; leave empty if the lesson has none]

## Notes

[Optional — nuances, contrasts, or learner pitfalls. Omit the section if empty.]
```

Rules for populating each section:
- `lesson` — the lesson code (e.g. `UN5GL14`)
- `pattern` — the exact heading text, unchanged
- `topic_slug` — leave as empty string `""` for now; filled in step 9
- `level` — from the lesson path (`N5`, `N4`, etc.)
- `proofread` — always `false` on creation
- One-line gloss after `# <heading>` — derive from the body text; keep it to one line
- `## Use Cases` — explanation from the lesson body, in English. If the body is in Polish,
  translate to English. Omit the section entirely if the gloss line already covers it.
- `## Structure` — the formation rule. If the body has a clear structural description or
  bullet, use it. If not, derive from examples.
- `## Examples` — all example sentences found in the body. Preserve Japanese + any
  translation present. Always include the section; leave it empty if the lesson has none.
- `## Notes` — always omit on creation (leave out the section entirely).

**Container file format** — used when classification is `container`:

```
---
lesson: <lesson-code>
pattern: <exact heading text>
topic_slug: ""
level: <N5 | N4 | N3 | N2 | N1>
proofread: false
---

# <exact heading text>

> <One-line description of what this group of patterns covers>

## Sub-topics

- [<pattern>](/JapaneseNotes/grammar-index/grammar/<slug>) · <level>
- [<pattern>](/JapaneseNotes/grammar-index/grammar/<slug>) · <level>

## Notes

```

List only the sub-headings that were classified as `grammar` or `container` (not `skip`).

**Vocabulary file format** — used for `grammar` headings sourced from `# Vocabulary`:

```
---
lesson: <lesson-code>
pattern: <exact heading text>
topic_slug: ""
level: <N5 | N4 | N3 | N2 | N1>
proofread: false
---

# <exact heading text>

<body content with #w / #wc / #wp tag prefixes stripped>
```

Rules for vocabulary file body:
- Copy the entire body content from the lesson file verbatim.
- Strip only the tag prefix from lines that start with `#w `, `#wc `, or `#wp ` — keep everything after the tag and space.
  - `#w こんな - like this/ so` → `こんな - like this/ so`
  - `#wc 出来る（でき）- to be built` → `出来る（でき）- to be built`
- Lines without a tag prefix (prose, bullet points, sub-headings) are copied unchanged.
- Do **not** add `## Structure`, `## Meaning`, `## Examples`, or `## Notes` sections.
- Do **not** create a topic index entry (step 9) for vocabulary files — their subdir path is their classification.

Target path: `grammar-index/grammar/vocabulary/<subdir>/<slug>.md`
Create the subdir if it does not exist.

### 8. Add wikilink to lesson file

After creating the standalone grammar file, insert an Obsidian wikilink under the
corresponding heading in the lesson file, so it is navigable directly from the lesson.

**Format** — insert on the line immediately after the heading, before any existing body content:

```
## ね - seeking approval
→ [[grammar-index/grammar/seeking-approval]]

Ne - seeking approval...
```

**Rules:**
- Only for files **Created** in step 7 — skip files that were already skipped in step 6.
- Skip if `[[grammar-index/grammar/<slug>]]` is already present anywhere under that heading.
- Use Python to locate the heading line and insert after it:

  ```python
  import re
  with open(lesson_path) as f:
      content = f.read()
  link = "→ [[grammar-index/grammar/slug]]"
  # Insert after the heading line, before its body
  content = re.sub(
      r'(^#{1,6} ' + re.escape(heading) + r'[ \t]*\n)',
      r'\1' + link + r'\n',
      content,
      count=1,
      flags=re.MULTILINE
  )
  with open(lesson_path, "w") as f:
      f.write(content)
  ```

- Never modify `<!--ID: -->` lines.
- Never read or write past `# Summary`.

### 9. Classify into grammar-index topics

Run this step after all grammar-index/grammar/ files for the lesson are written. Only process files
that were **Created** in step 7 — skip files that were already skipped in step 6.

**9a. Read existing topic file list**

```bash
ls grammar-index/*.md | grep -v 'index.md'
```

Read each file's `> <description>` line to understand what each topic covers.
This is the current taxonomy — respect it.

**9b. Plan all classifications before writing**

For each newly created grammar point, decide which topic file(s) it belongs to.
Write out the full plan (grammar point → topic file(s)) before touching any file.
This catches misclassifications before they land.

Apply these rules (same as `summarize-grammar`):
- Bias toward existing topic files.
- A point may appear in up to 3 topic files if it genuinely fits more than one.
- Create a new topic file only when no existing topic fits AND the new name is broad
  enough to attract future lessons (not a one-off).
- Cap at 3 topics per point. If more than 3 seem to fit, pick the strongest 3.

**9c. Update topic files**

For each (grammar point, topic file) pair:

- **Dedup**: skip if `grammar-index/grammar/<slug>)` already appears in the file.
- **Entry format**: `- [<pattern>](/JapaneseNotes/grammar-index/grammar/<slug>) · <level>`
  where `<pattern>` is the exact heading text from the grammar point. Use full absolute
  URLs — NOT wikilinks or relative paths. This ensures the link works on GitHub Pages.
- **Exists**: insert immediately before `## See also` (or append to end of `## Entries`
  if no `## See also`). Use Python:

  ```python
  with open(path) as f: content = f.read()
  entry = "- [同じ - same](/JapaneseNotes/grammar-index/grammar/same) · N5"
  if "## See also" in content:
      content = content.replace("\n## See also", "\n" + entry + "\n\n## See also", 1)
  else:
      content = content.rstrip() + "\n" + entry + "\n"
  with open(path, "w") as f: f.write(content)
  ```

- **New topic file**: create from the template in **Topic file template** below.

**9c-ii. Bidirectional `## See also` between topic files**

After all entries are written, ensure `## See also` links between topic files are symmetric.

For every pair of topic files (A, B) where a grammar point appears in both:
- If A's `## See also` links to B but B's `## See also` does not link to A → add A to B's `## See also`.
- If B's `## See also` links to A but A's `## See also` does not link to B → add A to B's.
- **Dedup**: skip if the link is already present.
- **Format**: `- [<Topic Title>](/JapaneseNotes/grammar-index/<slug>) — <short reason>`
  where `<Topic Title>` is the `# heading` of the target topic file.
- **Reason phrase**: write a short phrase describing why the topics are related (do not copy the filename verbatim).
- Insert inside the `## See also` section (append before end-of-section or end-of-file).

Also apply this rule when a new topic file is created with a `## See also` entry: add the reverse link in the referenced topic.

**9d. Fill `topic_slug` in each grammar-index/grammar/ file**

After classifying, patch the `topic_slug: ""` field in the frontmatter of each newly
created grammar-index/grammar/ file. Always use a YAML list, even for a single topic:
- Single topic: `topic_slug: ["reasons-causes"]`
- Multiple topics: `topic_slug: ["reasons-causes", "particles-de"]`

**9e. Update `index.md`**

Only if at least one new topic file was created in step 9c. Regenerate
`grammar-index/index.md` from the current state of `grammar-index/`, following the
format in **`index.md` format** below.

---

### 10. Completion report

After processing each lesson file, print a compact report:

```
UN5GL14 — 6 grammar points processed

  [文法]
  Created:  grammar-index/grammar/point-1.md  → requests-commands
  Created:  grammar-index/grammar/v-plain-form-n-noun-modifier.md  → sentence-structure, verb-forms
  Skipped:  grammar-index/grammar/point-3.md (user chose skip)

  [Vocabulary]
  Created:  grammar-index/grammar/vocabulary/Adjectives/konna-sonna-anna.md
  Created:  grammar-index/grammar/vocabulary/Verbs/dekiru.md
```

After printing the report, if any files were created in this session, ask:

```
Run preprocess-grammar on the N newly created files? (yes / no / all)
```

- **yes** — load `.cowork/skills/lesson-to-web/preprocess-grammar.md` and pass the list of created file paths.
- **no** — end the skill.
- **all** — load preprocess-grammar in **all** mode, which chains through review-grammar → structure-grammar → see-also-grammar without prompting at handoffs.
- If `.cowork/skills/lesson-to-web/preprocess-grammar.md` does not exist yet — skip this prompt silently.

---

## Topic file template

Use when creating a new grammar-index topic file (step 9c):

```markdown
# <Topic Name>

> <One-line description of what this topic covers — your own words>

## Entries

- [<pattern>](/JapaneseNotes/grammar-index/grammar/<slug>) · <level>

## See also

- [<related-topic>](/JapaneseNotes/grammar-index/<related-topic>) — <short reason>
```

- Filename: kebab-case English, descriptive, reusable across future lessons.
  Good: `reasons-causes.md`, `verb-te-form.md`, `particles-wa-ga.md`.
  Bad: `kara.md`, `because-only.md`, `n5-particles.md`.
- Title: human-readable derivation of the filename.
- Description: one sentence explaining when to look here.
- "See also": 1–2 full absolute URL links to existing related topics if obvious; otherwise omit.

---

## `index.md` format

Lives at `grammar-index/index.md`. Groups topic files into a fixed high-level taxonomy:

- **Verbs** — `verb-*` topic files
- **Adjectives** — `adjectives-*` topic files
- **Particles** — `particles-*` topic files
- **Patterns** — sentence-level patterns: reasons, comparisons, suggestions, conditionals, etc.
- **Forms & Counters** — counters, time expressions, numbers
- **Other** — anything that doesn't fit the above

```markdown
# Grammar Index

## Verbs

- [verb-te-form](/JapaneseNotes/grammar-index/verb-te-form) — <description from file's > line>

## Particles

- [particles-wa-ga](/JapaneseNotes/grammar-index/particles-wa-ga) — <description>

## Patterns

- [reasons-causes](/JapaneseNotes/grammar-index/reasons-causes) — <description>

(etc. — omit empty groups)
```

---

## Slug normalisation — quick reference

| Input character type | Action |
|---|---|
| Hiragana / Katakana | Transliterate to romaji (Hepburn) first — see step 5 table |
| Kanji | Strip (not transliterated) |
| Latin letters (A–Z, a–z) | Lowercase and keep |
| Digits (0–9) | Keep |
| Space | Replace with `-` |
| Other non-ASCII (`〜`, `・`, `（`, `）`, `「`, `」`) | Strip |
| Punctuation (`.`, `,`, `!`, `?`, `(`, `)`, `/`, `'`) | Strip |
| Hyphen `-` | Keep |
| Multiple consecutive `-` | Collapse to one `-` |
| Leading or trailing `-` | Strip |
| Empty result (all kanji, no kana/Latin) | Use positional fallback: `point-1`, `point-2`, etc. |

