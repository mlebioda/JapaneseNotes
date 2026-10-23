# Findings by topic — grouped view for note-extraction planning

Source: `findings.md` (219 individual finding bullets across 90 file-chapters).
This file consolidates those into **one entry per underlying grammar/vocab
gap**, listing every source file it appears in (with line refs) instead of
repeating the same explanation per file. Purpose: decide what can become one
grammar-index note vs. what's too thin/vocab-level/uncertain to bother with.

Each entry has:
- **Status** — `GAP` (no coverage anywhere) or `UNCERTAIN` (near-miss/variant/
  register question — needs a judgment call before treating as a real gap)
- **Files** — every source file + line ref where this topic was found
- **Why not covered** — consolidated reasoning (which grammar-index files
  were checked and why they don't match)
- **Note-worthiness** — my read on whether this has enough material/breadth
  to justify a standalone note, purely to help you triage

Categories are grouped by what kind of note they'd become, not by JLPT level
or lesson order.

## Udemy-covered topics removed (2026-09-11)

17 topics originally listed here turned out to already be covered by the
current Udemy course, found under `grammar-index/grammar/` — either because
the original per-topic check missed the right file, or because
`UN5GL1L2`–`UN5GL6` hadn't been run through `extract-grammar` yet and have
since been extracted. They've been deleted from this file rather than kept
as resolved entries.

**Already covered, wrong file checked originally (7):** N1 (な-adj+なの →
`no-meishika.md`), I3 (apology hierarchy → `vocabulary/Nouns/im-sorry.md`),
J4 (なる+plain negative → `you-ni-narimasu-naku-narimasu.md`), H1
(V-stem+たい → `hoshii-i-want-n.md`), I5 (plain+と思う →
`vocabulary/Verbs/i-think-toimasu.md`), G2 (plain-object もらう／くれる／
あげる → `kureru-giving-receiving.md` + `ageru.md` + `morau.md`), D2 (さい
counter → `vocabulary/Nouns/years-old.md`).

**Covered once `UN5GL1L2`–`UN5GL6` were extracted (10):** A3 (ない形 →
`nai-form.md`), B1 (へ → `he-ni-direction-destination.md`), B2 (で-means →
`de-means-or-method.md`), B3 (で-location →
`de-where-the-action-will-take-place.md`), B8 (どうやって →
`douyatte-how-to.md`), D3 (clock time → `hour.md`/`minutes.md`), D4 (じかん
duration → `period-of-time.md`), D5 (間-duration suffix →
`days.md`/`weeks.md`/`years.md`), E1 (ある／いる existence →
`p-ni-n-ga-arimasu-imasu-there-is-something-somewhere.md` +
`something-is-somewhere.md`), E2 (positional nouns → `directions.md` + the
E1 files).

The いつも half of O6 and the ね half of C1 resolved the same way but those
two topics are kept below, trimmed, since their other half (よく, and
な／の／ぜ／ぞ respectively) is still genuinely open.

**Topic count after removal: 49 distinct topics remain** (down from 66),
grouped into 14 categories (A–M, O — category N is now empty and removed).

---

## A. Verb conjugation mechanics (forms)

The single biggest gap cluster in the whole vault: nothing documents the
mechanical dictionary-form → X-form conversion rules by verb-ending group.
Every existing file (`i-adjective-conjugation.md`, `na-adjective-conjugation.md`,
`te-form.md`, etc.) either covers *adjectives* or assumes a verb form is
*already formed* and documents only its *use*. The ない形 half of this family
is now covered (`nai-form.md`, extracted from `UN5GL6`) — these three
remaining forms are naturally one family — arguably **one note "Verb
conjugation by group" with three sections (ます／て／た)** rather than three
separate notes, since the underlying content (godan/ichidan/irregular
endings) is the same table reused each time.

### A1. ます形 conjugation by verb-ending group (present + past)
- **Status:** GAP
- **Files:** `Semest1/L13/GramatykaS1L13.md` (60-72, present), `Semestr2/L08/GramatykaS2L8.md` (30-49, past — "this is the past-tense half of that gap"), `Semestr3/L1/GramatykaS3L1.md` (63-93, present), `Semestr6/S6L11.md` (174-261, combined with て/ない/た forms)
- **Why not covered:** No file for basic present- or past-tense ます形 conjugation by group, unlike adjectives which have their own dedicated files.
- **Note-worthiness:** Moderate — 4 files, and this is the most fundamental conjugation a learner needs.

### A2. て形 formation rules by verb-ending group
- **Status:** GAP
- **Files:** `Semestr2/L10/GramatykaS2L10.md` (44-90), `L11` (1-10, 27-127), `L12` (1-9,15-27,45), `L13` (1-9,71-81), `Semestr3/Podsumowanie semestr 3.md` (35-49,71-79), `L09` (1-15, Powtórzenie), `L10` (1-15, Powtórzenie), `Semestr4/L01/GramatykaS4L1.md` (15-40), `L13` (15-23), `Semestr6/S6L11.md` (174-261, combined with ます/ない/た forms)
- **Why not covered:** `te-form.md`/`te-form-sequencing-order.md` both assume て形 is already known and document only its sequencing *use*, never the う／つ／る→って, む／ぶ／ぬ→んで, く→いて, ぐ→いで, す→して conversion rules.
- **Note-worthiness:** **Strong** — appears in 9 distinct files, most with full worked tables. Highest-value candidate in this whole audit.
- ⚠️ **Udemy check:** `UN5GL6`'s header explicitly announces "ないけい、てけい、たけいを理解する" and has stub `#### て けい` headers (in both the working section and the Grammar Summary), but **they're left completely empty** — no structure, no examples. So unlike ない形, this is a genuine content gap even in the current official course, not just an extraction gap.

### A4. た形 (plain past) conjugation by verb-ending group
- **Status:** GAP
- **Files:** `Semestr3/L10/GramatykaS3L10.md` (70-81,83-111), `Semestr4/L06/GramatykaS4L6.md` (151-222), `Semestr6/S6L11.md` (174-261, combined with ます/て/ない forms)
- **Why not covered:** Same reasoning as A2 — `te-form.md` family and everything built on top of た形 (`tokoro-desu-ta-form.md`, `ta-bakari.md`, `ta-kotogaarimasu-have-you-ever.md`) all assume た形 conjugation as a given.
- **Note-worthiness:** Moderate — 3 files but full worked drills each time.
- ⚠️ **Udemy check:** Same `UN5GL6` lesson announces た形 too (stub `#### た けい` header) but it's equally empty — not actually taught anywhere in the current course either.

---

## B. Core particles

### B4. に — stative-location particle (residence/existence)
- **Status:** GAP
- **Files:** `Semestr3/L5/GramatykaS3L5.md` (102-106,117-118), `L6` (170-171, recurrence), `Semestr4/L04/GramatykaS4L4.md` (106-112), `Semestr5/L11/GramatykaS5L11.md` (222)
- **Why not covered:** `particles.md` only has よ; this is に marking *where something exists/resides* (すむ／いる／ある), distinct from action-location で.
- **Note-worthiness:** Strong — 4 files. **Pairs well with a location-particles note** since several files (L5, L6) explicitly teach it as a contrast pair with で.

### B5. から — spatial/temporal starting-point particle ("from")
- **Status:** GAP
- **Files:** `Semestr5/L10/GramatykaS5L10.md` (74-91), `L11` (38-40, から〜まで), `Semestr6/L01/GramatykaS6L1.md` (53, から来ました)
- **Why not covered:** `kara-because.md` only covers the causal ("because") sense; `made.md` covers まで but not the paired origin particle.
- **Note-worthiness:** Strong — 3 files, and pairs naturally with the existing `made.md` (could even be added as a section there, or as a "から...まで" companion note).

### B6. について — "about/regarding"
- **Status:** GAP
- **Files:** `Semestr4/L05/GramatykaS4L5.md` (61-69), `Semestr5/L3/GramatykaS5L3.md` (112-113,155), `Semestr6/L10/GramatykaS6L10.md` (111-112,119,124-125)
- **Why not covered:** Zero matches anywhere in `grammar-index/grammar/` for について/tsuite.
- **Note-worthiness:** Strong — 3 files, clean single-pattern note.

### B7. と vs に with 会う-type verbs (companionship "with" vs. target of meeting)
- **Status:** GAP
- **Files:** `Semestr4/GramatykaPodsumowanie.md` (24-28), `L01/GramatykaS4L1.md` (26-28,68-72,78-81)
- **Why not covered:** No file addresses this と/に distinction at all.
- **Note-worthiness:** Moderate — 2 files, but a clean, teachable contrast pair.

### B9. なにか／だれか／どこか + に／で combinatorial particle marking
- **Status:** UNCERTAIN
- **Files:** `Semestr5/L12/GramatykaS5L12.md` (53-90)
- **Why not covered:** `dareka-someone.md`/`dokoka-somewhere-anywhere.md` only document the bare indefinite pronoun, not this に(target)/で(means) attachment pattern.
- **Note-worthiness:** Weak — single file, may just be compositional (indefinite pronoun + already-known particle rule) rather than a new grammar point. Needs a judgment call.
- **Udemy check:** `UN5GL11` teaches どこか（へ）+V and どこも/どこへも with full structure (extracted in `dokoka-somewhere-anywhere.md`/`dokomo-dokohemo-nowhere.md`) — but that's the へ-attachment pattern, not the に/で combinations this entry specifically flags. Adjacent, not a direct resolution — still needs the judgment call noted above (is B9 about a different particle than what's actually taught?).
- **DECISION:** Skip. This is compositional — なにか／だれか／どこか already exist as indefinite pronouns, and に/で are already-taught particles; attaching one to the other isn't a new grammar point worth its own note.
- **STATUS:** Confirmed 2026-09-12, no action needed (Skip = no-op).

### B10. に as source-of-transfer marker with もらう-type verbs
- **Status:** UNCERTAIN
- **Files:** `Semestr5/L12/GramatykaS5L12.md` (90)
- **Why not covered:** Related to the giving/receiving gaps (see G-section) but calls out に's specific role.
- **Note-worthiness:** Weak — single mention, likely folds into whichever giving/receiving note gets written, not a standalone topic.
- **DECISION:** Skip — に here is just part of もらう's existing structure (already documented in `vocabulary/Verbs/morau.md`), not a separate grammar point to track.
- **STATUS:** Confirmed 2026-09-12, no action needed (Skip = no-op).

### B11. と — quotative marker for onomatopoeia/mimicry
- **Status:** UNCERTAIN
- **Files:** `Semestr6/L01/GramatykaS6L1.md` (81)
- **Why not covered:** Existing と-files all cover thought/speech verbs, not sound-mimicking words.
- **Note-worthiness:** Very weak — single instance (ワンワンとほえますか), likely too narrow for its own note. Probably skip or fold into vocabulary notes on onomatopoeia if those exist.
- **DECISION:** New file. Drafted into Leftovers-<N>.md for later extract-grammar processing (see STATUS for exact file).
- **STATUS:** Drafted 2026-09-12 into JPLessons/Udemy/N4/Grammar/Leftovers-1.md — pending user review, then extract-grammar.

---

## C. Sentence-final particles & discourse connectors

### C1. な／の／ぜ／ぞ sentence-final particles (register/gender/emphasis family)
- **Status:** GAP
- **Files:** `Indywidualne/L2.md` (57-77,166-176,202-217 — な), `L8.md` (13-30), `L10.md`-`L16.md` (recurring boilerplate, ~14-31 each), `Semestr3/Podsumowanie semestr 3.md` (146-155 — の and な), `L09` (109-195 — full な/の/ぜ/ぞ family with register notes), `Semestr4/L03/GramatykaS4L3.md` (71-78), `Semestr6/L05/GramatykaS6L5.md` (51,71), `L06` (52)
- **Why not covered:** No file addresses な／の／ぜ／ぞ as sentence-final particles. ね itself is now covered separately (see Udemy check).
- **Note-worthiness:** **Strong** — appears in ~13 files. `Semestr3/L09` is the richest single source (has the fullest structure/register breakdown incl. ぜ/ぞ). Natural "one note per particle" cluster (na.md, no-sentence-final.md, ze-zo.md) or one combined "sentence-final particles" note.
- **Udemy check:** ね itself is now covered via `ne-seeking-approval.md` (extracted from `UN5GL1L2`), and `deshou-seems-right.md`'s stale "ね particle (not yet in grammar-index)" note should be updated to point at it. な／の／ぜ／ぞ remain fully open — no source material identified for them anywhere in the current Udemy course.

### C2. ところで — topic-change discourse marker ("by the way")
- **Status:** GAP
- **Files:** `Semestr6/L02/GramatykaS6L2.md` (216) — also in `GramatykaS6L2 1.md` (same content, later fill-templates version)
- **Why not covered:** `conjunctions.md` only covers くて／で "and" and contrastive が.
- **Note-worthiness:** Weak alone (1 source) but a clean, common, teachable discourse marker.
- **DECISION:** New file. Maps to JLPT-N3-Grammar-List.md's confirmed ところで gap — drafted as the vault's first N3-level content.
- **STATUS:** Drafted 2026-09-12 into JPLessons/Udemy/N3/Grammar/Leftovers-1.md (first N3 folder/Leftovers file in the vault) — pending user review, then extract-grammar.

### C3. じゃあ — discourse transition ("well then / so")
- **Status:** UNCERTAIN
- **Files:** `Semestr6/L02/GramatykaS6L2.md` (226)
- **Why not covered:** Not addressed anywhere.
- **Note-worthiness:** Weak/borderline — could be vocab rather than grammar. Pairs naturally with C2 as a small "conversational transition words" note if you want one.
- **DECISION:** Vocab, not grammar. No master-list anchor at any level (checked N5/N4/N3), doesn't clear the new-file gate as a grammar point — added as a `#w` vocabulary card instead.
- **STATUS:** Added 2026-09-12 to `JPLessons/Udemy/N4/Grammar/Leftovers-1.md`'s new `# Vocabulary` section (two cards: bare じゃあ + the source example sentence). Not a grammar-index candidate.

### C4. どうしますか vs 何をしますか — usage-nuance contrast
- **Status:** UNCERTAIN
- **Files:** `Semestr6/L02/GramatykaS6L2.md` (191-194)
- **Why not covered:** Not addressed anywhere.
- **Note-worthiness:** Weak — single file, could be judged vocab-level rather than grammar. Low priority.
- **DECISION:** Vocab. Source's own `#g` note (Polish) shows a real, non-interchangeable nuance (どう = decision/approach to a situation, 何を = naming a concrete activity), not just a compositional overlap — but single-instance and no master-list anchor at any level, so two vocab cards + a comparison note rather than a grammar file or fold-in.
- **STATUS:** Added 2026-09-12 to `JPLessons/Udemy/N4/Grammar/Leftovers-1.md`'s `# Vocabulary` section — two chapters (どうしますか, 何をしますか), each with its own `#w` card, plus a shared comparison note.

### C5. と言ったら — free-association "when you say X, [it makes you think of] Y"
- **Status:** GAP
- **Files:** `Semestr6/L03/GramatykaS6L3.md` (137-147)
- **Why not covered:** `toiuimidesu-means.md` covers という意味です (defining a term), a different function.
- **Note-worthiness:** Weak-moderate — single file but a distinct, real pattern (word-association game), not vocab.
- **DECISION:** New file. Maps to JLPT-N3-Grammar-List.md's confirmed と言えば gap (と言ったら is the same pattern, slightly more emphatic variant) — drafted alongside C2 as N3 content.
- **STATUS:** Drafted 2026-09-12 into JPLessons/Udemy/N3/Grammar/Leftovers-1.md — pending user review, then extract-grammar.

---

## D. Counters

All minor/vocabulary-adjacent, but this system does treat individual counters
as their own grammar-index files (`dai-counter.md`, `satsu-number-of-books.md`,
etc.), so these are legitimate gaps in that same style — likely best handled
as a **batch of small per-counter entries** rather than one big note, matching
the existing pattern, OR one consolidated "counters not yet covered" note if
you'd rather not create a dozen one-line files.

### D1. Assorted counters — かげつ, かこく, かしょ, かん(volume), きょく, きれ, くち, くみ, けん(case/building), ご(words), しゅるい, しゅう
- **Status:** GAP
- **Files:** `Indywidualne/L1.md` (1-65)
- **Why not covered:** Not among the counters in `counters.md`/`counter-sufixes.md`.
- **Note-worthiness:** Weak — source file itself is sparse/fragmentary raw notes, few examples. Low extraction value.

### D6. 度（ど）— counter for degrees/temperature
- **Status:** GAP
- **Files:** `Semestr6/L04/GramatykaS6L4.md` (57-60)
- **Note-worthiness:** Weak — single mention, simplest possible addition (one counter word).

---

## E. Existence, possession & need

### E3. 要る／いります — "to need" (distinct from 必要)
- **Status:** GAP
- **Files:** `Semestr3/Podsumowanie semestr 3.md` (91-96,207-208), `L07` (38-58), `L08` (23), `L09` (23), `L10` (23), `Semestr6/L01/GramatykaS6L1.md` (22-23)
- **Why not covered:** `hitsuyou-noun-use-ga-aru-nai.md` covers a different word (必要) and structure (V+必要がある); no file for the verb 要る／いります itself.
- **Note-worthiness:** **Strong** — 6 files, clean single-word/single-pattern note, and a genuinely useful contrast with 必要.
- **Udemy check:** `UN5GL5` only lists it as a bare vocabulary tag ("#wc いる - to need") with no structure or example — thin, matching the source course's own thin treatment. `UN4GL9` teaches 必要 extensively (necessity, な-adjective use, 必要がある/ない) but 要る／いります itself never appears there (confirmed via grep) — so this lesson doesn't touch E3 despite being the natural place to contrast it. Extraction status: not yet extracted anywhere. **Still a genuine gap**, and apparently under-taught in the current course too, not just under-extracted.

---

## F. Requests, directives & desire-of-others

### F1. Vて形 + ください — basic affirmative request ("please do X")
- **Status:** GAP
- **Files:** `Semestr2/L10/GramatykaS2L10.md` (94-104), `L11` (22-127, whole file built around it), `Semestr4/L02/GramatykaS4L2.md` (57), `Semestr5/toimport1.md` (1991,2026), `Semestr6/S6L11.md` (417-418)
- **Why not covered:** `wokudasai-please-give-me.md` is N+を+ください (object request); `vnaidekudasai-please-dont-do-it.md` is negative-only; `o-go-v-masukudasai-respectful-request-form.md` is the sonkeigo variant only. **The single most basic request form in Japanese has no file.**
- **Note-worthiness:** **Very strong** — 5 files, and arguably the highest-priority gap to fix given how fundamental it is.
- **Udemy check:** Confirmed still fully open despite two touchpoints. `UN4GL12`'s 命令形 section mentions てください only as a one-line "softer alternative," never as its own structure. `UN5GL14` uses plain affirmative てください heavily (its own opening example sentence + 4 ひょうげん examples: 電気をつけてください, 手をあげてください, 写真を見せてください, 単語を覚えてください) but never gives it a dedicated 文法 section — only the negative Vないでください gets one, extracted as `vnaidekudasai-please-dont-do-it.md`, which doesn't cross-reference an affirmative counterpart. **The single most basic request form in Japanese genuinely isn't taught as its own point anywhere in the current course either** — this is a real content gap, not just an extraction gap.

### F2. Vないでほしい — negative "I want X to NOT do Y"
- **Status:** UNCERTAIN
- **Files:** `Semestr6/L10/GramatykaS6L10.md` (82-85,156-162,197-200,248-250), `L11` (83-86)
- **Why not covered:** `te-form-hoshii-desu.md` documents only the affirmative Vて形+ほしい; its negative counterpart isn't mentioned.
- **Note-worthiness:** Moderate — appears independently in 2 files with clear examples, confirms it's deliberately taught, not a one-off. Good candidate to add as a section to the existing `te-form-hoshii-desu.md` rather than a new file.
- **Udemy check:** No match found in any of the 29 lessons.
- **DECISION:** Fold in. Added as a negative-counterpart Structure/Examples addition to te-form-hoshii-desu.md rather than a new file.
- **STATUS:** Added 2026-09-12 to grammar-index/grammar/te-form-hoshii-desu.md (Structure + Examples sections updated).

### F3. ほしがる／を — 3rd-person desire, が→を particle switch
- **Status:** UNCERTAIN
- **Files:** `Semestr6/L08/GramatykaS6L8.md` (82-85,94,107-109,122-123,148-151,166-170)
- **Why not covered:** `hoshii-i-want-n.md` mentions 欲しがる in passing for 3rd person but gives no example and doesn't document the が→を shift.
- **Note-worthiness:** Weak as a new file, but a good candidate to **add as a missing detail to the existing `hoshii-i-want-n.md`** rather than write a new note.
- **Udemy check:** `UN5GL13` teaches the same thin one-liner ("3rd person: 欲しがる — describes someone else wanting something," no example, no particle-shift detail) — and `hoshii-i-want-n.md` (extracted from this exact lesson) mirrors that same thinness. **Confirms this is genuinely under-taught in the source course, not just under-extracted** — closing this gap needs new research/examples, not just an extraction pass.
- **DECISION:** New file (gate exception, approved — no master-list anchor at any level, same as B11). Drafted into Leftovers-1.md as its own entry rather than folded into hoshii-i-want-n.md.
- **STATUS:** Drafted 2026-09-12 into JPLessons/Udemy/N4/Grammar/Leftovers-1.md — pending user review, then extract-grammar.

### F4. たがる — 3rd-person "wants to do" (parallel gap, no examples given)
- **Status:** GAP *(not in the original 66-topic audit — surfaced while reviewing F3; same source lesson, same file, same shape of gap)*
- **Files:** `Semestr6/L08/GramatykaS6L8.md` (107-110, 166-171)
- **Why not covered:** `hoshii-i-want-n.md` §2 (Vたい) line 43 states "3rd person: Vます-stem + たがる — describes someone else wanting to do something" but gives no example, same as F3's bare mention.
- **Note-worthiness:** Same shape as F3 — a missing detail (examples) in an already-existing file, clean fold-in.
- **DECISION:** New file (gate exception, approved — no master-list anchor at any level, same as B11 and F3). Drafted into Leftovers-1.md as its own entry rather than folded into hoshii-i-want-n.md.
- **STATUS:** Drafted 2026-09-12 into JPLessons/Udemy/N4/Grammar/Leftovers-1.md — pending user review, then extract-grammar.

---

## G. Giving & receiving

### G1. Vて形 + やる (te-yaru — favor for a lower-status recipient: kids/pets/plants)
- **Status:** GAP
- **Files:** `Indywidualne/L4.md` (whole file), `L8.md` (158-165), `L10.md`-`L16.md` (recurring, ~157-164 each)
- **Why not covered:** `vte-agemasu-kuremasu-moraimasu.md` and its sub-files cover あげる/くれる/もらう but not やる.
- **Note-worthiness:** Strong — 9 files. Natural 4th sub-file alongside the existing あげる/くれる/もらう trio.
- **Udemy check:** No match found — none of the 29 lessons teach やる.

### G3. Plain-object いただく／くださる／さしあげる — honorific version of plain-object giving/receiving
- **Status:** GAP
- **Files:** `Indywidualne/L10.md` (352-374,649-669), `L11.md` (305-327,752-764), `L12.md`-`L16.md` (305-327 each)
- **Why not covered:** Only the Vて形＋いただく／くださる favor construction is covered (`te-form-itadaku-kudasaru-favor-received.md`); no file for the plain noun-object honorific exchange.
- **Note-worthiness:** Strong — 7 files. Honorific counterpart of the (now-resolved) plain-object あげる／くれる／もらう family.
- **Udemy check:** `UN5GL10`'s あげる section has a passing Register note ("giving to someone of higher status... normally calls for the humble さしあげる instead") — names the word but gives no structure/example. Extracted in `vocabulary/Verbs/ageru.md`, which carries forward that same one-line mention verbatim. **Confirms G3 is genuinely under-taught in the source course** (not just under-extracted) — still open, and the more clearly isolated remaining gap in this family.

---

## H. Wanting, needing & skill/preference vocabulary

### H2. とくい／にがて — skill good-at/poor-at (register variant of 上手／下手)
- **Status:** UNCERTAIN
- **Files:** `toimport6.md` (10-13), `Semestr3/Podsumowanie semestr 3.md` (107-121), `L07` (78-103,158-176), `L08` (25-39), `L09` (25-39), `L10` (25-39), `Semestr5/L5/GramatykaS5L5.md` (61-71)
- **Why not covered:** `be-good-poor-at-jouzu-heta.md` covers 上手／下手 precisely (same が-marking structure) but doesn't list とくい／にがて as a variant/entry.
- **Note-worthiness:** Moderate-strong (7 files) but genuinely uncertain whether this warrants its own file vs. being added as a vocabulary note to the existing jouzu/heta file — recommend resolving the uncertainty first before deciding format.
- **Udemy check:** `UN4GL4`'s vocabulary section has a bare `#wp 苦手 (にがて) - weak` tag whose Anki-card note explicitly draws the exact H2 contrast ("subjective — dislike/discomfort with something; compare 下手, an objective assessment of low skill") — but only as a single vocabulary card, no structure/examples. Lesson coverage: **partial (vocabulary-level only)**. Extraction status: **not extracted at all** — confirmed `be-good-poor-at-jouzu-heta.md` (from a different lesson) still doesn't mention とくい／にがて. **Still fully open** — and now with a concrete Udemy source (UN4GL4) to build a real structure/examples section from, if you decide it deserves one.
- **DECISION:** Vocab. Two distinct senses of にがて exist (skill vs preference) — this is the skill sense, added as a #w card set rather than folded into be-good-poor-at-jouzu-heta.md.
- **STATUS:** Added 2026-09-12 to JPLessons/Udemy/N5/Grammar/Leftovers-1.md's new # Vocabulary section (Chapter 1: とくい／にがて skill sense).

### H3. にがて on the すき preference scale (だいすき＞すき＞にがて＞きらい)
- **Status:** UNCERTAIN
- **Files:** `Semestr3/Podsumowanie semestr 3.md` (1-13,123-129), `L1/GramatykaS3L1.md` (45-50)
- **Why not covered:** `suki-kirai-like-dislike.md` documents 好き／嫌い／大好き／大嫌い but has no にがて entry.
- **Note-worthiness:** Weak — single file, and this may just be the same vocabulary word as H2 used in a different sentence slot rather than a separate grammar point. Likely resolves together with H2.
- **DECISION:** Vocab. The preference sense of にがて (distinct from H2's skill sense) — added as a #w card rather than folded into suki-kirai-like-dislike.md.
- **STATUS:** Added 2026-09-12 to JPLessons/Udemy/N5/Grammar/Leftovers-1.md's new # Vocabulary section (Chapter 2: にがて preference sense), cross-referenced against H2's chapter.

### H4. つもりはない — structurally distinct negation of つもり
- **Status:** UNCERTAIN
- **Files:** `toimport6.md` (322-335), `Semestr5/toimport1.md` (1767-1786), `L7` (34-49)
- **Why not covered:** `vplaintsumoridesu-conviction-of-doing-something-planned-by-speaker.md` documents only V「ない」+つもりです; the つもり+はない variant (negating via はない rather than the verb) isn't shown.
- **Note-worthiness:** Moderate — 3 files, confirmed as a deliberately-taught alternate structure (not just a typo) in L7. Good candidate to add as a note/section to the existing つもり file rather than a new one.
- **Udemy check:** `UN4GL5` teaches Vないつもりです (e.g. どうようびにべんきょうしないつもりです) — that's the *already-covered* V「ない」+つもりです variant, not the つもりはない structure this entry is about. No lesson teaches the はない variant — still open.
- **DECISION:** Skip. No exact master-list match, but its closest relatives (つもりだった, つもりで) are both tagged N3 — treated as N3-level, out of scope for now.
- **STATUS:** Decided 2026-09-12, no action taken.

---

## I. Aspect, tense & causal nuance

### I1. ました vs ～ていました — "did once" vs. "used to do (but stopped)"
- **Status:** UNCERTAIN
- **Files:** `Semestr4/GramatykaPodsumowanie.md` (1-22), `L01/GramatykaS4L1.md` (3-22,59-64,93-103)
- **Why not covered:** `teiru.md`/`teiru-show-state.md` cover ongoing action/habit and resultant state but not this specific "used to, but stopped" aspectual nuance vs. plain past.
- **Note-worthiness:** Moderate — 2 files, a real and teachable nuance, though it's more a usage-note than a new structure (ています is already covered; this is about interpreting its past tense specifically).
- **Udemy check:** No match found.
- **DECISION:** Fold in. Added as a past-tense interpretation nuance (ました vs ていました) to teiru-show-state.md §2, rather than a new file — ています itself is already covered, this is purely about reading its past form correctly.
- **STATUS:** Added 2026-09-12 to grammar-index/grammar/teiru-show-state.md §2 (Ongoing Action/Habit section).

### I2. て形 as reason/cause ("X-て、Y" = "because X, Y")
- **Status:** GAP
- **Files:** `Semestr3/L3/GramatykaS3L3.md` (1-53,114-130)
- **Why not covered:** `te-form-sequencing-order.md` explicitly flags this as a *different* function in its own Notes (one bare example only, no structure/examples of its own).
- **Note-worthiness:** Moderate — single file but a real, distinct て形 function that deserves its own examples/structure section (could be added to `te-form.md`'s family rather than a wholly new file).
- **Udemy check:** `UN5GL7`'s て形-sequencing section has the identical passing Notes aside ("て形 is also used to give a reason/cause, e.g. 熱があって、休みました") — one bare example, no structure. Extracted in `te-form-sequencing-order.md`, which reproduces that exact same thin mention. **Confirms findings2's original assessment is accurate** — the extraction faithfully mirrors the lesson's own thin treatment; still a genuine gap needing real development, not just extraction.

### I4. Vて + うれしいです ("glad/happy that ~")
- **Status:** GAP
- **Files:** `Semestr3/Podsumowanie semestr 3.md` (58-61)
- **Why not covered:** `te-form-hoshii-desu.md` covers Vて＋ほしいです, a different function.
- **Note-worthiness:** Weak — single mention, likely too thin alone; could fold into I2 (て形-as-reason) since うれしい examples are basically that pattern.

---

## J. Verb derivation & state-change

### J1. V-stem + だす — "suddenly start doing" (unintentional)
- **Status:** GAP
- **Files:** `Indywidualne/L5.md` (177-228), `L8.md` (49-61)
- **Why not covered:** No file for verb-stem+だす, distinct from 始める and ようになる (both covered elsewhere, discussed as contrasts in the same source lesson).
- **Note-worthiness:** Moderate — 2 files, clean single-pattern note.

### J2. V-stem + つづける — "continue doing"
- **Status:** GAP
- **Files:** `Indywidualne/L6.md` (382-392,462-479), `L7.md` (60-64), `L8.md` (113-117), `L10.md`-`L16.md` (74-78 each)
- **Why not covered:** No dedicated file anywhere.
- **Note-worthiness:** **Strong** — 10 files, very well-attested, easy clean note.

### J3. Noun + する verb formation (verbal nouns)
- **Status:** GAP
- **Files:** `Semestr3/L1/GramatykaS3L1.md` (95-102)
- **Why not covered:** `narimasu-vs-shimasu-change-of-state.md` covers a different pattern (who caused a change of state), not the general noun→verb word-formation rule.
- **Note-worthiness:** Weak-moderate — single file but a genuinely fundamental word-formation rule (りょうりする, せんたくする, etc.) worth documenting once.
- **Udemy check:** `UN5GL7`'s 勉強 section states the same general rule once in passing ("Xを勉強する — follows the general noun＋する pattern... see アルバイトをする, 研究する"), not as a dedicated section. Extracted in `vocabulary/Verbs/benkyou-learn.md`, which carries forward the same generalization — extraction adequately reflects the lesson's own (still partial) treatment. Still open, low priority.

---

## K. Minor sentence-pattern grammar (suggestion, continuation, naming, habitual)

### K1. Vた + まま — "leave/remain in an unchanged state"
- **Status:** GAP
- **Files:** `Indywidualne/L6.md` (208-229,271-274), `L8.md` (226-239), `L10.md`-`L16.md` (216-229 each)
- **Why not covered:** `v-te-okimasu.md` mentions そのまま only in passing; the standalone まま structure (Vたまま, ままだ, ままのN) isn't documented.
- **Note-worthiness:** **Strong** — 9 files.
- **Udemy check:** `UN4GL3`'s Vて形＋おきます section explicitly says "often with そのまま、このまま" and its vocabulary defines このまま／そのまま — but never teaches the true Vたまま／ままだ／ままのN construction. Extracted in `v-te-okimasu.md` — which is in fact the exact file findings2 already cites in its own reasoning. **Confirms the gap assessment is accurate**; no new resolution, just verified.

### K2. Vた + らどう(ですか) — "why don't you / how about"
- **Status:** GAP
- **Files:** `Indywidualne/L6.md` (232-243,276,295-300), `L8.md` (241-246), `L10.md`-`L16.md` (231-236 each)
- **Why not covered:** No dedicated file anywhere.
- **Note-worthiness:** **Strong** — 9 files.

### K3. という — "called/named X" (B という A)
- **Status:** GAP
- **Files:** `Indywidualne/L6.md` (399-411), `L7.md` (16-28,68-74,89-103, incl. っていう contraction), `L8.md` (261-269), `L10.md`-`L16.md` (251-259 each)
- **Why not covered:** `toiuimidesu-means.md` covers というimidesu ("what does X mean"), a different pattern.
- **Note-worthiness:** **Strong** — 10 files.

### K4. ～てもかまわない／かまいません — affirmative "it's fine to do"
- **Status:** UNCERTAIN
- **Files:** `Indywidualne/L6.md` (369-376), `L8.md` (196-200), `L10.md`-`L16.md` (197-201 each)
- **Why not covered:** Only the negative なくてもかまいません is documented; the affirmative variant of てもいい has no file.
- **Note-worthiness:** Strong (9 files) but genuinely a near-miss/register-variant of an already-covered pattern (てもいい) — good candidate to add as a "casual variant" note to `temoiidesuka-permission.md` rather than a new file.
- **DECISION:** Fold in. Same register-tier relationship as the already-covered なくてもかまいません／なくてもいいです negative pair (かまいません = more formal/deferential variant, same meaning) — added to temoiidesuka-permission.md's existing tiered-register scale rather than a new file.
- **STATUS:** Added 2026-09-12 to grammar-index/grammar/temoiidesuka-permission.md (Structure, Examples, and Register sections updated).

### K5. V-dict + ことがある — habitual/occasional occurrence (extends to い/な-adjectives and nouns)
- **Status:** GAP *(upgraded from uncertain — see Semestr7/L01 for the confirming full lesson treatment)*
- **Files:** `Indywidualne/L3.md` (20-27), `Semestr7/S7L1-L2.md` (throughout, extends to adjective/noun forms), `L01/GramatykaS7L1.md` (9-44, full contrastive treatment)
- **Why not covered:** `ta-kotogaarimasu-have-you-ever.md`/`ttakotogaarimashita-...md` cover only the た形 experience/recollection meanings and explicitly warn the dictionary-form variant means something different — but nothing documents that dictionary-form habitual meaning itself.
- **Note-worthiness:** **Strong** — genuinely a full grammar point with its own structure (dict-form vs adjective vs noun variants), confirmed via dedicated lesson content in Semestr7/L01.

---

## L. Comparison & selection

### L1. どれ vs どちら — selection question (3+ options vs. 2)
- **Status:** UNCERTAIN
- **Files:** `Semestr4/GramatykaPodsumowanie.md` (83-84,112), `L12/GramatykaS4L12.md` (45-64), `Semestr6/L05/GramatykaS6L5.md` (155)
- **Why not covered:** `comparsion-dochira-nohouga.md` only documents どちらが＋Adj comparative usage, not the plain "which one of these" selection function; no file for どれ at all.
- **Note-worthiness:** Moderate — 3 files, a real near-miss worth resolving (could be a short addition to the dochira file distinguishing "comparative どちら" from "selection どれ／どちら").
- **DECISION:** Fold in. Added as a new "Selection どれ／どちら (not comparative)" section to comparsion-dochira-nohouga.md, distinct from that file's existing comparative どちらが＋Adj content.
- **STATUS:** Added 2026-09-12 to grammar-index/grammar/comparsion-dochira-nohouga.md (new section added after Examples).

### L2. どのくらい／ぐらい — approximation + かかる idiom ("how long/much does it take")
- **Status:** UNCERTAIN
- **Files:** `Semestr4/GramatykaPodsumowanie.md` (120-124), `L12` (69-109), `Semestr5/L11/GramatykaS5L11.md` (65-81)
- **Why not covered:** `vocabulary/Verbs/kakaru.md` documents only the verb かかる itself, not the どのくらい question pattern.
- **Note-worthiness:** Moderate — 3 files, clean idiom-note candidate.
- **DECISION:** New file (clears the gate — くらい／ぐらい is a confirmed 🔴 gap directly on JLPT-N5-Grammar-List.md line 34, no exception needed). Drafted into Leftovers-1.md rather than folded into kakaru.md, since the master-list gap is about くらい／ぐらい itself, broader than just this one idiom.
- **STATUS:** Drafted 2026-09-12 into JPLessons/Udemy/N5/Grammar/Leftovers-1.md — pending user review, then extract-grammar.

### L3. もっと — comparative degree adverb ("more")
- **Status:** GAP
- **Files:** `Semestr4/L08/GramatykaS4L8.md` (83-84)
- **Why not covered:** `comparisons.md` covers より／のほうが／の中で一番 (comparing specific things); `degree-adverbs-sukoshi-amari-zenzen.md` covers diminishing degree. Neither covers もっと as a standalone intensifier.
- **Note-worthiness:** Weak-moderate — single mention but simple, obvious addition.
- **Udemy check:** `UN5GL15` teaches もっと as vocabulary with 3 examples (もっと左, もっと暑い, もっと勉強しなければなりません) — more thorough than the old-course mention, but still no dedicated structure/contrast-with-より section. Extraction status: **not yet extracted** (appears only in a ごい block with no wikilink, so `extract-grammar` never picked it up). Still open, but good source material exists.

### L4. 同じ／と同じくV — "the same as X"
- **Status:** GAP
- **Files:** `Semestr7/S7L1-L2.md` (63-85), `L02/GramatykaS7L2.md` (3-8)
- **Why not covered:** 同じ only surfaces as a passing "confused with" note inside `issho-together-same.md`, not a dedicated structure/examples section; structurally distinct from どちら/のほうが/より comparison patterns (equality vs. degree); the と同じくV comparative-verb structure isn't covered anywhere.
- **Note-worthiness:** Moderate — 2 files, a clean distinct pattern.
- **Udemy check:** `UN5GL1L2` teaches 同じ＋Noun (structure + 2 examples: 同じ会社, 同じ大学) and has since been extracted — but the material only landed as a one-line "confused with" mention in `issho-together-same.md`, not its own file/section. Still open for a proper dedicated treatment; the と同じくV form isn't taught anywhere in the current course either.

### L5. すごく vs とっても — "very" intensifier register pair
- **Status:** GAP
- **Files:** `Semestr7/L03/GramatykaS7L3.md` (61-65,113-120)
- **Why not covered:** `degree-adverbs-sukoshi-amari-zenzen.md` covers 少し／あまり／全然 (amount/negation-scaled degree), a different function.
- **Note-worthiness:** Weak-moderate — single file, simple register-pair note.

---

## M. Conjunctions & listing

### M1. や...や — non-exhaustive noun listing (context-tied, vs. とか)
- **Status:** GAP
- **Files:** `Semestr7/S7L1-L2.md` (221-283), `L02/GramatykaS7L2.md` (45-57,73-119)
- **Why not covered:** `tokatoka-enumerate-examples.md` fully covers とか but mentions や...や only in passing in its Notes, with no structure/examples/register treatment of its own.
- **Note-worthiness:** Moderate — 2 files, best handled as an addition to the existing とか file (as a contrast/"often confused with" entry) rather than a wholly separate note.
- **DECISION:** New file. Drafted into Leftovers-<N>.md for later extract-grammar processing (see STATUS for exact file).
- **STATUS:** Drafted 2026-09-12 into JPLessons/Udemy/N5/Grammar/Leftovers-1.md — pending user review, then extract-grammar.

---

## O. Miscellaneous register/vocabulary items (small, mostly single-file)

These are all thin (1 file each) and several are explicitly flagged uncertain
as possibly vocab-level rather than grammar. Listed together since they're
unlikely to become their own notes individually — worth a quick judgment call
on each, or bundling into a single small "miscellaneous register notes" page.

### O1. こちら vs この — polite spatial/object pointer (retail register)
- **Status:** UNCERTAIN — **Files:** `Semestr6/L06.md`-`L10.md` (recurring, one source lesson)
- `sonkeigo-polite-people-reference.md` covers こちら only as a way to refer to a *person*, not this object-pointing retail usage.
- **DECISION:** Resolved — the original check looked at the wrong file. `kochira-sochira-achira-dochira-indicate-place-location-and-direction-person.md` already fully covers this exact retail/direction usage (こちらに椅子があります, explicit "business and customer-service settings" register note). While reviewing it, also found a genuine adjacent gap — casual こっち／そっち／あっち／どっち had no coverage anywhere — and added it as a new row + note to that same file.
- **STATUS:** Verified 2026-09-12 (no action needed for O1 itself); casual row added to grammar-index/grammar/kochira-sochira-achira-dochira-indicate-place-location-and-direction-person.md as a bonus fix found along the way.

### O2. ありがとうございました vs ありがとうございます — past vs. present polite thanks
- **Status:** UNCERTAIN — **Files:** `Semestr6/L06.md`-`L10.md` (recurring, one source lesson)
- May be fixed-phrase/vocabulary rather than grammar.
- **DECISION:** Skip.
- **STATUS:** Decided 2026-09-12, no action taken.

### O3. さいきん + casual verb + 時間がありません idiom
- **Status:** UNCERTAIN — **Files:** `Semestr6/L06.md`-`L10.md` (recurring, one source lesson)
- Likely too minor/compositional for its own file.
- **DECISION:** Skip. Not on any JLPT grammar master list, and 最近(さいきん) itself already has a full card in `Vocabulary/JLPT-decks/N4/Nouns.md` — compositional idiom over already-covered pieces (V-dict+N modification, ある/ない existence, and now confirmed さいきん vocab), no new grammar point.
- **STATUS:** Decided 2026-09-12, no action taken.

### O4. に興味／関心があります — "to be interested in"
- **Status:** GAP — **Files:** `Semestr3/L07/GramatykaS3L7.md` (26-27)
- Zero matches anywhere for kanshin/kyoumi/interested. Clean single-pattern note if you want one — this is the strongest candidate in this section (not vocab, a real grammar pattern with a formality contrast built in).

### O5. まえ — "X ago" / "before X" (as opposed to Vdict+前に "before doing")
- **Status:** GAP — **Files:** `Semestr4/GramatykaPodsumowanie.md` (58-59), `L06` (11-12,46-49)
- `vocabulary/Adverbs/mae-ni-before.md` only covers the "before doing X" sense, not "N ago." Worth a short addition to that file rather than a new one.

### O6. よく — frequency adverb ("often")
- **Status:** GAP
- **Files:** `Semestr2/L01/GramatykaS2L1.md` (93-104,108-109), `Semestr3/Podsumowanie semestr 3.md` (14-30, fuller vocabulary set), `L1` (52-61,130-137), `Semestr4/L02/GramatykaS4L2.md` (85,203), `L04` (96), `Semestr6/L01/GramatykaS6L1.md` (109-121, with negation)
- **Why not covered:** `degree-adverbs-sukoshi-amari-zenzen.md` is about degree not frequency; `kai-frequency.md` is about the 回 counter. いつも (the other half of this originally-combined topic) is now covered via `vocabulary/Nouns/itsumo-always-usual.md`, but よく never appears there.
- **Note-worthiness:** Moderate — write a short note/addition just for よく (or add it alongside いつも's existing file as a companion adverb), rather than a whole new note.
- **Udemy check:** `UN5GL15` only teaches よく as bare vocabulary (one example: 彼がよく山にのぼって…) with no structure — not yet extracted (no wikilink). Still open.

---

# Verification against findings.md

Cross-checked all 219 individual finding bullets (220 grep matches minus 1
template/example bullet in the file's own header block) against the topics
above, chapter by chapter. Method: read `findings.md` in full, tallied bullet
counts per chapter with a script (cross-checked against plain `grep -c`),
then walked every chapter's bullets against the topic list one at a time.

This caught **3 real omissions** in the first draft, now fixed:
- `Semestr2/L08/GramatykaS2L8.md` (ます形 past conjugation) was missing from A1.
- `Semestr3/L1/GramatykaS3L1.md` (にがて on the preference scale) was missing from H3.
- `Semestr6/S6L11.md` (combined ます／て／ない／た conjugation mention) was
  only attached to A2 initially — now cross-referenced in A1 and A4 too
  (and formerly A3, since resolved and removed), since its one bullet covers
  all four forms at once.

After these fixes, every bullet in every one of the 90 file-chapters in
`findings.md` was accounted for in at least one topic entry. 17 of those
topics have since been removed as covered by Udemy (see the callout near the
top) — **49 distinct topics remain**, grouped into 14 categories (A–M, O).

---

# Udemy cross-check summary

**Still partial:** L3 (もっと) and the よく half of O6 both have source
material in `UN5GL15` — a lesson not yet run through `extract-grammar`. L4
(同じ) has basic-form material already extracted from `UN5GL1L2`, but only as
a passing note inside `issho-together-same.md`, not a dedicated section. C1
is now only about な／の／ぜ／ぞ (ね itself is covered).

**Confirmed as genuine content gaps even in the current course** (not just
extraction gaps — worth writing fresh, no Udemy shortcut): **A2/A4** (て形/た形
formation — `UN5GL6` announces them but leaves the sections empty), **F1**
(Vて形+ください — heavily *used* in `UN5GL14` but never taught as its own
point), **F3** (ほしがる／を — `UN5GL13`'s extraction mirrors the lesson's
own thinness), **G3** (いただく／くださる／さしあげる — one-line mention
only), **H2** (とくい／にがて — vocab-only mention in `UN4GL4`), **E3**
(要る — bare vocab tag in `UN5GL5`, and not even mentioned in `UN4GL9`'s
otherwise-thorough 必要 lesson), **I2** (て形-as-reason — extraction mirrors
lesson's one-line aside, confirms accurate), **K1** (Vたまま — confirmed
accurate, no change), **H4** (つもりはない — `UN4GL5` only teaches the
already-covered variant).

**Highest-priority note candidates:**
- **Write fresh (confirmed real gaps, no Udemy shortcut):** A2, A4, F1, G1,
  G3, J2, K1, K2, K3, K5, and the よく half of O6.
- **Extract, if `UN5GL15` is run next:** L3 (もっと) and the よく half of O6.

**Best folded into existing files rather than new notes:** F2/F3 (add to
`te-form-hoshii-desu.md`/`hoshii-i-want-n.md`), H4 (add to つもり file), K4
(add to `temoiidesuka-permission.md`), M1 (add to
`tokatoka-enumerate-examples.md`), O5 (add to `mae-ni-before.md`), L4 (add a
proper 同じ section — currently only a passing note in
`issho-together-same.md`).

**Needs a judgment call before deciding format:** H2/H3 (とくい／にがて —
is this really distinct from 上手／下手／好き？), L1 (どれ vs どちら — real
gap or just missing どちら examples?), B9 (real gap, or missing どこか-style
examples for a different particle than what's actually taught?), B10/B11
(likely too narrow to bother with).
