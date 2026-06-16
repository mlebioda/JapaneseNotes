# Kanji-File: Bare Link Migration and Broken Link Removal Fix — Tasks

- [x] Edit `.cowork/skills/kanji-file.md` Step 4: change "log a warning; do not remove the link" → remove the link and record it as `REMOVED: [[<link>]] — no file found` in the completion report
- [x] Edit `.cowork/skills/kanji-file.md` Step 5: replace single-destination migration ("move to `## Occurences`") with two-destination classification — bare links without `#` → `### Parts`; bare links with `#` → `## Occurences`
- [x] Edit `.cowork/skills/kanji-file.md` Step 6: remove language implying broken links are only warned about; add check that no bare links remain outside named `##` sections after Steps 4–5
- [x] Edit `.cowork/skills/kanji-file.md` completion report examples: replace single `bare link migration` count with separate `REMOVED` count and `### Parts migration` count
- [x] Fix `Caligraphy/Kanji/千-1000.md`: read file first, then remove `[[丿 - component]]` from `## Occurences`, move `[[十-ten,10]]` to `### Parts`, leave `[[UN5KL2#千 - 1000・ち・セン]]` untouched
