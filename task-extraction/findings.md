# Findings — grammar topics not covered in grammar-index

See task-description.md for method. One `##` chapter per file that produced a
finding. Format per topic:

```
- **<topic name>** (line/section ref): short description of the pattern and
  why it looks distinct from what's in grammar-index/grammar/. Note "uncertain"
  if it's a near-miss/variant rather than a clear gap.
```

Files with zero findings don't need a chapter here — their checkbox in
file-list.md being checked is enough signal that they were reviewed.

---

## JPLessons/Japoński_lekcje/toimport6.md

- **とくい／にがて (skill/weak-point words)** (lines 10-13): うたうのがとくいです／ドイツ語がにがてです — uses the same が-marking structure as 上手/下手 (covered in `be-good-poor-at-jouzu-heta.md`), but with a different vocabulary pair (得意／苦手) that carries a slightly different nuance (forte/weak point vs. skilled/unskilled). That file's "confused_with" doesn't include an とくい/にがて entry. Uncertain — needs review whether this deserves its own file or is just a vocabulary variant of the existing pattern.
- **V「plain」/N + つもりはない (no intention to do X)** (lines 322-335): ..かけるつもりはない／げつようびにいくつもりはない／どうようびにべんきょうするはない — negates intention via はない rather than the V「ない」+つもりです form documented in `vplaintsumoridesu-conviction-of-doing-something-planned-by-speaker.md`. Same meaning, different negation structure — not explicitly covered.

## JPLessons/Japoński_lekcje/Indywidualne/L1.md

- **Assorted counters without a standalone file** (lines 1-65): raw notes list several counters not present under `grammar-index/grammar/` — かげつ (months), かこく (countries), かしょ (places), かん (volumes), きょく (songs/tracks), きれ (slices), くち (bite/sip), くみ (pairs/groups), けん (case/incident and separately buildings), ご (words), しゅるい (kinds/types), しゅう (rounds). Existing counters (だい, かい, さつ, ほん, ひき, etc.) already have their own files, so this system does track counters as grammar points. Note: this source file is very sparse/fragmentary (bare word list, few examples), so value of extracting is limited.

## JPLessons/Japoński_lekcje/Indywidualne/L2.md

- **ね (sentence-final particle — empathy, seeking agreement, softening)** (lines 57-77, restated 202-217): 今日はあついですね／これはおいしいね. No dedicated grammar-index file for ね itself (only `njanai-seeking-agreement.md`, which is the distinct じゃない construction, not plain ね).
- **な (sentence-final particle — male speech, emotional emphasis, rhetorical question)** (lines 166-176, restated 209-217): ii na, ureshii na; "pytanie bez odpowiedzi" (rhetorical question use). Distinct from the prohibitive な covered in `vdictna-dont-do.md` (dict-form + な = "don't do") — this file's な-as-emphasis/emotion/rhetorical-question use is not covered anywhere.

## JPLessons/Japoński_lekcje/Indywidualne/L3.md

- **N（object）を もらう／くれる — receiving/giving of things (not actions)** (lines 75-99): マリアにフィリピンのお土産をもらいました／CDをもらいました. This is the basic "receive/give an object" construction, distinct from the て-form action-favor versions already covered (`vte-agemasu.md`, `vte-kuremasu.md`, `vte-moraimasu.md`, which are all Vて形+あげる/くれる/もらう). No file covers the plain noun-object version.
- **V「dict」+ ことがある (habitual/occasional occurrence)** (lines 20-27): 時々日本料理を作ることがある／1か月、雨が降らないことがあります. Uncertain — this exact contrast is mentioned as a *note* inside `ta-kotogaarimasu-have-you-ever.md` ("登ることがあります means 'I sometimes climb' (habitual)") but that file's main structure/examples are all about the た形 experiential use; the dict-form habitual use has no examples or structure of its own anywhere.

## JPLessons/Japoński_lekcje/Indywidualne/L4.md

- **Vて形 + やる (te-yaru — doing something for a lower-status recipient)** (whole file): 父は犬にえさをやった／私は弟にゲームを買ってやった. `vte-agemasu-kuremasu-moraimasu.md` and its three sub-files cover あげる/くれる/もらう but not やる.

## JPLessons/Japoński_lekcje/Indywidualne/L5.md

- **V-stem + だす (to suddenly start doing, unintentionally)** (lines 177-228): 泣きだした／わらいだした／おどりだした／ふりだした. No grammar-index file for verb-stem+だす (distinct from 始める and from ようになる, both of which are discussed in this same file as contrasts).

## JPLessons/Japoński_lekcje/Indywidualne/L6.md

- **V-stem + つづける (to continue doing something)** (lines 382-392, 462-479): 歌つづける／書きつづけています／ふえつづけています／歩きつづけた. No dedicated file.
- **Vた + まま (leave/remain in an unchanged state)** (lines 208-229, 271-274): すわったまま／テレビがついたままだ／入れたままだった. `v-te-okimasu.md` mentions そのまま only in passing as a companion phrase to ておく; the standalone まま structure (Vたまま, ままだ, ままのN) isn't documented anywhere.
- **Vた + らどう(ですか) — "why don't you / how about"** (lines 232-243, 276, 295-300): 行ったらどうですか／飲んだらどう／N4の試験を受けたらどうですか. No dedicated file.
- **という — "called/named X" (B という A)** (lines 399-411): お花見というイベント. `toiuimidesu-means.md` covers というimidesu ("what does X mean"), a different pattern — plain という for naming/introducing isn't covered.
- **～てもかまわない／かまいません (affirmative "it's fine to do")** (lines 369-376): 着てもかまいません. Uncertain — only the negative なくてもかまいません is documented (in `nakutemoiidesu-nakutemokamaimasen-doesnt-have-to.md`); the affirmative てもかまわない (variant of てもいい) has no file of its own.

## JPLessons/Japoński_lekcje/Indywidualne/L7.md

- **という — "called/named X"** (lines 16-28, 68-74, 89-103): アロンというレストラン／トムヤムクンというタイのスープ. Same gap as L6 above; this file also shows the っていう casual contraction.
- **V-stem + つづける** (lines 60-64): 泣きつづけています／連絡をとりつづけています. Same gap as L6 above.

## JPLessons/Japoński_lekcje/Indywidualne/L8.md

Summary/repetition file — restates topics from L2, L5, L6, L7. Same gaps recur here:
- **ね／な sentence-final particles** (lines 13-30) — same as L2 above.
- **V-stem + だす** (lines 49-61) — same as L5 above.
- **V-stem + つづける** (lines 113-117) — same as L6/L7 above.
- **Vて形 + やる** (lines 158-165) — same as L4 above.
- **Vた + まま** (lines 226-239) — same as L6 above.
- **Vた + らどう(ですか)** (lines 241-246) — same as L6 above.
- **という** (lines 261-269) — same as L6/L7 above.
- **～てもかまわない** (lines 196-200) — same as L6 above, uncertain.

## JPLessons/Japoński_lekcje/Indywidualne/L10.md

Long review/lesson file. Fresh lesson content on ている／てある／のに (lines 460-587) is fully covered — `teiru-show-state.md` (resulting state for punctual verbs), `vte-arimasu-resultant-state.md` (Vて形＋あります／てある), `v-teiru-teinai.md` (ongoing/negative ている), and `temoiidesuka-permission.md` (covers both the statement and question forms of てもいいです) all match. New reviewed topics よ／ながら／だす／やすい・にくい／かた／ことになる／ようになる／かどうか／てあげる・くれる・もらう／ても／ておく／てみる／から are all covered (`yo.md`, `nagara.md`, `vmasuyasuidesu-nikuidesu-easy-difficult-to-do.md`, `kata-a-way-of-doing.md`, `v-dict-koto-ni-narimasu-it-was-decided.md`, `you-ni-narimasu-naku-narimasu.md`, `kadouka-whether-or-not.md`, `vte-agemasu.md`/`vte-kuremasu.md`/`vte-moraimasu.md`, `temo-even-if-even-though.md`, `v-te-okimasu.md`, `temiru-to-try.md`, `kara-because.md`). Sonkeigo お/ご～になる and the irregular special verbs (めしあがる、なさる、いらっしゃる、ごらんになる、おっしゃる) are covered by `o-vmasu-ninarimasu.md` and `tokubetsunadoushi-special-verbs.md`.

Recurring gaps from earlier files in this batch (same patterns, not covered anywhere in grammar-index):
- **ね／な sentence-final particles** (lines 14-31) — same gap as L2/L8 above.
- **V-stem + つづける** (lines 74-78) — same gap as L6/L7/L8 above.
- **Vて形 + やる** (lines 157-164) — same gap as L4/L8 above.
- **～てもかまわない** (lines 197-201) — same gap as L6/L8 above, uncertain.
- **Vた + まま** (lines 216-229) — same gap as L6/L8 above.
- **Vた + らどう(ですか)** (lines 231-236) — same gap as L6/L8 above.
- **という** (lines 251-259) — same gap as L6/L7/L8 above.

New finding:
- **Plain-object いただく／くださる／さしあげる (honorific receive/give of a thing, not a favor)** (lines 352-374, restated ~649-669): 先生から本をいただきました／先生が辞書をくださいました／これをあなたに差し上げます. Only the Vて形＋いただく／くださる favor construction is covered (`te-form-itadaku-kudasaru-favor-received.md`); there is no file for the plain noun-object honorific exchange (receiving/giving a physical thing, not a favor-action). This is the honorific-register counterpart of the plain-object あげる／くれる／もらう gap already flagged for L3.md.

## JPLessons/Japoński_lekcje/Indywidualne/L11.md

Same review boilerplate as L10 repeats here, plus new lesson content on ば／なら conditionals (lines 358-862), which is fully covered — `joukenkei-ba-conditional-form.md`, `nara-if.md`, and `v-ba-iidesuka.md` (the どうすればいいですか question pattern) all match.

Recurring gaps:
- **ね／な sentence-final particles** (lines 14-31) — same as above.
- **V-stem + つづける** (lines 74-78) — same as above.
- **Vて形 + やる** (lines 157-164) — same as above.
- **～てもかまわない** (lines 197-201) — same as above, uncertain.
- **Vた + まま** (lines 216-229) — same as above.
- **Vた + らどう(ですか)** (lines 231-236) — same as above.
- **という** (lines 251-259) — same as above.
- **Plain-object いただく／くださる／さしあげる** (lines 305-327, restated ~752-764) — same gap as L10 above.

## JPLessons/Japoński_lekcje/Indywidualne/L12.md

Pure review repeat of L10/L11 boilerplate, no new lesson content (Notatki section empty). Same gaps recur:
- **ね／な sentence-final particles** (lines 13-30)
- **V-stem + つづける** (lines 74-78)
- **Vて形 + やる** (lines 157-164)
- **～てもかまわない** (lines 197-201), uncertain
- **Vた + まま** (lines 216-229)
- **Vた + らどう(ですか)** (lines 231-236)
- **という** (lines 251-259)
- **Plain-object いただく／くださる／さしあげる** (lines 305-327)

## JPLessons/Japoński_lekcje/Indywidualne/L13.md

Same review boilerplate, plus new lesson content on とか。。。とか (enumeration) and し (listing reasons), both fully covered — `tokatoka-enumerate-examples.md` and `shishi-conjunction.md`.

Recurring gaps:
- **ね／な sentence-final particles** (lines 13-30)
- **V-stem + つづける** (lines 74-78)
- **Vて形 + やる** (lines 157-164)
- **～てもかまわない** (lines 197-201), uncertain
- **Vた + まま** (lines 216-229)
- **Vた + らどう(ですか)** (lines 231-236)
- **という** (lines 251-259)
- **Plain-object いただく／くださる／さしあげる** (lines 305-327)

## JPLessons/Japoński_lekcje/Indywidualne/L14.md

Same review boilerplate, plus new lesson content on と／たら conditionals and た＋ほうがいい, all fully covered — `v-dict-to-if.md`, `past-tense-tara-if.md`, `v-ta-nai-hou-ga-ii-desu.md`.

Recurring gaps:
- **ね／な sentence-final particles** (lines 13-30)
- **V-stem + つづける** (lines 74-78)
- **Vて形 + やる** (lines 157-164)
- **～てもかまわない** (lines 197-201), uncertain
- **Vた + まま** (lines 216-229)
- **Vた + らどう(ですか)** (lines 231-236)
- **という** (lines 251-259)
- **Plain-object いただく／くださる／さしあげる** (lines 305-327) — also recurs as plain-object もらいました (line 525: 弟はマリアのお母さんにお土産をもらいました), same plain-object-exchange gap already flagged for L3.md.

## JPLessons/Japoński_lekcje/Indywidualne/L15.md

Same review boilerplate, plus new lesson content on Vように (purpose), はず／はずがない, and かもしれない, all fully covered — `youni-in-order-to.md`, `hazudesu-should-do-ought-logically.md` (covers はずがない in its section 2), `kamoshiremasen-kamoshirenai-may-might.md`.

Recurring gaps:
- **ね／な sentence-final particles** (lines 13-30)
- **V-stem + つづける** (lines 74-78)
- **Vて形 + やる** (lines 157-164)
- **～てもかまわない** (lines 197-201), uncertain
- **Vた + まま** (lines 216-229)
- **Vた + らどう(ですか)** (lines 231-236)
- **という** (lines 251-259)
- **Plain-object いただく／くださる／さしあげる** (lines 305-327)

## JPLessons/Japoński_lekcje/Indywidualne/L16.md

Pure review repeat, no new lesson content. Same gaps recur:
- **ね／な sentence-final particles** (lines 12-29)
- **V-stem + つづける** (lines 73-77)
- **Vて形 + やる** (lines 156-163)
- **～てもかまわない** (lines 196-200), uncertain
- **Vた + まま** (lines 215-228)
- **Vた + らどう(ですか)** (lines 230-235)
- **という** (lines 250-258)
- **Plain-object いただく／くださる／さしあげる** (lines 304-326)

## JPLessons/Japoński_lekcje/Semest1/L13/GramatykaS1L13.md

- **Telling clock time — ～じ (hour) ＋ はん (half past)** (lines 5-25, 31-33): いちじ／にじ／…／じゅうにじ, いちじはん, ごぜん／ご、いま、なんじですか。No grammar-index file covers the じ hour-counter or はん (half-past) — `times.md` and `kai-frequency.md` under `counter-sufixes.md` are both about 回 (frequency "times"), a different word entirely, not clock time.
- **ます形 (polite non-past) verb conjugation by group** (lines 60-72): dictionary-form → ます-form conversion rules by ending (かう→かいます、いる→います、する→します、くる→きます、う-verbs ending in つ→ちます, etc.). Adjective conjugation has dedicated files (`i-adjective-conjugation.md`, `na-adjective-conjugation.md`) and て-form has its own (`te-form.md`), but there's no equivalent file for basic present-tense ます-form verb conjugation by group (godan/ichidan/irregular).
- **さい (age counter)** (line 54): "Ile masz lat – anata wa nan sai desuka." No file for 歳/さい, same category of gap as the "assorted counters" finding already flagged for `Indywidualne/L1.md`.

## JPLessons/Japoński_lekcje/Semest1/L14/GramatykaS1L14.md

- **へ — direction/goal particle ("to")** (lines 3-4): watashi wa ie e ikimasu／kouen e ikimasu. No dedicated file for へ as a direction particle; `particles.md`'s only sub-topic is よ.
- **で — instrument/means particle ("by")** (lines 8-19): kuruma de／dzitensha de／toho de (by car/bike/on foot). `subject-de-v-who-performs-action.md` explicitly notes this is a *different* use of で from the one it documents (person/group performing an action) and says so in its own Notes section — confirming the instrument/means で has no file of its own.
- **で — location-of-action particle ("at/in")** (lines 31-34): lunch o ie de tabemasu／anime o ie de mimasu (eating/watching at home). Same gap category as above — no file covers で marking the place an action happens.

## JPLessons/Japoński_lekcje/Semestr2/L01/GramatykaS2L1.md

- **へ — direction/goal particle ("to")** (lines 67-70): Tokyo e, Watashi wa Google e ikimashita. Same gap as `GramatykaS1L14.md` above.
- **よく／いつも — frequency adverbs ("often"/"always")** (lines 93-104, 108-109): messeeji o yoku kakimasu／ongaku o itsumo kikimasu. No file covers these; `degree-adverbs-sukoshi-amari-zenzen.md` is about 少し／あまり／全然 (degree, not frequency) and `kai-frequency.md` is about the 回 counter, not adverbs like よく／いつも.

## JPLessons/Japoński_lekcje/Semestr2/L05/GramatykaS2L5.md

- **ある／いる — existence and possession ("there is/are", "to have")** (lines 45-56, 66-93): neko ga imasu／koohii ga arimasuka／watashi wa keitai ga arimasu／anata wa koibito ga imasuka. This is a foundational N5 pattern (animate いる vs inanimate ある, question form ～がありますか／いますか, possession via 「Xは Yが あります／います」 doubling as "X has Y") with no standalone file anywhere in `grammar-index/grammar/` — searched for arimasu/imasu/existence/aru/iru files and found none; the only near-matches (`gozaimasu-polite-arimasu-desu.md`, `ta-kotogaarimasu-have-you-ever.md`) cover unrelated derived patterns (the super-polite でございます tier, and the たことがあります experiential-past construction), not the base ある／いる distinction itself.

## JPLessons/Japoński_lekcje/Semestr2/L06/GramatykaS2L6.md

No findings — reviewed, all topics covered (い-adjective past tense, ません／ませんでした negation).

## JPLessons/Japoński_lekcje/Semestr2/L07/GramatykaS2L7.md

- **ある／いる — existence** (lines 14-22, 47-59): mizu ga arimasuka／oshiro ga arimasu／eki wa doko ni arimasuka／isha wa doko ni imasuka. Same gap as `Semestr2/L05/GramatykaS2L5.md` above.
- **Positional nouns (上／下／右／左／前／後ろ) + の...に あります／います — relative location** (lines 61-94, 118-129): yuka no ue, pantsu wa rampu no ue ni arimasu, kutsushita wa beddo no shita ni arimasu, Dorota san wa Mariola san no migi ni imasu; summary formula "N1はN2のkierunekにあります". No spatial/positional-noun file found under `grammar-index/grammar/` — distinct N5 pattern from the plain existence construction above, though closely related.

## JPLessons/Japoński_lekcje/Semestr2/L08/GramatykaS2L8.md

- **Dictionary-form → ます形 past conjugation by verb group** (lines 30-49): hanasu→hanashimashita, kau→kaimashita, yomu→yomimashita, kuru→kimashita, suru→shimashita, etc. Same gap as `Semest1/L13/GramatykaS1L13.md` above (ます形 conjugation by group) — this is the past-tense half of that gap. Copula past/negative でした／じゃありませんでした in this file IS covered by `teineikei-vs-futsuukei-polite-form-vs-plain-form.md`, not a finding.

## JPLessons/Japoński_lekcje/Semestr2/L09/GramatykaS2L9.md

- **ある／いる — existence** (line 18-19): arimasu (nieżywy) / imasu (żywy). Same gap as `Semestr2/L05.md` above.
- **Positional nouns + に あります／います** (lines 2-16, 42-54): dorota san wa mariola san no migi desu. Same gap as `Semestr2/L07.md` above.
- **で — instrument/means particle ("by")** (lines 39-40): genkin de - gotówką (pay by cash). Same gap as `Semest1/L14/GramatykaS1L14.md` above.
- **に／へ — direction/goal particle** (line 56): "do - ni/e". Same gap as `Semest1/L14.md`/`Semestr2/L01.md` above; note に also used interchangeably with へ for direction here.

## JPLessons/Japoński_lekcje/Semestr2/L10/GramatykaS2L10.md

- **ある／いる + positional nouns** (lines 2-19): recap of the same formula. Same gaps as `Semestr2/L07.md`/`L09.md` above.
- **て形 formation rules by verb-ending group** (lines 44-90): う／つ／る→って, む／ぶ／ぬ→んで, く→いて, ぐ→いで, す→して, くる→きて, する→して, いく→いって, with worked examples. `te-form.md` and its only sub-topic `te-form-sequencing-order.md` both assume the て形 is already known and document only the "chain events" *use*; neither contains the actual dictionary→て-form conversion rules by verb group. Distinct gap from the "ます形 conjugation by group" gap above — same category (conjugation mechanics), different target form.
- **Vて形 + ください — basic affirmative request ("please do X")** (lines 94-104): tsukutte kudasai, motte kudasai, matte kudasai, katte kudasai, totte kudasai. `wokudasai-please-give-me.md` covers N＋を＋ください (object request, not verb request); `vnaidekudasai-please-dont-do-it.md` covers the negative Vないでください only; `o-go-v-masukudasai-respectful-request-form.md` covers only the sonkeigo お／ご＋ますkudasai variant. No file covers the plain affirmative Vて形＋ください.

## JPLessons/Japoński_lekcje/Semestr2/L11/GramatykaS2L11.md

- **て形 formation rules by verb-ending group** (lines 1-10, 27-127): the file's entire body is built around this. Same gap as `Semestr2/L10.md` above.
- **Vて形 + ください** (lines 22-24, 35, 43, 51-53, 59, 62, 79-84, 97-103, 109, 113, 127): koko de sutte kudasai, matte kudasai. Same gap as `Semestr2/L10.md` above. (Checked `itadakemasenka-polite-request.md`/`kudasaimasenka-polite-request.md` — those are more-polite くださいませんか／いただけませんか variants, not the plain form.)

## JPLessons/Japoński_lekcje/Semestr2/L12/GramatykaS2L12.md

- **て形 formation rules by verb-ending group** (lines 1-9, 15-27, 45): Same gap as `Semestr2/L10.md`/`L11.md` above. (てもいいですか permission content in this file IS covered by `temoiidesuka-permission.md` — not a finding.)

## JPLessons/Japoński_lekcje/Semestr2/L13/GramatykaS2L13.md

- **て形 formation rules by verb-ending group** (lines 1-9, 71-81): Same gap as `Semestr2/L10.md`-`L12.md` above.
- **ある／いる + directional location** (lines 48-51, 67-69): arimasu/imasu (dead/alive) with 「Xは Yの [kierunek] に あります／います」. Same gap as `Semestr2/L05.md`/`L07.md`/`L09.md` above. (い-adj/な-adj past-negative conjugation in this file IS covered by `i-adjective-conjugation.md`/`na-adjective-conjugation.md` — not a finding.)

## JPLessons/Japoński_lekcje/Semestr3/Podsumowanie semestr 3.md

- **て形 formation rules by verb-ending group** (lines 35-49, 71-79): Same gap as `Semestr2/L10.md`-`L13.md` above.
- **Frequency adverbs (毎日／よく／しょっちゅう／時々／たまに／あまりません／ぜんぜん)** (lines 14-30): fuller vocabulary set for the same gap already flagged for `Semestr2/L01/GramatykaS2L1.md` (よく／いつも frequency adverbs).
- **の — sentence-final particle (softer/feminine equivalent of よ)** (lines 146-151): "の = よ, ale używane przez kobietę" — pasta o taberuno. `yo.md`'s own Notes acknowledge ね has no standalone file yet, but don't address の; `ndesu-nodesu-explaining-reason.md` covers the explanatory んです nominalizer, a different function. Extends the already-known ね／な sentence-final-particle gap (first flagged in `Indywidualne/L2.md`) to include の.
- **な — sentence-final particle (exclamation, "ale...")** (lines 154-155): おいしいな. Same gap as `Indywidualne/L2.md`/`L8.md` above (ね／な sentence-final particles).
- **ない形 (plain negative) conjugation by verb-ending group** (lines 157-186): full table (よむ→よまない, かく→かかない, する→しない, くる→こない, etc.). `teineikei-vs-futsuukei-polite-form-vs-plain-form.md` mentions ない／なかった only generically as one line of the plain-form contrast, without by-ending conjugation rules. Same category of gap as the ます形/て形-by-group conjugation gaps above — the ない形 mechanics have no file either.
- **Vて + うれしいです (glad/happy that ~)** (lines 58-61): あなたにあってうれしいです. No file matches (searched grammar-index/grammar for "ureshii" — no hits); `te-form-hoshii-desu.md` covers the different Vて＋ほしいです ("want someone to") pattern.
- **いる／います as "to need" (要る, distinct from 必要)** (lines 91-96, 207-208): 私はきっぷがいります／そうじがいります. `hitsuyou-noun-use-ga-aru-nai.md` covers V「dict」+必要がある／がない (a different word, 必要, and different structure) — no file covers the verb 要る／いります itself.
- **Apology-expression register hierarchy after て形** (lines 189-196): おくれてすみません／おくれてごめんなさい／おくれてもうしわけありません／…ございません. No file documents this politeness-tiered apology construction (searched for sumimasen/moushiwake/gomennasai — no match). Related to, but distinct from, the て形-as-reason/cause gap flagged for `Semestr3/L3/GramatykaS3L3.md` below — this finding is about the apology-word politeness ladder itself, not the て形-causal grammar.
- **とくい／にがて skill good-at/poor-at (Xがとくいです for nouns, Xのがとくいです for verbs)** (lines 107-121): recurring instance of the uncertain gap first flagged in `toimport6.md`; this file adds the が vs のが structural distinction. Uncertain — needs review.
- **にがて on the すき preference scale (だいすき＞すき＞にがて＞きらい)** (lines 1-13, 123-129): here にがて is used on the like/dislike scale, not the skill scale. `suki-kirai-like-dislike.md` documents 好き／嫌い／大好き／大嫌い precisely but has no にがて entry. Possible near-miss/vocabulary variant rather than a distinct pattern. Uncertain — needs review.

## JPLessons/Japoński_lekcje/Semestr3/L1/GramatykaS3L1.md

- **ます形 conjugation by verb-ending group** (lines 63-93): nomu→nomimasu, hanasu→hanashimasu, taberu/miru/suru→ます. Same gap as `Semest1/L13/GramatykaS1L13.md` above.
- **Noun + する verb formation (verbal nouns)** (lines 95-102): ryouri suru／sentaku suru／souji suru. `narimasu-vs-shimasu-change-of-state.md` covers a different pattern (なります vs します marking who caused a change of state), not the general word-formation rule that a noun becomes a verb by attaching する. No file documents it.
- **が すき／にがて preference scale** (lines 45-50): gasuki／nigate／daisuki／kirai. Same uncertain gap as `Semestr3/Podsumowanie semestr 3.md` above.
- **Frequency adverbs** (lines 52-61, 130-137): mainichi／yoku／shocchuu／tokidoki／tamani／amari masen／zenzen. Same gap as `Semestr2/L01.md` above.

## JPLessons/Japoński_lekcje/Semestr3/L2/GramatykaS3L2.md

No findings — reviewed, all topics covered (て形-sequencing of actions, matched by `te-form-sequencing-order.md`).

## JPLessons/Japoński_lekcje/Semestr3/L3/GramatykaS3L3.md

- **て形 as reason/cause before an apology or emotion expression** (lines 1-53, 114-130): おくれてすみません／おくれてごめんなさい (apologizing because of X); あなたにあってうれしいです／プレゼントをもらってうれしいです (glad because of X). This is the causal/reason use of て形 (X-て、Y = "because X, Y"), distinct from the sequencing use. `te-form-sequencing-order.md` explicitly flags this as a *different* function in its own Notes section (one bare example, no structure/examples of its own) — confirming no file documents this construction on its own terms. (The すみません／ごめんなさい／もうしわけありません politeness-ladder vocabulary itself is separately covered in `grammar/vocabulary/Nouns/im-sorry.md`, so only the て形-as-reason grammar is the gap, not the word list. てもいいですか permission content in this file IS covered by `temoiidesuka-permission.md` — not a finding.)

## JPLessons/Japoński_lekcje/Semestr3/L4/GramatykaS3L4.md

No findings — reviewed, all topics covered (てはいけません prohibition matches `tehaikemasen-must-not.md`/`v-tewa-ikemasen-forbidden.md`; てもいいです matches `temoiidesuka-permission.md`).

## JPLessons/Japoński_lekcje/Semestr3/L5/GramatykaS3L5.md

- **に — location-of-existence/residence particle (with すむ／いる／ある-type stative verbs)** (lines 102-106, 117-118): Wieliczka **ni** sundeimasu; hitori de sundeimasu; Łódź **ni** sundeimasu ("mieszkam w Łodzi"). No file on に as a stative-location particle exists (`particles.md`'s only sub-topic is よ). Distinct particle gap from the already-flagged で (instrument/means, location-of-action) and へ (direction) gaps — に marking the location where something exists/resides (vs. where an action happens) is undocumented. (ている present-continuous/resultant-state content in this file IS covered by `teiru.md`/`teiru-show-state.md`/`v-teiru-teinai.md` — not a finding.)

## JPLessons/Japoński_lekcje/Semestr3/L6/GramatykaS3L6.md

- **に vs で locative-particle distinction (recurrence)** (lines 170-171): "de - w / ni - do" (reversed/garbled in the student's own notes, but the underlying に-stative-location gap is the same as `Semestr3/L5/GramatykaS3L5.md` above). から (reason) content in this file IS covered by `kara-because.md` — not a finding.

## JPLessons/Japoński_lekcje/Semestr3/L07/GramatykaS3L7.md

- **に興味／関心があります — "to be interested in"** (lines 26-27): x に興味があります (casual, hobby-interest) vs. x に関心があります (formal, e.g. politics). No file in `grammar-index/grammar/` covers this (searched for kanshin/kyoumi/interested — no matches).
- **N/Adj + が + いります／要る (to need)** (lines 38-58): とも達がいります／じかんがいります／きっぷがいります, explicitly contrasted with いる=いますas "to be present". Same gap as `Semestr3/Podsumowanie semestr 3.md` above (要る, distinct from 必要).
- **とくい／にがて skill good-at/poor-at, の-marking for verbs vs. plain が for nouns** (lines 78-103, 158-176): 私は歌うのがとくいです（動詞）vs 私は日本語がとくいです（名詞）. Same uncertain gap first flagged in `toimport6.md`. Uncertain — needs review.

## JPLessons/Japoński_lekcje/Semestr3/L08/GramatykaS3L8.md

- **N/Adj + が + いります (need)** (line 23, Powtórzenie recap): same gap as `Semestr3/L07.md` above.
- **とくい／にがて** (lines 25-39, Powtórzenie recap): same gap as `Semestr3/L07.md` above. Uncertain — needs review.

(New lesson content in this file — い/な-adjective+なる change-of-state, casual/plain-present speech — IS covered by `narimasu-vs-shimasu-change-of-state.md`/`teineikei-vs-futsuukei-polite-form-vs-plain-form.md`, not a finding.)

## JPLessons/Japoński_lekcje/Semestr3/L09/GramatykaS3L9.md

- **ね／な／の／ぜ／ぞ sentence-final particles (register/gender/emphasis variants)** (lines 109-195): だ as blunt/rude standalone assertion; よ as "you know" assertion incl. masculine ぜ／ぞ variants; の as feminine/softer よ equivalent; な after adjectives for exclamation. Same gap first flagged in `Indywidualne/L2.md`, here extending it to explicitly include the ぜ／ぞ masculine-register variants — `yo.md`'s own Notes acknowledge ね has no file, and don't address の/ぜ/ぞ either.
- **ない形 conjugation by verb-ending group** (lines 197-265): full worked table plus ないで as bare prohibition. Same gap as `Semestr3/Podsumowanie semestr 3.md` above.
- **N/Adj + が + いります (need)** (line 23, Powtórzenie recap): same gap as `Semestr3/L07.md` above.
- **とくい／にがて** (lines 25-39, Powtórzenie recap): same gap as `Semestr3/L07.md` above. Uncertain — needs review.
- **て形／で形 formation rules by verb-ending group** (lines 1-15, Powtórzenie recap): same gap as `Semestr2/L10/GramatykaS2L10.md` above.

## JPLessons/Japoński_lekcje/Semestr3/L10/GramatykaS3L10.md

- **た形 (plain/casual past) conjugation by verb-ending group** (lines 70-81, 83-111): "skrócony czas przeszły" — matta／katta／mita／tabeta／nonda／shinda, presented as the て形→た形 parallel. No file documents た形 conjugation mechanics — `te-form.md`/`te-form-sequencing-order.md` assume て形 is already known and cover only its sequencing use; `tokoro-desu-ta-form.md`/`ta-bakari.md`/`ta-kotogaarimasu-have-you-ever.md` all assume た形 as a given and build compound patterns on top of it. Same category as the already-flagged ます形／て形／ない形-by-group conjugation gaps, extended here to a fourth target form (plain past).
- **ある／いる existence, incl. negative ない／いない** (lines 146-177): 「じゃない」／koibito ga iru/inai／yotei ga aru/nai. Same gap as `Semestr2/L05/GramatykaS2L5.md` above.
- **ない形 conjugation by verb-ending group** (lines 83-111): further worked examples. Same gap as `Semestr3/L09.md` above.
- **N/Adj + が + いります (need)** (line 23, Powtórzenie recap): same gap as `Semestr3/L07.md` above.
- **とくい／にがて** (lines 25-39, Powtórzenie recap): same gap as `Semestr3/L07.md` above. Uncertain — needs review.
- **て形／で形 formation rules by verb-ending group** (lines 1-15, Powtórzenie recap): same gap as `Semestr2/L10.md` above.

## JPLessons/Japoński_lekcje/Semestr4/Egzamin.md

No findings — file contains only embedded image attachments and one vocabulary line; no extractable text content to analyze.

## JPLessons/Japoński_lekcje/Semestr4/GramatykaPodsumowanie.md

- **ました (single past fact) vs. ～ていました (habitual action that has since stopped)** (lines 1-22): べんきょうしました "studied once/as a fact" vs. べんきょうしていました "used to study regularly (not anymore)"; same contrast for あう. `teiru.md`/`teiru-show-state.md` cover ongoing action/habit and resultant state, but not this specific past-tense "used to, but stopped" aspectual nuance vs. plain past; `teiru-teru-teita-teta-casual-contraction.md` glosses ていた as "was doing/used to do" only in passing, no dedicated structure/examples. Uncertain — needs review.
- **と vs に with 会う-type verbs (companionship "with" vs. target of meeting/going out)** (lines 24-28): ともだちと (staying in/online together) vs. ともだちに (going out to meet). No file covers this と/に distinction (`particles.md` only has よ).
- **ない形 conjugation by verb-ending group, incl. irregulars** (lines 30-40): same gap as `Semestr3/Podsumowanie semestr 3.md` above.
- **まえ — "N ago" (temporal, e.g. 2時間まえ)** (lines 58-59): checked `vocabulary/Adverbs/mae-ni-before.md` — it only documents Vdict+前に／Nの前に ("before doing X"), not the standalone "N+まえ = N ago" reading used here. No file covers this reading.
- **どれ vs どちら — interrogative "which" (3+ options vs. 2 options)** (lines 83-84, 112): plain selection-question words. `comparsion-dochira-nohouga.md` only documents どちらが＋Adj comparative (N1とN2とどちらが好きですか), not the general "which one of these" selection usage; no file for どれ exists at all. Uncertain — needs review (near-miss with the dochira-comparison file).
- **どのくらい／ぐらい — asking "about how much/how long"** (lines 120-124): どのくらいかかりますか. `vocabulary/Verbs/kakaru.md` documents only the verb かかる itself, not the どのくらい question-word pattern. Uncertain — needs review.
- **な-adjective + なの ("the [na-adj] one")** (line 99): `adjno-substitute-of-noun.md`/`no-meishika.md` cover い-adjective+の and general nominalization but not specifically な-adj+なの. Uncertain — needs review.
- **へ／に direction particle** (lines 107-118): same gap as `Semest1/L14/GramatykaS1L14.md` above.

## JPLessons/Japoński_lekcje/Semestr4/L01/GramatykaS4L1.md

- **て形 formation rules by verb-ending group** (lines 15-40): same gap as `Semestr2/L10/GramatykaS2L10.md` above.
- **と vs に with 会う-type verbs** (lines 26-28, 68-72, 78-81): same gap as `Semestr4/GramatykaPodsumowanie.md` above.
- **ました vs ～ていました past-tense aspect contrast** (lines 3-22, 59-64, 93-103): same gap as `Semestr4/GramatykaPodsumowanie.md` above. Uncertain — needs review.

## JPLessons/Japoński_lekcje/Semestr4/L01/Untitled.md

No findings — confirmed via Read that the file is completely empty (0 bytes). This resolves the ⚠ flag from task-description.md: it is not a lesson/grammar file, just an empty note.

## JPLessons/Japoński_lekcje/Semestr4/L02/GramatykaS4L2.md

- **Vて形＋ください — basic affirmative request** (line 57): same gap as `Semestr2/L10.md`/`L11.md` above.
- **いつも — frequency adverb** (lines 85, 203): same gap as `Semestr2/L01/GramatykaS2L1.md` above.

## JPLessons/Japoński_lekcje/Semestr4/L03/GramatykaS4L3.md

- **ない形 conjugation by verb-ending group** (lines 30-52, 61-63): same gap as `Semestr3/Podsumowanie semestr 3.md` above.
- **ね／な sentence-final particles** (lines 71-78): same gap as `Indywidualne/L2.md` above.

## JPLessons/Japoński_lekcje/Semestr4/L04/GramatykaS4L4.md

- **ない形 conjugation by verb-ending group** (lines 9-61): same gap as `Semestr3/Podsumowanie semestr 3.md` above.
- **に — stative-location particle** (lines 106-112): same gap as `Semestr3/L5/GramatykaS3L5.md` above.
- **いつも — frequency adverb** (line 96): same gap as `Semestr2/L01/GramatykaS2L1.md` above.

## JPLessons/Japoński_lekcje/Semestr4/L05/GramatykaS4L5.md

- **ない形 conjugation by verb-ending group** (lines 9-29): same gap as `Semestr3/Podsumowanie semestr 3.md` above.
- **について — "regarding/about X"** (lines 61-69): あなたについてはなします／ぽーらんどについてはなします／じぶんについてはなします. Searched `grammar-index/grammar/` for "tsuite"/について — no matches anywhere; `particles.md` doesn't cover it either. No file documents this topic-marking construction.

(Frequency practice with 回 counter, lines 89-153, IS covered by `kai-frequency.md` — not a finding.)

## JPLessons/Japoński_lekcje/Semestr4/L06/GramatykaS4L6.md

- **まえ — "X ago" / "before X"** (lines 11-12, 46-49): 2時間まえ／5じかんまえ. Same gap as `Semestr4/GramatykaPodsumowanie.md` above.
- **じかん — hour-duration counter ("for X hours")** (lines 6-10, 37-42): いちじかん／にじかん／よじかん. Same category as the already-flagged assorted-counters gap (`Indywidualne/L1.md`) and さい／じ counter gaps (`Semest1/L13/GramatykaS1L13.md`) — `counter-sufixes.md`/`counters.md`/`times.md` don't cover 時間 as a duration counter.
- **た形 conjugation by verb-ending group** (lines 151-222): full drill table (nomu→nonda, matsu→matta, kau→katta, suru→shita, iku→itta, etc.). Same gap as `Semestr3/L10/GramatykaS3L10.md` above.

(ある／いる existence, Vないでください／dict+な prohibition in this file ARE covered by existing files — not findings.)

## JPLessons/Japoński_lekcje/Semestr4/L07/GramatykaS4L7.md

No findings — reviewed, all topics covered (adjective-to-adverb conversion, が vs は, adjective+くなります／になります change-of-state).

## JPLessons/Japoński_lekcje/Semestr4/L08/GramatykaS4L8.md

- **な-adjective + なの ("the [na-adj] one")** (lines 86-104, 128, 133-146): しずかなの／きれいなの／はでなの／ばかなの. `adjno-substitute-of-noun.md` documents ADJ+の only with い-adjective examples in its Structure section, not the な-adjective+なの surface form. Uncertain — needs review.
- **もっと — comparative degree adverb ("more")** (lines 83-84): もっとはやい. `comparisons.md` only covers より／のほうが／の中で一番 (comparing specific things); `degree-adverbs-sukoshi-amari-zenzen.md` covers 少し／あまり／全然 (diminishing degree). Neither covers もっと as a standalone "more/-er" intensifier.

(ある／いる existence, ADJ+の for い-adjectives, 何か／だれか indefinite pronouns, が vs は — all covered by existing files, not findings.)

## JPLessons/Japoński_lekcje/Semestr4/L09/GramatykaS4L9.md

No findings — file is empty.

## JPLessons/Japoński_lekcje/Semestr4/L11/GramatykaS4L10.md

No new findings — reviewed. て形-sequencing, N+の時, and the plain-past/negative conjugation drill and さい age counter are all recurrences of already-known gaps, not new ones.

## JPLessons/Japoński_lekcje/Semestr4/L12/GramatykaS4L12.md

- **間（かん）as a duration-forming counter suffix** (lines 6-29): 一週間(いっしゅうかん)／三年間(さんねんかん)／一年間半. `aida-between-during-among.md` documents 間 read あいだ, used as a standalone noun with に／で／から〜まで — a structurally different pattern from this かん-reading duration-counter suffix. Same category as the already-flagged assorted-counters gap.
- **どれ vs どちら — "which one" selection question** (lines 45-64): distinguished by count (どれ = 3+, どちら = 2). Same gap as `Semestr4/GramatykaPodsumowanie.md` above. Uncertain — needs review.
- **ぐらい／くらい — approximation particle + どのくらい(かかりますか) idiom** (lines 69-109): どのくらいかかりますか／十五時間ぐらい. Same gap as `Semestr4/GramatykaPodsumowanie.md` above (どのくらい／ぐらい). Uncertain — needs review.
- **で — instrument/means particle** (lines 100-109): same gap as `Semest1/L14/GramatykaS1L14.md` above.

(Vplain+N relative clause and まで content in this file ARE covered by existing files — not findings.)

## JPLessons/Japoński_lekcje/Semestr4/L13/GramatykaS4L13.md

- **Plain-form + と思う ("I think that ~")** (line 67): ぐうたらだと思う. `v-plain-to-itteimashita.md` documents the parallel-but-distinct structure plain+と言っていました ("X said that ~", hearsay/relay), a different function from personal opinion. No file matches plain+と思う (only the polite ます形+と思います is covered, via `vocabulary/Verbs/i-think-toimasu.md`).
- **ない形 conjugation by verb-ending group** (lines 7-14): same gap as `Semestr3/Podsumowanie semestr 3.md` above.
- **て形 conjugation by verb-ending group** (lines 15-23): same gap as `Semestr2/L10/GramatykaS2L10.md` above.

## JPLessons/Japoński_lekcje/Semestr5/toimport1.md

- **V「plain」/N + つもりはない (no intention to do X)** (lines 1767-1786): same gap as `toimport6.md` above.
- **Vて形 + ください — basic affirmative request** (lines 1991, 2026): same gap as `Semestr2/L10.md`/`L11.md` above.

(Remainder of this large card-dump file matches existing grammar-index files — と言っていました, より／のほうが, の中で一番, 上手／下手, indirect questions, やすい／にくい, そう appearance-inference — not findings.)

## JPLessons/Japoński_lekcje/Semestr5/L01/GramatykaS5L1.md

- **ない形 (plain negative) conjugation by verb-ending group** (lines 18-36, 51-73): same gap as `Semestr3/Podsumowanie semestr 3.md` above.

(い/な-adjective conjugation in this file IS covered — not a finding.)

## JPLessons/Japoński_lekcje/Semestr5/L02/GramatykaS5L2.md

- **ない形 conjugation by verb-ending group, present + past なかった** (lines 71-144, 190-247): same gap as `Semestr5/L01.md` above.

## JPLessons/Japoński_lekcje/Semestr5/L3/GramatykaS5L3.md

- **について — "about/regarding"** (lines 112-113, 155): 東京についてどうもいますか. Same gap as `Semestr4/L05/GramatykaS4L5.md` above.
- **ない形 conjugation by verb-ending group** (lines 2-20): same gap as `Semestr5/L01.md` above.

(と思います and より／のほうが in this file ARE covered — not findings.)

## JPLessons/Japoński_lekcje/Semestr5/L4/GramatykaS5L4.md

No findings — reviewed, all topics covered (と思います, といっていました／と言っていました). ない形 boilerplate recap is the same recurring known gap, not re-detailed since no new content.

## JPLessons/Japoński_lekcje/Semestr5/L5/GramatykaS5L5.md

- **とくい (skill/good-at-for-oneself, alongside 上手／下手)** (lines 61-71): same uncertain gap as `toimport6.md`/`Semestr3/L07.md` above. Uncertain — needs review.

(V-dict+のが+すきです／上手／下手 and ない形 boilerplate recap in this file ARE covered/already-known — not new findings.)

## JPLessons/Japoński_lekcje/Semestr5/L6/GramatykaS5L6.md

No findings — reviewed, all topics covered (と思います, といっていました, の-nominalizer+すきです, つもりです affirmative, い-adjective くて-chaining).

## JPLessons/Japoński_lekcje/Semestr5/L7/GramatykaS5L7.md

- **つもりはない — structurally distinct negation of つもり** (lines 34-49): the lesson explicitly presents two negation patterns side by side — (1) V「ない」+つもりです and (2) つもり+はない (かけるつもりはない／どうようびにべんきょうするつもりはない). `vplaintsumoridesu-conviction-of-doing-something-planned-by-speaker.md` documents only pattern (1). Same gap as `toimport6.md` above, now confirmed as a deliberately taught alternate structure rather than a stray typo. Uncertain — needs review.

## JPLessons/Japoński_lekcje/Semestr5/L8/GramatykaS5L8.md

No findings — file is essentially empty (template headers only).

## JPLessons/Japoński_lekcje/Semestr5/L9/GramatykaS5L9.md

No findings — reviewed, all topics covered (superlative, comparison, どちらも, が vs は, やすい／にくい).

## JPLessons/Japoński_lekcje/Semestr5/L10/GramatykaS5L10.md

- **で — instrument/means particle** (lines 57-72): はしで食べます／くるまで／にほんごで, with a note that 乗る takes に not で. `subject-de-v-who-performs-action.md` explicitly excludes this use from its own scope. Same gap as `Semest1/L14/GramatykaS1L14.md` above.
- **どうやって — "how/by what method"** (lines 59-61, 77-91): すしはどうやって食べますか／XからYまでどうやっていきますか. `doudesuka-how-is.md` covers どうですか (asking for opinion/impression), a distinct function from asking about method. No file covers どうやって.
- **から — spatial/temporal starting-point particle ("from")** (lines 74-91): XからYまで／どうやっていきますか. `kara-because.md` covers only the causal ("because") sense; `made.md` covers まで but not から as the paired origin particle. No file covers から in this "from" sense.

## JPLessons/Japoński_lekcje/Semestr5/L11/GramatykaS5L11.md

- **から〜まで — "from X to Y" range/route marker** (lines 38-40): same gap as `Semestr5/L10.md` above.
- **どのくらいかかりますか** (lines 65-81): same gap as `Semestr4/GramatykaPodsumowanie.md`/`L12.md` above (どのくらい／ぐらい approximation + かかる idiom). Uncertain — needs review.
- **で — instrument/means particle** (line 127): same gap as `Semest1/L14.md` above.
- **に — stative-location particle** (line 222): same gap as `Semestr3/L5/GramatykaS3L5.md` above.

## JPLessons/Japoński_lekcje/Semestr5/L12/GramatykaS5L12.md

- **で — causal/instrumental particle** (lines 43-46): same gap as `Semest1/L14.md` above.
- **へ vs に with motion verbs** (line 51): same gap as `Semest1/L14.md` above.
- **なにか／だれか／どこか + に／で combinatorial particle marking** (lines 53-90): 何かに（おびえる）／何かで（人をころす）／だれかに／だれかで／どこかに／どこかで. `dareka-someone.md`/`dokoka-somewhere-anywhere.md` document only the bare indefinite pronoun, not the systematic に(agent/target) vs で(means) attachment with distinct meanings. Uncertain — needs review.
- **に as source-of-transfer marker with もらう-type verbs** (line 90): related to the already-flagged plain-object もらう/くれる gap, but specifically calling out に's role as "received from" marker — not addressed by any file. Uncertain — needs review.

## JPLessons/Japoński_lekcje/Semestr5/L13/GramatykaS5L13.md

- **V-stem + たい — "want to do"** (lines 11-19): したい (chcieć). `hoshii-i-want-n.md` covers N が ほしい (want a noun); `te-form-hoshii-desu.md` covers Vて+ほしいです (want someone else to do something). Neither documents the volitional V-stem+たい ("I want to do X") pattern itself — a foundational N5 pattern with no dedicated file.

## JPLessons/Japoński_lekcje/Semestr6/S6L11.md

- **Vて形+ください** (lines 417-418): same gap as `Semestr2/L10.md`/`L11.md` above.
- **ます形／て形／ない形／た形 conjugation-by-verb-group** (lines 174-261): same gaps as flagged throughout Semestr2-4 above.

## JPLessons/Japoński_lekcje/Semestr6/L01/GramatykaS6L1.md

- **いる — "to need" (distinct from 必要)** (lines 22-23): same gap as `Semestr3/Podsumowanie semestr 3.md` above.
- **から — "from" origin particle** (line 53): ...から来ました. Same gap as `Semestr5/L10.md` above.
- **ある — existence** (line 86): same gap as `Semestr2/L05.md` above.
- **よく + negative — frequency adverb with negation** (lines 109-121): same gap as `Semestr2/L01.md` above.
- **と — quotative marker for onomatopoeia/mimicry** (line 81): ワンワンとほえますか. No file documents と attaching to sound-mimicking words (existing と-files all cover thought/speech verbs). Likely too narrow for its own entry. Uncertain — needs review.

## JPLessons/Japoński_lekcje/Semestr6/L02/GramatykaS6L2.md

- **ところで — topic-change discourse marker ("by the way")** (line 216): そうですか。ところで、たけしさんは…. No file covers this discourse connector (`conjunctions.md` only covers くて／で "and" and contrastive が).
- **どうしますか vs 何をしますか — usage-nuance contrast** (lines 191-194): asking about a course of action/decision vs. a concrete activity. No file addresses this distinction. Uncertain — needs review (could be vocab-level rather than a distinct grammar pattern).
- **じゃあ — discourse transition ("well then / so")** (line 226): sentence-initial conversational connector. No file covers it. Uncertain — needs review (borderline vocab/discourse-marker).

(なる change-of-state paradigm, いい→よく, どっち／のほうが, どこにも+neg — all covered by existing files, not findings.)

## JPLessons/Japoński_lekcje/Semestr6/L02/GramatykaS6L2 1.md

**Not a true duplicate.** Compared byte-for-byte against `GramatykaS6L2.md`: the `## Notatki`/`### Gramatyka`/`### Konwersacja` sections are identical between the two files. This file additionally has a filled-in `## Podsumowanie` Anki flashcard block (Rzeczowniki/Czasowniki with `Tłumaczenie:`/`<!--ID:-->` lines) that the other file lacks — i.e. this is the same lesson *after* the fill-templates step ran, a later processing stage rather than a content fork. This resolves the ⚠ flag from task-description.md. Same three findings as `GramatykaS6L2.md` above apply (same line numbers); no additional findings from the flashcard section (vocabulary only, no new grammar).

## JPLessons/Japoński_lekcje/Semestr6/L03/GramatykaS6L3.md

- **と言ったら — free-association "when you say X, [it makes you think of] Y"** (lines 137-147): word-association pattern (suika to ittara midori — "watermelon" → "green"). `toiuimidesu-means.md` covers という意味です (explaining a definition), a different function. No file covers this pattern.

(のほうが～より, all four conditionals たら/ば/と/なら, も...も — all covered by existing files, not findings.)

## JPLessons/Japoński_lekcje/Semestr6/L04/GramatykaS6L4.md

- **度（ど）— counter suffix for degrees/temperature** (lines 57-60): 何度／五度. Not among the counters documented in `counters.md`/`counter-sufixes.md`. Extends the already-known assorted-counters gap with a specific new counter.

(の中で一番, ADJ+の as noun substitute — covered by existing files, not findings.)

## JPLessons/Japoński_lekcje/Semestr6/L05/GramatykaS6L5.md

- **ね sentence-final particle** (lines 51, 71): same gap as `Indywidualne/L2.md` above.
- **どちら as a plain selection question (not comparative)** (line 155): どちらのコーヒーを飲みますか. Same gap as `Semestr4/GramatykaPodsumowanie.md`/`L12.md` above (どれ vs どちら). Uncertain — needs review.

(Vたい full paradigm — covered by `hoshii-i-want-n.md` per this file's own examples, but see `Semestr5/L13.md` above for the base V-stem+たい pattern gap; ADJ+の, いかがですか — covered by existing files, not findings.)

## JPLessons/Japoński_lekcje/Semestr6/L06/GramatykaS6L6.md

- **なる + plain negative verb (V-ない+なる) — "it became the case that I no longer do X"** (lines 19-21): 行かない→行かなくなる. `narimasu-vs-shimasu-change-of-state.md` shows no negative-verb example; `you-ni-narimasu-naku-narimasu.md`'s なくなります is restricted to the potential form ("become unable to"), a distinct meaning from this plain cessation use. No file covers plain-verb+なくなる.
- **ね sentence-final particle** (line 52): same gap as `Indywidualne/L2.md` above.
- **こちら vs この — polite spatial/object pointer (retail register)** (line 75, 237, 243): shop staff pointing at merchandise. `sonkeigo-polite-people-reference.md` covers こちら/そちら/あちら/どちら only as a polite way to refer to a *person*, not this spatial/object-pointing usage. Uncertain — needs review.
- **ありがとうございました vs ありがとうございます — past vs. present polite thanks** (line 74): `gozaimasu-polite-arimasu-desu.md` doesn't address this tense/register distinction. Uncertain — needs review, may be fixed-phrase rather than grammar.
- **さいきん + casual-form verb + 時間がありません idiom** (line 76): no file documents this compositional construction. Uncertain — needs review, may be too minor for its own file.

## JPLessons/Japoński_lekcje/Semestr6/L07/GramatykaS6L7.md

No new findings — recurrences only of the L06 gaps above (なる+negative verb, ね, こちら vs この, ありがとうございました, さいきん idiom). たがっている, と言っていました, そう appearance-inference, にする decision are all covered by existing files.

## JPLessons/Japoński_lekcje/Semestr6/L08/GramatykaS6L8.md

- **ほしがる／ほしがっています with を — particle switches from が to を for 3rd-person noun-desire** (lines 82-85, 94, 107-109, 122-123, 148-151, 166-170): source explicitly flags "zmiana partykuły!!!" (particle change!). `hoshii-i-want-n.md` mentions 欲しがる in passing for 3rd person but gives no example and doesn't document the が→を particle shift. Uncertain — needs review, partial/near-miss coverage.

(Recurrences of L06 gaps also present — なる+negative verb, ね, こちら vs この, ありがとうございました, さいきん idiom.)

## JPLessons/Japoński_lekcje/Semestr6/L09/GramatykaS6L9.md

No new findings — recurrences only of L06/L08 gaps above. ために (purpose) IS covered by `tameni-for-purpose-of.md`.

## JPLessons/Japoński_lekcje/Semestr6/L10/GramatykaS6L10.md

- **について** (lines 111-112, 119, 124-125): クリスマスについて話しましょうか. Same gap as `Semestr4/L05/GramatykaS4L5.md` above.
- **Vないでほしい — negative "I want X to NOT do Y"** (lines 82-85, 156-162, 197-200, 248-250): いかないでほしい／友だちにうそを付かないでほしいです. `te-form-hoshii-desu.md` documents only the affirmative Vて形+ほしい; its negative counterpart isn't mentioned anywhere. Same finding as `Semestr6/L11.md` below. Uncertain — needs review.

(Recurrences of L06/L08 gaps also present. Affirmative Vて形+ほしい IS covered by `te-form-hoshii-desu.md` — only the negative form above is new.)

## JPLessons/Japoński_lekcje/Semestr6/L11/GramatykaS6L11.md

- **Vないでほしい — negative "want someone NOT to do X"** (lines 83-86): 友だちにうそを付かないでほしいです. Same finding as `Semestr6/L10.md` above, appearing independently in both files — confirms this is a deliberately taught negative counterpart to てほしい, not a one-off. Uncertain — needs review.

## JPLessons/Japoński_lekcje/Semestr6/L12/GramatykaS6L12.md

No findings — reviewed, a near-duplicate review recap of L11 with no new material.

## JPLessons/Japoński_lekcje/Semestr6/L13/GramatykaS6L13.md

No findings — reviewed, all topics covered (た形+ことがあります matches `ta-kotogaarimasu-have-you-ever.md`; remainder repeats L11).

## JPLessons/Japoński_lekcje/Semestr7/S7L1-L2.md

- **や...や(など) — non-exhaustive listing conjunction for nouns** (lines 221-283): explicitly drilled in contrast with とか...とか (cards flagged "!!! Zwróć uwagę na spójnik"), e.g. 東京や京都やおおさかに行きました. Same finding as `Semestr7/L02/GramatykaS7L2.md` below.
- **と同じ／と同じくV — "the same as N"** (lines 63-85): すずきさんと同じコートをきています／木森さんと同じくスキーする. Same finding as `Semestr7/L02.md` below.
- **ことがある (dict-form habitual, extended to な-adjective/copula/noun forms)** (throughout): 夜のさんぽすることがある／たいどが失礼であることがある／しずかなことがある／田中さんは先生のことがあります. Same gap as `toimport6.md`'s already-flagged V-dict+ことがある, here confirming the extension to adjective/noun forms — see `Semestr7/L01/GramatykaS7L1.md` below for the fuller confirmed-gap writeup.

## JPLessons/Japoński_lekcje/Semestr7/S7L3.md

No findings — reviewed, almost entirely vocabulary/conjugation-form tables; the one grammar item (contrastive が) IS covered by `contrastive-ga-but.md`.

## JPLessons/Japoński_lekcje/Semestr7/L01/GramatykaS7L1.md

- **辞書形+ことがある — occasional/habitual occurrence (upgrading from uncertain to confirmed gap)** (lines 9-44): explicitly contrasts (a) 辞書形/adjective/noun+ことがある = "it sometimes happens that..." (present-tense habitual, e.g. 犬が夜に吠えることがある, extended to い-adjectives, な-adjectives「なことがある／であることがある」, and nouns「のことがある／であることがある」) against (b) た形+ことがある/ことがあった (past-experience patterns). `ta-kotogaarimasu-have-you-ever.md` and `ttakotogaarimashita-i-once-did-recalling-a-single-past-experience.md` both only cover the た形 experience/recollection meanings and explicitly warn the dictionary-form variant means something different — but no file exists for the dictionary-form habitual/occasional-occurrence meaning itself, including its adjective/noun extensions. This was previously flagged as uncertain (`Indywidualne/L3.md`); now confirmed as a genuine gap given the full dedicated lesson treatment here.

## JPLessons/Japoński_lekcje/Semestr7/L02/GramatykaS7L2.md

- **同じ — "the same as X"** (lines 3-8): Xさんと同じN／Xさんと同じくVerb. Searched all of `grammar-index/grammar/` for 同じ — zero matches. Structurally distinct from どちら/のほうが (more) and より (more than) comparison patterns.
- **や...や (non-exhaustive noun listing, context-tied) vs とか (context-free listing)** (lines 45-57, 73-119): や implies items share a place/time/context; とか doesn't. `tokatoka-enumerate-examples.md` fully covers とか but mentions や...や only in passing inside its Notes, with no structure/examples/register treatment of its own.

## JPLessons/Japoński_lekcje/Semestr7/L03/GramatykaS7L3.md

- **すごく vs とっても — "very" intensifiers (register pair)** (lines 61-65, 113-120): すごく (casual/emotional) vs とっても (neutral, more common). `degree-adverbs-sukoshi-amari-zenzen.md` covers 少し／あまり／全然 (amount/negation-scaled degree), a different function. No file covers this positive-intensifier register pair.

(どんな+N covered by `donna-n-what-kind.md` — not a finding.)

## JPLessons/Japoński_lekcje/Semestr7/L04/GramatykaS7L4.md

No findings — file contains no text content, only section headers and a pasted image.

## JPLessons/Japoński_lekcje/Semestr8/L01/GramatykaS8L1_pre.md

No findings — reviewed, all topics covered (んです／のです matches `ndesu-nodesu-explaining-reason.md` closely).
