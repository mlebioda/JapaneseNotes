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
Load `.cowork/skills/_heading-roles.md` before starting — heading-role recognition rules (scaffolding / container / point), shared with `_practice-grammar-common.md`.

---

### 1. Find the target lesson file

Resolve the lesson code to its full path under `JPLessons/Udemy/N<level>/Grammar/`.
The level is the digit immediately after `UN` (e.g. `UN5GL14` → `N5`). Match a file named
exactly `<code>.md` or starting with `<code>-` (code followed by a hyphen, e.g.
`UN5GL14-Please-come-to-station-at-7-pm.md`). A bare prefix match is not enough —
`UN4GL1` must not match `UN4GL14.md`. If zero or multiple files match, stop and ask the user.

### 2. Read up to `# Summary` only

Never read past the `# Summary` line. Use:

```bash
awk '/^# Summary[[:space:]]*$/{exit} {print}' "$LESSON_FILE"
```

Verify the guard actually fired: if the slice equals the whole file (no `# Summary` line
found), **stop and ask the user** how to proceed — never silently process the full file,
since later steps would then see the plugin-generated export and `<!--ID: -->` lines.
The user decides.

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

**Empty sections:** a section that is present but has no content below its heading is treated the same as an absent section — empty `文法` logs the same `[SKIP]` line; empty `Vocabulary` is skipped silently. Empty sections are omitted from the step 4b classification table.

### 4. Collect all headings and assign roles

Collect **every** heading found in both target sections into a tree — do not drop any. For each heading record:
- `heading` — the exact heading text (preserve kanji, kana, punctuation, spaces)
- `body` — everything below the heading until the next same-or-higher-level heading
- `parent` — the nearest ancestor heading (for tree display and step 8 targeting)
- `source` — `文法` or `Vocabulary` (which section the heading came from)

Then assign each heading a role — **scaffolding**, **container**, or **point** — using the
shared rules in `.cowork/skills/_heading-roles.md`. Scaffolding headings (bare structural
labels like `Examples`, `Structure`) fold into their nearest non-scaffolding ancestor's
body; they are never classification candidates and never appear in the step 4b table.

### 4b. Classify headings — ask the user

Before creating any files, present every **candidate** heading (containers and points —
never scaffolding) to the user, tree-indented, with its suggested role and a brief
description of its content. Suggested roles are proposals from `_heading-roles.md` —
the user confirms or overrides each one; nothing is auto-skipped silently.

Compute each heading's proposed slug (step 5 rules) before printing the table, and show it — slugs become permanent filenames and public URLs, so this table is the user's chance to correct them before any file exists. A slug override given here replaces the computed slug in all later steps. Prefer context-qualified slugs for generic headings — a `### Verbs` container under 謙譲語 should become `kenjougo-verbs`, not `verbs`; suggest such qualified slugs proactively in the table.

**Format — print this table and wait for user input:**

```
Headings found in <lesson-code>:

  [文法]
  1. ## Numbers                [container: no prose, groups 2–3]                        slug: numbers
  2.   #### Only numbers       [grammar: reference table 0–万]                          slug: only-numbers
  3.   #### 同じ - same        [grammar: has Structure + Examples]                      slug: ji-same

  [Vocabulary]
  4. ## こんな, そんな, あんな  [grammar: 3 example lines]        → subdir: Adjectives?  slug: konna-sonna-anna
  5. ### 出来る（できる)       [grammar: 2 structures + examples] → subdir: Verbs?      slug: dekiru

Confirm or override each role (grammar / container / skip).
Slugs are the proposed filenames (permanent URLs) — to change one, type: slug <n> <new-slug>
For Vocabulary items, confirm or change the suggested subdir.
If the suggested subdir doesn't fit, type: new:<dirname> or other
```

Indent each candidate under its parent candidate to show the tree. The bracketed role
uses the classification vocabulary: a `_heading-roles.md` **point** is shown as
`[grammar: …]`, a **container** as `[container: …]`.

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

Scaffolding headings are never listed and never classified — their bodies already belong
to their parent candidate (see `_heading-roles.md`). If the user believes a listed
candidate is actually scaffolding (or vice versa), that is a signal to extend the
scaffolding label list in `_heading-roles.md` — with user confirmation — before proceeding.

**After the user responds**, proceed with steps 5–10 using only the classified
headings, processing each heading sequentially: complete steps 5 → 7 → 8 for one
heading fully before moving to the next. Do not batch slug computation or file
content planning across multiple headings before creating the first file.
Carry the classification forward:
- `grammar` from `文法` → `grammar-index/grammar/<slug>.md` (normal flow, steps 5–11)
- `grammar` from `Vocabulary` → `grammar-index/grammar/vocabulary/<subdir>/<slug>.md` (vocabulary file format, step 7b; step 8 applies normally — under a routed POS container, "applies normally" includes this heading getting its own per-child link in addition to the container's bare link; see Step 8's "Per-child link (routed containers only)" subsection)
- `container` sourced from `# Vocabulary`, whose normalized heading text is exactly `Verbs`,
  `Nouns`, or `Adjectives`, and whose children are exclusively Vocabulary-sourced `grammar`
  headings → routes to step 7c (vocabulary POS container, consolidated) instead of step 7;
  step 8 inserts a bare, anchor-less wikilink to `grammar-index/grammar/vocabulary-<pos>.md`
- `container` (any other case — a non-POS-named `# Vocabulary` heading, one that mixes in a
  nested container, or **any** `# 文法`-sourced container regardless of heading text) → step 7
  creates a container file; step 8 inserts wikilink in lesson
- `skip` → no file created, no wikilink inserted

### 5. Normalise the slug

If the user provided a slug override for this heading in step 4b, use it verbatim and skip the rules below.

Apply these steps in order to the heading text:

1. **Replace separator characters `・` and `/` with a space** — they mark word
   boundaries; stripping them later would glue adjacent words together
   (`お・ご` → `お ご`, `progressive/state` → `progressive state`).
2. **Prefer parenthesized readings** — when the heading contains a kanji word followed
   by its kana reading in parentheses (`<kanji>（<reading>）`, fullwidth or ASCII parens),
   keep only the kana reading: drop the kanji run, any okurigana directly attached to it,
   and the parentheses. `特別な動詞（とくべつなどうし）` → `とくべつなどうし`; `出来る（できる)` → `できる`.
3. **Transliterate kana to romaji** using standard Hepburn romanization (table below).
   Apply compound kana before single kana (e.g. `きゃ→kya` before `き→ki`).
   Special rules: `っ` doubles the following consonant (`っか→kka`, `っぱ→ppa`); lone `っ` at end → `t`.
   `ん` before b/m/p → `m` (`しんぶん→shimbun`); elsewhere → `n`.
   `ー` (long vowel mark) → drop.
   Kanji are **not** transliterated — they are stripped in step 6.
4. **Lowercase** all characters.
5. **Dedup kana against Latin** — if a transliterated kana token equals a Latin token
   already present in the heading (case-insensitive, ignoring `-`), drop the transliterated
   copy and keep the Latin original: `ウチ・ソト (Uchi-Soto)` → keep `uchi-soto`, drop `uchisoto`.
6. **Strip all remaining non-ASCII** characters (kanji, `〜`, `（`, `）`, `「`, `」`, etc.).
7. **Strip punctuation except `-`** (removes `.`, `,`, `!`, `?`, `(`, `)`, `'`, etc.).
8. **Replace one or more spaces with a single `-`**.
9. **Strip leading and trailing `-`**.
10. **Collapse consecutive `-`** to a single `-`.
11. If the result is empty (heading was entirely kanji with no Latin or kana), use the
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
- `お・ご V「ます形」します` → separators: `お ご V「ます形」します` → transliterate/lowercase/strip: `o go v masushimasu` → `o-go-v-masushimasu`
- `特別な動詞（とくべつなどうし）` → reading preference: `とくべつなどうし` → transliterate: `tokubetsunadoushi`
- `ウチ・ソト (Uchi-Soto) - In-group / Out-group` → separators: `ウチ ソト (Uchi-Soto) - In-group  Out-group` → dedup (`uchi soto` duplicates `Uchi-Soto`): `(Uchi-Soto) - In-group  Out-group` → lowercase/strip/collapse: `uchi-soto-in-group-out-group`

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

Also check whether the same grammar point already exists under a **different** slug — slug
rules may have changed since the file was created, and a re-extraction must not silently
create a duplicate. Search existing frontmatter for this heading's `pattern`:

```bash
grep -rlF 'pattern: <exact heading text>' grammar-index/grammar/
```

then confirm the `lesson:` field matches too. If such a file exists, treat it exactly like
the target-path collision below (same Skip / Overwrite / Rename prompt; when in doubt,
Skip preserves the existing file and its slug).

**Consolidated vocabulary POS containers are exempt from this `pattern:` grep.** For a
`container` heading routed to Step 7c, the target file's `pattern:` frontmatter is always the
fixed POS name (e.g. `Verbs`), which would trivially "match" on every single append and is
useless as a duplicate signal. For this path, idempotency is handled entirely by Step 7c's own
per-entry link-target check — dedup by the vocabulary leaf file's path, not by a lesson-code
section or by frontmatter `pattern` text.

If the target path already exists, ask the user:
```
<target-path> already exists. What should I do?
  1. Skip — keep the existing file
  2. Overwrite — replace with new content
  3. Rename — use a different slug (you provide)
```
Wait for the user's choice before proceeding.

### 7. Create the file

**Overwrite preservation rule:** if the user chooses **Overwrite** and the existing file carries `register:` or `confused_with:` frontmatter fields, or `## Register` / `## Often confused with` sections (the typical case: a later full extraction pass resolving a `partial: true` stub that register-confusability-grammar already processed), preserve them when recreating the file from the step-7 template:
- Carry the `register:` and `confused_with:` frontmatter values into the new frontmatter block unchanged (in their canonical position per `_conventions.md`: after `level`, before `proofread`).
- Carry the `## Register` and `## Often confused with` sections into the new body unchanged, in their `_conventions.md` section-order position.
Without this, overwriting silently wipes the mirror while other files still hold reverse links to this slug — a dangling half-relation.

Populate the file with the agreed format:

```
---
lesson: <lesson-code>
pattern: <exact heading text>
topic_slug: ""
function: []
level: <N5 | N4 | N3 | N2 | N1>
proofread: false
---

# <exact heading text>

> [One-line English gloss of what the pattern expresses — derive from body text]

## Structure

[Formation rule — extract or derive from body text; e.g. "Verb (ない-form) + でください"]

## Examples

[Example sentences extracted from the lesson file body — required; leave empty if the lesson has none.
One Markdown bullet (`- `) per sentence — see `_conventions.md` "## Examples content format"]

## Use Cases

[Optional — explanation of when/how to use the pattern, in English. Omit the section if the gloss line already covers it fully.]

## Notes

[Optional — nuances, contrasts, or learner pitfalls. Omit the section if empty.]
```

Section order matches `_conventions.md` **File structure rules**: Structure → Examples → Use Cases → Notes.

Rules for populating each section:
- `lesson` — the lesson code (e.g. `UN5GL14`)
- `pattern` — the exact heading text, unchanged
- `topic_slug` — leave as empty string `""` for now; filled in step 9
- `function` — leave as empty array `[]`; filled in step 9d from the `_conventions.md` controlled vocabulary. Grammar point files only — do **not** add `function` to container or vocabulary file frontmatter
- `level` — from the lesson path (`N5`, `N4`, etc.)
- `proofread` — always `false` on creation
- One-line gloss after `# <heading>` — derive from the body text; keep it to one line
- `## Structure` — the formation rule. If the body has a clear structural description or
  bullet, use it. If not, derive from examples. Reference tables from the lesson body
  (e.g. a special-verbs conjugation table) are copied verbatim into `## Structure`,
  above any formation rule.
- `## Examples` — all example sentences found in the body. Preserve Japanese + any
  translation present. Always include the section; leave it empty if the lesson has none.
  One bullet per sentence, per `_conventions.md` "## Examples content format" — never
  blank-line-separated paragraphs.
- `## Use Cases` — explanation from the lesson body, in English, describing when/how to use
  **this pattern's own** forms or semantic variants. If the body is in Polish, translate to
  English. Omit the section entirely if the gloss line already covers it. Never put a
  comparison/nuance table naming a *different*, separately-named grammar pattern here — that
  belongs in `## Notes` below (or, once the compared pattern has its own
  `grammar-index/grammar/` file, in `## Often confused with`, populated later by
  register-confusability-grammar — not this skill).
- `## Notes` — omit on creation (leave out the section entirely) **unless** the lesson body
  contains a nuance/contrast table or prose comparing this pattern against a genuinely
  *different* pattern that has no standalone `grammar-index/grammar/` file yet — `##
  Often confused with` requires a resolvable slug to link to, so it cannot hold this content
  until that other pattern is itself extracted. In that case, carry the comparison here
  verbatim under `## Notes`. This is the only content extract-grammar ever puts in `## Notes`
  on creation — never add anything else, and never emit an empty placeholder section when no
  such table exists in the lesson body.

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
```

List only the sub-headings that were classified as `grammar` or `container` (not `skip`).
As with grammar point files, always omit `## Notes` on creation — never emit an empty section.

**Not used for a routed Vocabulary POS container.** A `container` heading matching the Step 4b
routing criteria (§"Routing change") uses the consolidated file format and append logic in Step 7c
instead of this template — this template is only ever used for the non-routed container cases
listed in the Step 4b carry-forward bullets above.

**Vocabulary file format** — used for `grammar` headings sourced from `# Vocabulary`.

Frontmatter and heading block (literal — the only markdown extract-grammar.md keeps inline
for vocabulary files; it is unique to this skill's file-creation step and is not part of the
shared Structure format templates in `_conventions.md`):

```
---
lesson: <lesson-code>
pattern: <exact heading text>
topic_slug: ""
level: <N5 | N4 | N3 | N2 | N1>
proofread: false
---

# <exact heading text>
```

**Step 7b-i — infer single sense vs 2+ distinct senses**

Read the heading's collected body (from step 4) and judge whether it describes one unified
sense, or two-plus genuinely different senses (not just different grammatical forms of the
same meaning — the same test `structure-grammar.md` applies to grammar use cases, scoped
here to a vocabulary word's senses). Existing source structure (a `### Use cases` or
`### Meaning` list with 2+ distinct entries) is a strong signal but not authoritative.

Propose the shape to the user and wait for confirmation before writing the file, using a
prompt in the same style as `structure-grammar.md`'s ambiguity prompt:

```
Vocabulary word: <heading text> (<slug>)
Content summary: <brief description of what senses/uses appear in the source body>

Options:
  1. Single sense — flat ## Structure / ## Examples
  2. <N> distinct senses — numbered ## 1..<N> sections: <proposed sense names>
  3. Skip structuring — write flat shape anyway (fallback for genuinely unclear content)

Which should I use?
```

A user override of sense count or names is used verbatim in Step 7b-ii.

**Step 7b-ii — populate the file**

Populate the body per the flat or numbered vocabulary template in `_conventions.md`'s
**## Structure format** section — "Vocabulary files — flat (single sense)" or "Vocabulary
files — numbered (2+ distinct senses)" — chosen per the Step 7b-i inference. Reference the
template by name only; do **not** restate its markdown inline here.

Rules for vocabulary file body:
- Strip only the tag prefix from lines that start with `#w `, `#wc `, or `#wp ` — keep everything after the tag and space.
  - `#w こんな - like this/ so` → `こんな - like this/ so`
  - `#wc 出来る（でき）- to be built` → `出来る（でき）- to be built`
- Sort the (tag-stripped) body content into the `Structure` and `Examples` buckets of the
  confirmed template, per sense where numbered:
  - `Structure` — free-form prose: part of speech, reading, transitivity, collocations, an
    attachment note where relevant, and any source `### Structure` line.
  - `Examples` — bulleted, one sentence per bullet, per `_conventions.md` "## Examples
    content format".
  This replaces copying the body as one verbatim block — content is reorganized into these
  buckets, not pasted as-is.
- Do **not** add `## Use Cases`, `## Notes`, `## Register`, or `## Often confused with`
  sections (cross-reference `_conventions.md` "File structure rules (vocabulary file)").
- Do **not** create a topic index entry (step 9) for vocabulary files — their subdir path is their classification.

Target path: `grammar-index/grammar/vocabulary/<subdir>/<slug>.md`
Create the subdir if it does not exist.

### 7c. Vocabulary POS container (consolidated)

Runs for a `container` heading routed by the Step 4b rule (sourced from `# Vocabulary`,
normalized heading text exactly `Verbs`, `Nouns`, or `Adjectives`, children exclusively
Vocabulary-sourced `grammar` headings). Runs after the vocabulary leaf files themselves are
created (so their slugs/labels are known) and before the lesson-file wikilink step (Step 8).

**Runs regardless of Step 6's Created/Skip outcome for the underlying leaf.** Step 7c fires for
every Vocabulary-sourced leaf file under a routed container heading whether Step 6 resulted in
*Created* (a new leaf file this run) or *Skip* (the leaf file already existed from a prior run) —
its own per-entry dedup (the link-target check in item 2 below) is the only gate Step 7c needs,
and is sufficient on its own regardless of which case produced the leaf. This is a general rule,
not something true only incidentally for a one-off migration: if Step 7c were gated on Step 6's
Created outcome the way Step 8 and Step 9 are (see their "Only for files Created in step 7" /
"Only process files that were Created" rules), a re-run, or a leaf extracted by hand before this
step existed, would silently fail to get themed/appended. **Step 8's per-child link (for routed
containers, see Step 8's "Per-child link (routed containers only)" subsection) shares this same
reasoning and also does not inherit the "Created only" gate — do not "fix" either of them into
matching the gate still used by Step 9 and by Step 8's own container-level link.**

1. **Read the target file** (`grammar-index/grammar/vocabulary-<pos>.md`, `<pos>` ∈ `verbs` /
   `nouns` / `adjectives`, derived from the container heading's normalized POS text) if it
   exists; otherwise this append creates it fresh in the format below with an empty `##
   Sub-topics` body — no theming decision needed for a first entry, skip straight to item 3.

   File format on first creation:
   ```
   ---
   pattern: Verbs
   topic_slug: ""
   proofread: false
   ---

   # Verbs

   > Verb vocabulary consolidated across lessons.

   ## Sub-topics
   ```
   No `lesson:` field (the file spans many lessons — provenance stays one hop away in the linked
   leaf file's own `lesson:` frontmatter). No `level:` field (entries span multiple JLPT levels;
   level stays per-bullet, as today). `topic_slug: ""` (empty string, not `[]`) and `proofread:
   false`, never touched — matches the `vocabulary/**` leaf-file convention, not the old
   per-lesson container convention.

2. **Per-entry dedup (idempotency)** — before adding any new bullet, check whether a bullet
   already links to this exact `grammar-index/grammar/vocabulary/<subdir>/<slug>` path anywhere
   in the file (inside any theme, or ungrouped) — search by the **link target path**, not by a
   lesson-code section (there is no per-lesson section to key off in this shared file). If found,
   skip — do not add a duplicate bullet.

3. **Propose theme placement to the user** — for each new entry being appended (there may be
   several from one lesson), and considering it against both the *existing* themed groups in the
   file and the *other new entries from this same run*, propose one of:
   - **Join an existing theme** — the new entry genuinely shares that theme's topic with its
     current members.
   - **Start a new theme** — 2+ of the entries being considered (existing ungrouped entries in
     the file, and/or entries from this run) share a genuine topic not yet represented as a theme.
   - **Stay ungrouped** — no genuine shared topic found; add as a flat bullet.

   Prompt format (same style as `structure-grammar.md`'s ambiguity prompt and Step 7b-i's
   sense-count prompt):
   ```
   New vocabulary entries to add to grammar-index/grammar/vocabulary-verbs.md:
     - 渡す（わたす）- to hand over  (N5, from UN5GL15)
     - 渡る（わたる）- to cross / go overseas  (N5, from UN5GL15)
     - できる - can  (N5, from UN5GL15)

   Existing themes in the file: <list, or "(none yet)">
   Existing ungrouped entries: <list, or "(none)">

   Proposed placement:
     1. 渡す, 渡る → new theme "渡す／渡る (transitivity pair)" — both are the transitive/
        intransitive pair of the same root
     2. できる → ungrouped (no shared theme found with existing entries)

   Confirm, or override any entry's placement (join <theme name> / new theme <name> / ungrouped)?
   ```
   Wait for confirmation before writing. A user override is used verbatim.

4. **Never force a theme** — this mirrors the "don't force `## Often confused with` matches"
   caution already used in `register-confusability-grammar.md`. If nothing genuine is found,
   propose "stay ungrouped" as the default, not a strained theme.

5. **Write the append**:
   - Themed placement: insert the bullet under the matching `### <Theme Name>` heading (creating
     the heading, immediately after `## Sub-topics`, if this is the theme's first appearance —
     or immediately after the last existing themed group if joining one already created).
   - Ungrouped placement: append the bullet as a flat, un-headed bullet — keep it simple and
     append flat bullets at the end of the file's `## Sub-topics` content, after all themed
     groups, so themed groups stay visually contiguous at the top.
   - Bullet format is unchanged from today's container format:
     `- [<label>](/JapaneseNotes/grammar-index/grammar/vocabulary/<subdir>/<slug>) · <level>`.

### 8. Add wikilink to lesson file

After creating the standalone grammar file, insert an Obsidian wikilink under the
corresponding heading in the lesson file, so it is navigable directly from the lesson.

**Format** — insert on the line immediately after the heading, before any existing body content:

```
## ね - seeking approval
→ [[grammar-index/grammar/seeking-approval]]

Ne - seeking approval...
```

For a routed Vocabulary POS container, both the container heading and each child heading
receive their own link:

```
## Verbs
→ [[grammar-index/grammar/vocabulary-verbs]]

### 勉強 - learn
→ [[grammar-index/grammar/vocabulary/Verbs/benkyou-learn]]

雰囲気の勉強をしています...
```

**Consolidated-file routing case (container-level link):** for a `container` heading routed to
Step 7c, the inserted link is **not** `[[grammar-index/grammar/<slug>]]` (there is no per-lesson
slug) — it is a bare, anchor-less wikilink to the shared file,
`[[grammar-index/grammar/vocabulary-<pos>]]`. Under thematic grouping a lesson's vocabulary
entries can scatter across multiple themes or land ungrouped, so no predictable per-lesson
deep-link anchor exists inside the shared file; the link lands at the top of the file, same as
any other wikilink to a page without an anchor. This is a deliberate, accepted regression versus
the old one-lesson-one-file setup — but it describes only this **container-level** link's lack of
a precise per-item anchor; it does not mean no per-word link exists at all. See "Per-child link
(routed containers only)" below for the per-word link that covers that.

**Per-child link (routed containers only):** each Vocabulary-sourced `grammar` sub-heading under
a routed container (e.g. `### 勉強 - learn`) additionally gets its own wikilink to its leaf file,
`[[grammar-index/grammar/vocabulary/<subdir>/<slug>]]`, inserted immediately after that
sub-heading's own line — same insertion mechanic as the normal case above. This link is inserted
**regardless of whether Step 6 resulted in Created, Skip, or Rename** for that child's leaf file.
Skip is the *common* case for vocabulary — recurring words like できる, 待つ, ある get
re-extracted from many lessons — so this is not edge-case robustness, it is the primary path: the
current lesson's heading must still be linked to the leaf file that already exists. The **only**
gate is the dedup check below (link already present under that heading); it does **not** inherit
the "Only for files Created in step 7" gate that governs the container link and normal
grammar/container links elsewhere in this step. This mirrors Step 7c's identical reasoning for
not inheriting that gate (see Step 7c).

**Rules:**
- **Container-level link and normal (non-routed) links:** only for files **Created** in step 7
  (or, for the container link specifically, for headings whose leaf(s) were processed by Step
  7c) — skip if the leaf was skipped in step 6.
- **Per-child link (routed containers only):** insert regardless of Step 6's Created/Skip/Rename
  outcome for that child's leaf — this bullet intentionally does not reference "Created" at all;
  it is gated **only** by the dedup rule below.
- **Dedup (per link tier):**
  - normal case: skip if `[[grammar-index/grammar/<slug>]]` is already present under that heading.
  - container link: skip if `[[grammar-index/grammar/vocabulary-<pos>]]` is already present under
    that heading.
  - per-child link: skip if `[[grammar-index/grammar/vocabulary/<subdir>/<slug>]]` is already
    present under **that child's own heading** — checked independently of the container's dedup
    check, not shared with it.
- Use Python to locate the heading line and insert after it. The script must:
  1. **Slice at `# Summary` first** — only the pre-Summary slice is ever searched or
     modified; the tail is reattached unchanged. This enforces "never write past
     `# Summary`" structurally instead of incidentally.
  2. **Verify the insertion happened** (`re.subn` count) — a non-matching heading must
     produce a `[WARN]` line, never a silent no-op. Collect all `[WARN]` lines and
     include them in the step 10 completion report.

  ```python
  import re
  with open(lesson_path) as f:
      content = f.read()

  # Only the pre-Summary slice is ever modified
  m = re.search(r'^# Summary[ \t]*$', content, flags=re.MULTILINE)
  head, tail = (content[:m.start()], content[m.start():]) if m else (content, "")

  link = "→ [[grammar-index/grammar/slug]]"
  new_head, n = re.subn(
      r'(^#{1,6} ' + re.escape(heading) + r'[ \t]*\n)',
      r'\1' + link + r'\n',
      head,
      count=1,
      flags=re.MULTILINE
  )
  if n == 0:
      print("[WARN] no wikilink inserted for slug — heading not matched")
  else:
      with open(lesson_path, "w") as f:
          f.write(new_head + tail)
  ```

- **Duplicate heading texts:** if the heading text occurs more than once in the
  pre-Summary slice, do not rely on first-match — narrow the substitution to the parent
  section's line range (known from the step 4 heading tree) so the link lands under the
  correct occurrence. This applies identically to child headings under a routed container: a
  vocabulary word heading that repeats verbatim across the lesson must not get its link
  misattributed to the wrong occurrence.
- Never modify `<!--ID: -->` lines.
- Never read or write past `# Summary` (enforced by the slice above).

### 9. Classify into grammar-index topics

Run this step after all grammar-index/grammar/ files for the lesson are written. Only process files
that were **Created** in step 7 — skip files that were already skipped in step 6.

**Container files are included:** they receive topic entries (9c) and `topic_slug` (9d) just
like grammar points — they are the natural browsing entry point for their group. Their
sub-points are classified independently and may share topics with them. Containers never
receive `function`. Vocabulary files are excluded (their subdir path is their classification);
`vocabulary-<pos>.md` consolidated files are excluded too — POS-consolidated vocabulary files,
never individually topic-classified.

**9a. Read existing topic file list**

```bash
ls grammar-index/*.md | grep -v 'index.md'
```

Read each file's `> <description>` line to understand what each topic covers.
This is the current taxonomy — respect it.

**Graceful-empty:** if `grammar-index/` contains no topic files (fresh or wiped index — the `ls` glob matches nothing and errors), treat the taxonomy as empty and proceed: every classification then creates new topic files per the 9b/9c rules, and 9e regenerates `index.md` from scratch. This is expected, not an error.

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
- If B's `## See also` links to A but A's `## See also` does not link to B → add B to A's `## See also`.
- **Dedup**: skip if the link is already present.
- **Format**: `- [<Topic Title>](/JapaneseNotes/grammar-index/<slug>) — <short reason>`
  where `<Topic Title>` is the `# heading` of the target topic file.
- **Reason phrase**: write a short phrase describing why the topics are related (do not copy the filename verbatim).
- Insert inside the `## See also` section (append before end-of-section or end-of-file).

Also apply this rule when a new topic file is created with a `## See also` entry: add the reverse link in the referenced topic.

**9d. Fill `topic_slug` and `function` in each grammar-index/grammar/ file**

After classifying, patch the `topic_slug: ""` field in the frontmatter of each newly
created grammar-index/grammar/ file. Always use a YAML list, even for a single topic:
- Single topic: `topic_slug: ["reasons-causes"]`
- Multiple topics: `topic_slug: ["reasons-causes", "particles-de"]`

In the same pass, patch the `function: []` field: assign 0–2 values describing the
pattern's semantic role, taken **exclusively** from the controlled vocabulary in
`_conventions.md` (section **`function` controlled vocabulary**). An empty array is
allowed and correct when nothing on the list fits — do not force a value. If a
genuinely new function value seems needed, **stop**: propose adding it to the
`_conventions.md` list and wait for explicit user confirmation before using it.
This is the only step that sets `function`; after this run completes, the field is
immutable (same protected status as `topic_slug`).

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
  Appended: grammar-index/grammar/vocabulary-verbs.md ← watasu-to-hand-over, wataru, dekiru-can (new theme: 渡す／渡る transitivity pair; dekiru-can ungrouped)
```

After printing the report, if any grammar point or container files were created in this
session, ask — `N` counts **only grammar point and container files**; vocabulary files
(`grammar-index/grammar/vocabulary/…`) are complete at creation and never enter the
post-processing chain; `vocabulary-<pos>.md` consolidated files are excluded from `N` too,
whether newly created or appended to in this run:

```
Run preprocess-grammar on the N newly created files? (yes / no / all)
```

- **yes** — load `.cowork/skills/lesson-to-web/preprocess-grammar.md` and pass the list of created grammar point and container file paths (never `vocabulary/` paths).
- **no** — end the skill.
- **all** — load preprocess-grammar in **all** mode, which chains through review-grammar → structure-grammar → register-confusability-grammar → see-also-grammar without prompting at handoffs.

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
| Separators `・`, `/` | Replace with a space (first, before transliteration) |
| Kanji word + `（reading）` | Keep the reading only; drop kanji + attached okurigana |
| Hiragana / Katakana | Transliterate to romaji (Hepburn) — see step 5 table |
| Kana duplicating a Latin token | Drop the kana copy, keep the Latin original |
| Kanji (no parenthesized reading) | Strip (not transliterated) |
| Latin letters (A–Z, a–z) | Lowercase and keep |
| Digits (0–9) | Keep |
| Space | Replace with `-` |
| Other non-ASCII (`〜`, `（`, `）`, `「`, `」`) | Strip |
| Punctuation (`.`, `,`, `!`, `?`, `(`, `)`, `'`) | Strip |
| Hyphen `-` | Keep |
| Multiple consecutive `-` | Collapse to one `-` |
| Leading or trailing `-` | Strip |
| Empty result (all kanji, no kana/Latin) | Use positional fallback: `point-1`, `point-2`, etc. |
| User override from step 4b table | Always wins — use verbatim |

