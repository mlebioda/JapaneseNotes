# Grammar File Templates

Used by `extract-grammar.md` Steps 6c, 6c-ii, 6d, 7, 9.

## Grammar point file (Step 6c)

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

> [One-line English gloss]

## Structure

[Formation rule]

## Examples

[One bullet per sentence — section header is always present; leave the body empty if the lesson has no examples]

## Use Cases

[Optional — omit if gloss covers it]

## Notes

[Optional — omit unless a cross-pattern comparison table with no standalone file yet]
```
Section order: Structure → Examples → Use Cases → Notes (per `_conventions.md`).

## Container file (Step 6c, non-routed containers)

```
---
lesson: <lesson-code>
pattern: <exact heading text>
topic_slug: ""
level: <N5 | N4 | N3 | N2 | N1>
proofread: false
---

# <exact heading text>

> <One-line description of the group>

## Sub-topics

- [<pattern>](/JapaneseNotes/grammar-index/grammar/<slug>) · <level>
```
List only classified (`grammar`/`container`) sub-headings, never `skip`. No `## Notes` on creation.

## Vocabulary leaf file (Step 6c-ii)

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
Body: flat or numbered per `_conventions.md` "## Structure format" (chosen per the sense-count prompt in 6c-ii). No `function`, `## Use Cases`, `## Notes`, `## Register`, `## Often confused with`.

## Vocabulary POS-consolidated file (Step 6d, first creation only)

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
No `lesson:` (spans many lessons — provenance stays in the linked leaf file). No `level:` (per-bullet instead). `<pos>` ∈ verbs/nouns/adjectives, file name `vocabulary-<pos>.md`.

Bullet format (both themed and ungrouped): `- [<label>](/JapaneseNotes/grammar-index/grammar/vocabulary/<subdir>/<slug>) · <level>`

## Topic file (Step 7)

```
# <Topic Name>

> <One-line description>

## Entries

- [<pattern>](/JapaneseNotes/grammar-index/grammar/<slug>) · <level>

## See also

- [<related-topic>](/JapaneseNotes/grammar-index/<related-topic>) — <short reason>
```
Filename: kebab-case, reusable (`reasons-causes.md`, not `kara.md` or `n5-particles.md`).

- Title (`# <Topic Name>`): a human-readable derivation of the filename, not the filename verbatim.
- Description (`> <One-line description>`): one sentence explaining when to look at this topic.
- `## See also`: 1–2 full absolute URL links to existing related topics if the relation is obvious; otherwise omit the section entirely.

## index.md (Step 9)

```
# Grammar Index

## Verbs
- [verbs-forms](/JapaneseNotes/grammar-index/verbs-forms) — <description>

## Particles
- [particles-wa-ga](/JapaneseNotes/grammar-index/particles-wa-ga) — <description>

## Patterns
...
```
Fixed groups: Verbs (`verb-*`) / Adjectives (`adjectives-*`) / Particles (`particles-*`) / Patterns (sentence-level: reasons, comparisons, suggestions, conditionals) / Forms & Counters (counters, time, numbers) / Other. Omit empty groups.
