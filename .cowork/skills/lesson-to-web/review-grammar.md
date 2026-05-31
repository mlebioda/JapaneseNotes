---
name: review-grammar
description: >
  Review grammar files under grammar-index/grammar/ for substantive correctness
  and missing information. Two user-gated steps: correctness check and missing
  info suggestions. Trigger: "review grammar <file>" or called from preprocess-grammar.
---

# Review Grammar Skill

## Trigger

- "review grammar `<slug>`" — filename without `.md`
- "review grammar grammar-index/grammar/`<slug>`.md" — full relative path
- (called automatically from preprocess-grammar with a list of file paths)

---

## Workflow

Process each file in order. Apply both steps to one file before moving to the next.

If called with **all** mode (from preprocess-grammar "all" answer): skip the handoff prompt at the end and automatically continue to structure-grammar.

---

### Step 5 — Substantive correctness check

Verify the grammar explanation is accurate:
- Structure rules correct (correct conjugation forms listed)
- Example sentences grammatically valid Japanese
- English glosses match the Japanese

May use web search to verify. If something appears incorrect:
1. Present the issue and proposed correction to the user.
2. Wait for user approval before applying any change.
3. If the user declines or defers: skip, leave unchanged, continue to Step 6.

---

### Step 6 — Missing information suggestions

Check whether the file is missing important information:
- Common usage nuances not mentioned
- A major conjugation form not shown
- A frequent learner error not noted

If something is missing: suggest it. Do not add content without user approval. Wait for response before continuing.
If the user declines or defers: skip and continue to handoff.

---

## Handoff summary

After processing all files, print:

```
review-grammar — N files processed

  grammar-index/grammar/<slug>.md
    Substantive: OK
    Missing info: suggested adding negative form examples (user approved)

  grammar-index/grammar/<slug>.md
    Substantive: 1 issue raised, user approved correction
    Missing info: none suggested
```

Then ask (skip if running in **all** mode):

```
Run structure-grammar on these files? (yes / no / all)
```

- **yes** — load `.cowork/skills/lesson-to-web/structure-grammar.md` and pass the file list.
- **no** — end the skill.
- **all** — load structure-grammar, instructing it to continue through see-also-grammar without prompting at the next handoff.

---

## Never touch

- `<!--ID: -->` lines
- `TARGET DECK` lines
- Japanese text — never translate kana or kanji
- Files outside `grammar-index/grammar/`
- Lesson files under `JPLessons/`
- Other skill files or `.cowork/instructions.md`
- Do not run `git push` or any remote git operation
