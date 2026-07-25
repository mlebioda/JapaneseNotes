# lesson-to-web — Ideas: upgrading grammar-index toward an ontology

Status: idea backlog, not a plan. Source: analysis session 2026-07-25 (practice-grammar + lesson-to-web review).
Goal: make grammar-index structured enough that exercise generation can *reason* over relations (confusability, register, function) instead of re-deriving them from prose every session.

## Problem statement

Grammar-index already contains an implicit ontology, but most of it is stored as prose:

| Relation / attribute | Where it lives today | Machine-readable? |
|---|---|---|
| pattern → topic | `topic_slug` frontmatter array | yes |
| topic → patterns | topic file `## Entries` | prose links (dual of topic_slug — can drift) |
| pattern → container | `## See also` | prose links |
| confusable-with + distinguishing test | `## Often confused with` | prose links |
| register | `## Register` | prose |
| semantic contrasts (で vs に) | buried in `## Notes` free text | no |
| prerequisite / builds-on (て-form → ている/ておく) | nowhere | missing |
| formality counterpart (plain ↔ です/ます ↔ keigo) | nowhere — `## Register` names tiers but doesn't link the counterpart pattern | missing |

Corpus is small (~45 files, mostly N5) — structural changes are cheap now, painful at 300 files. Do them **before** backfilling N4 lessons so every file gets the structured form on first write, with no second migration.

## Idea 1 — Mirror Register + Often confused with into frontmatter (highest value)

`register-confusability-grammar` writes both the human-readable section AND machine-readable frontmatter:

```yaml
register: neutral            # or: polite, tiered
confused_with: [de-means-or-method, ni-time-of-occurrence-of-an-action]
```

- Section = human view; frontmatter = machine view (for practice-grammar and any future tooling).
- Bidirectional-backlink writes in Step 9 update the matched file's `confused_with` array too (same scoped proofread-guard exception, still append-only in spirit).
- `_conventions.md` frontmatter section documents both fields; the "no skill modifies frontmatter" rule gets a scoped carve-out for these two fields, owned by register-confusability-grammar.

## Idea 2 — Semantic `function` tag with controlled vocabulary

`topic_slug` values are surface-based (particles-de, time-date-expressions). Real learner confusions are function-based: purpose, cause, permission, obligation, hearsay, conditionals. ように/ために/のに share a *function*, not a surface topic.

```yaml
function: [purpose]
```

- Controlled vocabulary list lives in `_conventions.md` (single source of truth); extract-grammar's classification step assigns it at extraction time alongside `topic_slug`.
- Immediate consumer: register-confusability-grammar Step 9's candidate pool — `function` intersection is a much better confusability prefilter than `topic_slug` intersection.
- Future consumer: discrimination-exercise pool building in practice-grammar.
- Suggested starter vocabulary (extend as N4/N3 material demands): purpose, cause-reason, permission, prohibition, obligation, desire, intention, hearsay-appearance, conditional, temporal, comparison, existence-location, means-method, direction-destination, quantity-counting, request, giving-receiving, potential, passive-causative, formality.

## Idea 3 — Strict format for the distinguishing test

Current rule: "one line each with a short reason" — free prose. Enforce:

```
- [Label](/JapaneseNotes/grammar-index/grammar/<slug>) — test: <one-line question that picks between the two>
```

The `test:` line is literally the feedback a discrimination exercise should show on a wrong answer ("does the preceding verb name a controllable action, or a hypothetical one?"). Strict prefix ⇒ extractable without NLP.

## Idea 4 — One-time backfill: promote Notes-buried contrasts into Often confused with

Several existing files already contain perfect confusability data as `## Notes` prose — e.g. `de-where-the-action-will-take-place.md` has the で vs に minimal pair with examples. A one-time content pass over the ~45 existing files:

- Detect "X vs Y" contrast blocks in `## Notes`.
- Move/copy them into `## Often confused with` (+ frontmatter mirror per Idea 1), phrased as a `test:` line.
- Keep the example minimal pair in Notes if it serves the pattern itself; the *relation* moves to the structured section.

This seeds the confusability graph with confusions already documented, before any new backfill runs.

## Idea 5 — `builds_on` prerequisite relation (later, optional)

```yaml
builds_on: [te-form]
```

て-form → ている/ておく/てしまう; ない-form → なくてもいい/なければならない. Useful for exercise sequencing (don't drill ておく when て-form itself is weak) and for a future "prerequisite health check" in SRS. Not needed for the confusion problem — park it until practice-grammar consumption work starts.

## Idea 6 — Dual-representation consistency check

Two data dualities can silently drift:
- `topic_slug` frontmatter vs topic file `## Entries` lists
- `confused_with` frontmatter vs `## Often confused with` section links (once Idea 1 lands)

Add a lightweight audit (could extend `.claude/scripts/grammar-audit.py`) that verifies both directions and reports orphans/asymmetries. Run it as a pipeline self-review step or on demand.

## Sequencing suggestion

1. Ideas 1 + 3 — edits to `register-confusability-grammar.md` + `_conventions.md` (small, one planning round).
2. Idea 2 — touches `extract-grammar` classification + `_conventions.md` vocabulary list.
3. Idea 4 — one-time content pass over existing files (after 1–3 so the target format is final).
4. Ideas 5 + 6 — fold into the future practice-grammar consumption work (see `practice-grammar-ideas.md`).

Related: [[practice-grammar-ideas]] — the consumer side of this data.
