---
name: reading-jlpt
description: >
  JLPT N4 reading comprehension drill on user-pasted authentic passages.
  Auto-detects passage type, flags above-N4 vocabulary, generates multiple-choice
  questions (batch), explains results, suggests vocabulary, writes a session file
  to JPLessons/Reading/, and optionally chains to fill-templates.
tools: [Write, Bash]
---

# Reading JLPT Skill

## Trigger

User says any of:
- "practice reading"
- "reading drill"
- "jlpt reading [passage]"
- "let's do a reading drill"
- or pastes a Japanese passage and asks to practice reading

If the user triggers this skill but pastes no passage, ask them to provide one before proceeding.

---

## Recommended sources (print on user request)

| Source | Description |
|---|---|
| jlpt.jp | Official JLPT sample questions — free, authentic, level-labelled |
| NHK Web Easy | Real news articles rewritten for learners; N4–N3 range |
| Shin Kanzen Master N4 読解 | Structured drills closely matching real exam format |
| So-Matome N4 読解 | Lighter workload; good for daily reading warmup |

---

## Workflow

### Step 1 — Auto-detect passage type

Classify the pasted content by character count and layout:

| Type | Japanese name | Approx. length | Questions |
|---|---|---|---|
| Short | 短文 | ~100–200 characters | 1 |
| Medium | 中文 | ~300–400 characters | 2–3 |
| Information retrieval | 情報検索 | Document-like layout (tables, notices, forms) | 2–3 |

Announce the detected type to the user before proceeding:

> "Detected: **Short passage (短文)** — I will generate 1 question."

---

### Step 2 — Scan for above-N4 content

Before showing any questions, read through the passage and identify:
- Vocabulary likely above N4 (N3 or above)
- Kanji combinations unlikely to appear in N4

For each flagged item output:
```
- 語彙(ごい) — meaning — [above N4]
```

Present the full list. Then ask:

> "The passage contains X above-N4 items listed above. Do you want to proceed with the drill?"

If the user says no, stop. If yes, carry all flagged items forward — they become candidates in Step 5.

If no above-N4 items are found, say so briefly and proceed automatically.

---

### Step 3 — Generate all questions at once (batch mode)

Output all questions in a single message. Do not reveal answers, do not provide hints, do not add furigana to the question text.

Question types by passage type:
- Short (短文): detail question (what / who / when / where / why)
- Medium (中文): mix of detail, main idea, and inference
- Information retrieval (情報検索): information lookup and cross-reference

Format:

```
**Q1.** [question text in Japanese]

A. [option]
B. [option]
C. [option]
D. [option]
```

Close the question block with:

> "Submit all answers as: Q1: B, Q2: A, Q3: C — or equivalent format."

---

### Step 4 — Explain all answers

After the user submits their answers, process all of them in one message:

- **Correct answer**: one line confirming correctness + quote the key sentence from the passage that supports the answer.
- **Wrong answer**: two parts:
  1. Why the chosen option is wrong — cite specific passage evidence.
  2. Why the correct option is right — cite specific passage evidence.

Do not add furigana to quoted passage sentences.

---

### Step 5 — Word suggestions

Suggest #w/#wc/#wp candidates from:
1. Words directly linked to wrong answers (i.e. a misread word caused the error)
2. Above-N4 words flagged in Step 2

**Skip Step 5 entirely** if:
- User answered all questions correctly, AND
- Step 2 found no above-N4 items.

Otherwise, present suggestions in standard vault format:

```
#w 語彙(ごい) - vocabulary
#wc 動く(うご) - to move
#wp 難しい(むずか) - difficult
```

Ask:

> "Which of these do you want to keep? List the numbers or say 'all' / 'none'."

Format confirmed words only as the final `# Words to extract` list.

Rules for formatting:
- Readings are inline after each kanji using ASCII parentheses: `kanji(reading)` — e.g. `明日(あした)`
- Katakana-only words: no reading parentheses
- Suru nouns (n./G3): use #w with `(する)` appended — e.g. `#w 入院(にゅういん)(する) - hospitalization / to be hospitalized`
- な-adj entries: use #wp

---

### Step 6 — Write session file

Before writing, check that `JPLessons/Reading/` exists using Bash: `test -d "/Users/michallebioda/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianJP/JPLessons/Reading"`. If it does not exist, stop immediately and report: "JPLessons/Reading/ not found — check iCloud sync and create it manually." Do NOT create the directory.

Write the session file to `JPLessons/Reading/Reading-session-YYYYMMDDTHHMMSS.md` BEFORE asking about fill-templates. The file must be written even if the user later declines fill-templates.

**Exact file structure (preserve field order):**

```
TARGET DECK: JLPT-Reading
# Passage

[passage as pasted — no furigana added]

# Questions

[questions exactly as shown in Step 3]

# Results

[full explanations from Step 4]

# Words to extract

[confirmed #w/#wc/#wp lines — or leave section empty if none]

# Summary

```

Rules:
- `TARGET DECK: JLPT-Reading` must be on line 1 with no blank line before it.
- `# Summary` must always be present and always empty (no content, no blank lines after the heading other than what ends the file).
- Do not add any `<!--ID:-->` lines — the Obsidian-to-Anki plugin generates them on first export.
- Do not add furigana anywhere in the passage, questions, or results sections.
- The timestamp in the filename is today's date and current time in YYYYMMDDTHHMMSS format (ISO 8601 compact datetime).

After writing, confirm:

> "Session file written: JPLessons/Reading/Reading-session-YYYYMMDDTHHMMSS.md"

---

### Step 7 — Offer fill-templates

Ask:

> "Do you want to run fill-templates on this session file now to generate Anki cards from the words?"

- If yes: load `.cowork/skills/fill-templates.md` and follow its instructions exactly. The `# Words to extract` section feeds the vocabulary; fill-templates outputs into `# Summary`. (Interface note: fill-templates uses `fill_extract.py` which scans for `#w`/`#wc`/`#wp` tags anywhere in the file above `# Summary`, so `# Words to extract` is already a valid source with no changes needed to fill-templates.)
- If no: inform the user that the file is saved and fill-templates can be called manually at any time with "fill templates JPLessons/Reading/Reading-session-YYYYMMDDTHHMMSS.md".

---

## What this skill does NOT do

- Does not generate its own passages — authentic user-pasted content only.
- Does not maintain a persistent state JSON — session files in `JPLessons/Reading/` are the record.
- Does not add furigana to passage text, questions, or results (furigana only on vocabulary lines in # Words to extract).
- Does not suggest words when the user scored 100% and Step 2 found no above-N4 items.

---

## Never touch

- Lesson files under `JPLessons/` other than the session file being written (read-only)
- `<!--ID: -->` lines anywhere
- `TARGET DECK` lines in existing files
- Do not run `git push` or any remote git operation
