# Slug Normalization Rules

Used by `extract-grammar.md` Step 6a. Output path: `grammar-index/grammar/<slug>.md`.

## Algorithm (apply in order)

1. Replace `・` and `/` with a space.
2. Prefer parenthesized readings — `<kanji>（<reading>）` → keep only the kana reading, drop the kanji + attached okurigana + parens. `特別な動詞（とくべつなどうし）` → `とくべつなどうし`.
3. Transliterate kana → romaji (Hepburn, table below). Compound kana before single kana. `っ` doubles the next consonant (lone `っ` at end → `t`). `ん` before b/m/p → `m`, else `n`. `ー` → drop. Kanji are not transliterated here (stripped in step 6).
4. Lowercase everything.
5. Dedup kana against Latin — if a transliterated kana token equals a Latin token already present (case-insensitive, ignoring `-`), drop the transliterated copy. `ウチ・ソト (Uchi-Soto)` → `uchi-soto`, not `uchisoto-uchi-soto`.
6. Strip remaining non-ASCII (kanji, `〜`, `（`, `）`, `「`, `」`).
7. Strip punctuation except `-`.
8. Replace space-runs with a single `-`.
9. Strip leading/trailing `-`.
10. Collapse consecutive `-`.
11. Empty result (all-kanji heading, no kana/Latin) → positional fallback `point-1`, `point-2`, ...

## Kana → romaji table

| Kana | Romaji | Kana | Romaji | Kana | Romaji | Kana | Romaji | Kana | Romaji |
|---|---|---|---|---|---|---|---|---|---|
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

Compound kana (apply before single): きゃ→kya, きゅ→kyu, きょ→kyo, しゃ→sha, しゅ→shu, しょ→sho, ちゃ→cha, ちゅ→chu, ちょ→cho, にゃ→nya, にゅ→nyu, にょ→nyo, ひゃ→hya, ひゅ→hyu, ひょ→hyo, みゃ→mya, みゅ→myu, みょ→myo, りゃ→rya, りゅ→ryu, りょ→ryo, ぎゃ→gya, ぎゅ→gyu, ぎょ→gyo, じゃ→ja, じゅ→ju, じょ→jo, びゃ→bya, びゅ→byu, びょ→byo, ぴゃ→pya, ぴゅ→pyu, ぴょ→pyo. (Katakana equivalents transliterate the same.)

## Worked examples

| Heading | Slug |
|---|---|
| `Particle が vs は` | `particle-ga-vs-ha` |
| `Vないでください` | `vnaidekudasai` |
| `V + て-form (request)` | `v-te-form-request` |
| `がんばって！Let's do our best` | `ganbatte-lets-do-our-best` |
| `同じ` (kanji only, no kana) | `ji` |
| `目` (kanji only, no kana/Latin) | `point-1` |
| `お・ご V「ます形」します` | `o-go-v-masushimasu` |
| `特別な動詞（とくべつなどうし）` | `tokubetsunadoushi` |
| `ウチ・ソト (Uchi-Soto) - In-group / Out-group` | `uchi-soto-in-group-out-group` |

Note: Latin letters (`V`, `N`, `Adj`) pass through unchanged except lowercasing.

User override from Step 5 always wins — use verbatim, skip this file entirely.
