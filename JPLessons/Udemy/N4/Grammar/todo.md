Missing topic
- [x] 行ったことがありました
- たがっている
- want for other person
- think for other person
- Casual equivalent: だろう (used with friends and family).でしょう

- [x] if often confused with - write register or something without indicating answer

- Search form missing n5 and n4 topics
    - maybe worth to temp-index first:
        - if topic exist: update missing info (examples may be skipped, just knowledge)
        - if topic not exists (I'll make 2 files N5-grammar-leftovers, and same for N4):
            - add file to relevant jlpt file
            - refine with AI
            - extract grammar
            - practice grammar
    - assign to correct folders 
    - migrate vocabualry (needs separate deck and searching for redundand words)
    - check whether any topic or subtopic missing
        - add missing topics



- make consistent - extract grammar and practice grammar
    - after extraction 
        - keep interpreting as a reference optional legacy file
    - [x] split skills to 2
        - for file
        - for scheduled
- analyze skill/agents and 1 file structure to plan how to use ontology for words - maybe fetch definition to flashcard
- Vocab extraction - think how to handle in good order
    - separate for deck, and just list maybe


**extract grammar**
- skills for grammar and vocab  should share logic, no duplication
**Done**

**Practice grammar skill (when no leftovers):**
1. Process file mode
- no initial exercises get list of topics and go to the study mode
- vocab source - lesson file or vocab if not exist
- after study mode - print list and ask for selfevaluation (ignore study mode)
2. scheduled - standard:
- vocab source - global decks
- Read topics
- ask for batch number
- each batch 
    - self evaluation
    - ask for study mode
- after last batch
    - update grammar state (with load control)
    - produce calendar file



## Prompts


analyze practice grammar skill. verify, whether on uncovered topic left in grammar state json file and index-grammar grammar topic. It should be backward compatible 





```markdown
Review and correct the Japanese grammar/vocab notes in [FILE]. Work heading by heading — I'll paste each `##`/`###` section and you review just that one before moving to the next. Do NOT edit anything without my explicit approval first; present findings and wait for a "yes"/go-ahead.

For each section, check:

1. **Typos** — English spelling/grammar errors (missing articles, wrong verb agreement, misspellings), missing spaces before parentheses, mismatched full-width/half-width parentheses （）vs (), misplaced **bold** markers (must wrap the actual target word, not split mid-word or cross word boundaries), stray leading/trailing spaces before `#w` tags, furigana typos (e.g. a kanji's reading slot accidentally repeating the kanji itself instead of giving the actual reading).

2. **Formatting bugs that break card generation** — multiple `#w` tagged lines merged onto a single line without a break (must be split), non-example content (meta-notes, structural remarks) incorrectly tagged `#w` (should be de-tagged into plain prose instead, since it would generate a nonsense flashcard).

3. **Incorrect information** — wrong conjugations, wrong particle usage, mistranslations (e.g. confusing two similar-looking words, like 荷物 "package" vs "mail," or 日本中 "throughout Japan" vs 世界中 "whole world"), incomplete translations that drop a nuance word present in the Japanese (e.g. 必ず "surely" not reflected in the English gloss), English translations that don't match the actual Japanese grammar (e.g. tense/mood mismatches like "would" vs "will"), awkward inline annotations glued into a translation that break natural English (e.g. "walks(noun) fast").

4. **Missing information** — Structure bullets listed without a matching example (when sibling bullets all have one), general grammar principles that are only implicitly demonstrated through examples but never explicitly stated as a rule, missing conjugation forms (e.g. only past-tense examples shown when the pattern also attaches to plain/dictionary form), commonly-confused sibling constructions worth a one-line clarifying note (e.g. はずだった vs はずではなかった).

5. **Register** — add a short "Register:" note when the pattern has a meaningful politeness/formality tendency (neutral, polite-context typical, tiered) — skip it if there's nothing notable to say, don't force one.

6. **Confusable-topic comparisons** — search `grammar-index/grammar/*.md` and `grammar-index/index.md` (topic-based index) for existing pages covering related or easily-confused patterns (similar surface form, similar English gloss, or same topic_slug/function). When a genuine match exists, add a "**Don't confuse with [Label](/JapaneseNotes/grammar-index/grammar/<slug>)**" note with a 1–2 sentence distinguishing explanation. Only link to pages that actually exist — don't invent links. If uncertain whether a term/kanji choice is a real error or the instructor's own coined terminology (and there's no internal proof either way), flag it for me to decide rather than silently "fixing" it — unless there's confirming evidence elsewhere in the same file (e.g. the correct spelling used in another section), in which case fix it and note why you're confident.

**After every fix to a grammar-body example, check the `# Summary` section for the same sentence** — it often duplicates the content, sometimes already correct (skip it), sometimes carrying the identical error (fix to match). When adding a brand-new example that has no Summary card yet, add one in the established format:


```

[Plain English translation, no pipe-note unless needed for disambiguation] #k #card [Japanese sentence with inline furigana, kanji(reading)] <a href="https://kanji-trainer.org/Mnemonic_phrase/Mnemonic_<kanji>.html"><kanji></a> [...one link per unique kanji in the sentence, no duplicates]
 <!--ID: [epoch milliseconds, via `date +%s%3N`, unique per card]--> 

```

**Card front rule:** the front (text before `#card`) must never reveal the specific Japanese pattern/word being tested — that defeats the flashcard. Only add a `| note` on the front when two cards would otherwise have identical/near-identical English fronts and there'd be no way to know which construction to produce; in that case the note should name the grammar *category* only (e.g. "passive form" vs "resultative construction"), never spell out the actual Japanese answer.

Go through the file section by section in this style; I'll indicate which heading to look at next.

```

Start with analyzing un4gl5.

don't modify anything without my permission



## practice grammar standarization

--
  standardize header processing in extract-grammar and practice-grammar

  ## Problem

  `extract-grammar.md` and `practice-grammar.md` each independently derive a grammar
  point's "slug" and stored heading text from the same lesson-file headings, using
  two different, unshared algorithms. This causes real drift between
  `grammar-index/grammar/*.md` files and `.cowork/progress/grammar-state.json`
  entries for the same grammar point, discovered while auditing UN4GL8/UN4GL9:

  1. **Verbatim vs. paraphrase.** `extract-grammar`'s `pattern:` frontmatter field is
     contractually "the exact heading text, unchanged" (Step 7 rules). But
     `grammar-state.json`'s `grammar_header` field — written by `practice-grammar`
     sessions — is not reliably verbatim. Found in the wild:
     - Missing suffix: stored `必要（ひつよう）` vs. actual heading
       `必要(ひつよう) - essential / necessary, is need to`.
     - Full-width vs. half-width parens on the same entry (`（ひつよう）` vs `(ひつよう)`).
     - Fully reworded: stored `通りに（とおりに・どおりに）` vs. actual heading
       `通(とお)りに。。。 - exactly as, as, just like`.
     - A same-reading kanji typo divergence: stored `受身形（うけみけい）` (with 形)
       vs. the lesson file's actual heading `受身系（うけみけい）` (with 系) — the
       stored header used the "corrected" kanji the lesson itself never had.

  2. **Independent slug/ID algorithms.** `extract-grammar` Step 5 defines a detailed,
     fully-specified slug algorithm (separator handling, kanji+reading-parenthetical
     preference, Hepburn kana romanization table incl. compound kana/っ/ん/ー rules,
     punctuation stripping, positional fallback). `practice-grammar`'s "Grammar point
     ID" section defines its own much looser rule ("slug is the grammar header
     romanized/simplified — lowercase, non-alphanumeric collapsed to `-`, trimmed")
     with none of those edge-case rules spelled out. Nothing forces the two to agree,
     so the same heading can legitimately produce two different slugs/IDs depending
     on which skill derived it.

  3. **Consequence in practice-grammar's own matching.** The lesson-file flow
     (`practice-grammar.md`, Multi-lesson file loading step 2b) locates a grammar
     point by searching the lesson slice for a heading matching the stored
     `grammar_header`, trying exact → case-insensitive → whitespace-normalised. None
     of these strategies survive the drift above, so the entry gets silently skipped
     with a warning (the file already documents this failure mode as the "Migration
     note" under Parsing, but only as something to detect-and-warn, not prevent).

  4. **Downstream effect discovered today:** because of (1)+(2), several
     `grammar-state.json` entries for UN4GL8/UN4GL9 had drifted far enough from
     their lesson headings that they'd have silently orphaned on their next
     scheduled review, and separately, entries created before `_heading-roles.md`'s
     container/point classification existed no longer map 1:1 onto today's
     split-out point files (e.g. a single old `。。。ても。。。` entry vs. today's two
     separate child point files). Both had to be hand-repaired this session
     (`.cowork/progress/grammar-state.json`, commit context: UN4GL8/UN4GL9 grammar
     extraction). That manual repair should not be a recurring chore.

  ## Command

  **Standardize header processing in both files** — `.cowork/skills/lesson-to-web/extract-grammar.md`
  and `.cowork/skills/practice-grammar.md` — so a given lesson heading always
  produces the same slug/ID and the same verbatim text in both
  `grammar-index/grammar/*.md` frontmatter and `grammar-state.json`.

  Things to figure out/decide (open to planner's judgment, not prescribed):
  - Whether to extract `extract-grammar`'s Step 5 slug algorithm into a shared file
    (same pattern as `.cowork/skills/_heading-roles.md`, already loaded by both
    skills) so `practice-grammar`'s "Grammar point ID" section reuses it verbatim
    skills) so `practice-grammar`'s "Grammar point ID" section reuses it verbatim
    instead of restating a looser rule.
  - Whether `practice-grammar` should be instructed to copy the heading text
    byte-for-byte into `grammar_header` (never summarize/paraphrase), mirroring
    extract-grammar's `pattern:` contract.
  - Whether an audit script (there's already `.claude/scripts/grammar-audit.py` for
    grammar-index-internal consistency) should be extended, or a new one added, to
    detect `grammar-state.json` entries whose `grammar_header` no longer matches
    their `lesson_file`'s current heading — so this drift surfaces proactively
    instead of only when a scheduled review silently skips.
  - Whether the fix should also cover the split-container case (an old flat entry
    whose heading is reclassified as a container under later `_heading-roles.md`
    rules, orphaning it against today's child point files) — today's fix for that
    was a manual "duplicate the entry per child, same SM-2 state, new path" repair;
    worth deciding if that should become a documented, repeatable procedure.

  ## Context for planner

  This is process/infrastructure work on the shared lesson-to-web + practice-grammar
  pipeline, not a single-lesson content task. Load `.cowork/skills/lesson-to-web/extract-grammar.md`,
  `.cowork/skills/practice-grammar.md`, `.cowork/skills/_heading-roles.md`, and
  `.cowork/skills/lesson-to-web/_conventions.md` for full context before planning.