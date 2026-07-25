# practice-grammar — Ideas: consuming grammar-index for better exercises

Status: idea backlog, not a plan. Source: analysis session 2026-07-25.
Deferred by decision: the register/confusability consumption work goes through a later planner → skill-implementer session, after N4 backfill is further along.

## Root cause being fixed

practice-grammar generates exercises from the **lesson file only** (`# 文法` + `# Vocabulary`). It never reads grammar-index. Consequences:

1. **Type 2 discrimination exercises are lesson-scoped by rule** ("group of similar forms *in the lesson*") — but real confusions are cross-lesson: で (UN5GL6) vs に (UN5GL5), ように vs ために vs のに. `grammar-state.json` already records these ("で for action location vs に for existence location (recurred)") but the drill can never target them.
2. **Register/context never appears in exercises or feedback** — lessons teach the form, not the setting; the data now being added to grammar-index (`## Register`) is invisible to the session.

## Idea 1 — Resolve lesson grammar points to grammar-index files

At session start, for each parsed grammar point, compute the extract-grammar slug and check `grammar-index/grammar/<slug>.md`. If present, load frontmatter (+ Register / Often confused with sections) as an *enrichment layer* on the `{grammar_header, body_text}` triple. Missing file = degrade gracefully to current behavior (index coverage is partial and always will be mid-backfill).

Cheapest if lesson-to-web Idea 1 (frontmatter mirrors `register:` / `confused_with:`) lands first — then this is frontmatter reads, no prose parsing.

## Idea 2 — Cross-lesson discrimination drills from the confusability graph

Relax Type 2's "in the lesson" restriction: when a session grammar point has `confused_with` entries, the confusable *set* (from grammar-index, regardless of source lesson) qualifies as a discrimination group.

- Distractors = the confused_with patterns; all genuinely plausible by construction (that's what the relation asserts).
- Wrong-answer feedback = the stored `test:` line from `## Often confused with` — the distinguishing question, verbatim, instead of ad-hoc explanation.
- Vocabulary rule unchanged (session vocab pool first, N5 fillers otherwise) — only the *grammar* side goes cross-lesson.

## Idea 3 — Register-aware exercises and feedback

Two uses of `## Register` / `register:` data:

- **Feedback**: when grading, if the produced form is grammatical but register-wrong for the described situation, say so explicitly ("grammatical, but ちょうだい is casual — the prompt described talking to your boss").
- **New exercise angle (Type 1/3 variant)**: the situation prompt specifies the listener/setting ("ask your teacher…", "tell your little brother…") and grading requires the register-appropriate variant. Only for points whose register is not neutral — neutral-register points gain nothing from this.

## Idea 4 — Structured weak_points: bridge SRS to the confusability graph

weak_points are free-text strings today. When a mistake is a confusion between two indexed patterns, record it structurally alongside the prose:

```json
"confusions": [
  {"with": "ni-time-of-occurrence-of-an-action", "count": 2, "last": "2026-07-20"}
]
```

Payoff loop: recurring confusion pair → next session auto-includes a Type 2 discrimination drill on exactly that pair → feedback quotes the stored distinguishing test → SM-2 tracks whether the *pair* (not just the point) is resolved. This is the endgame the whole grammar-index structure builds toward.

## Idea 5 — Confusion-scope session trigger

New scope alongside TODAY/OVERDUE: "practice confusions" — selects from the structured `confusions` records (Idea 4), sorted by count/recency, and runs pure discrimination drills (Types 2/6) on the pairs. Small addition once Ideas 1–4 exist; meaningless before.

## Idea 6 — Prerequisite-aware sequencing (needs lesson-to-web `builds_on`, optional)

If a drilled point has `builds_on: [te-form]` and て-form itself has low ease / recent failures in grammar-state.json, prefer production exercises that exercise the prerequisite inside the target construction, and mention the prerequisite in feedback when it is the actual error site ("the ておく choice was right; the て-form of 待つ was wrong"). Park until lesson-to-web Idea 5 exists.

## Constraints to respect (unchanged from current skill)

- Lessons stay read-only; grammar-index stays read-only for this skill (only lesson-to-web skills write it — practice-grammar *may* write the new `confusions` records to grammar-state.json only).
- Furigana rule, exercise gates 1–3, batch-gate interaction rules, SM-2 mechanics — all unchanged.
- Graceful degradation everywhere: no grammar-index file, no `confused_with`, no register data ⇒ behave exactly as today. Enrichment is additive, never a dependency.

## Sequencing suggestion

1. Idea 1 (resolution + enrichment loading) — the foundation; ship alone first if needed.
2. Ideas 2 + 3 together — the visible quality jump (cross-lesson discrimination + register feedback).
3. Idea 4 — structured confusions in grammar-state.json.
4. Ideas 5 + 6 — follow-ons once data accumulates.

Depends on: [[lesson-to-web-idea]] — ideally its Ideas 1–3 land first so this skill reads frontmatter, not prose.
