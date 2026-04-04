# Skill: update-kanji-list

## Purpose
Search files with caligraphy lessons to update list of known kanjis that will be used to add #k tags to #w, #wc, #wp templates by other skills.

## Triger phrases
User says: "Update kanji list [file]"

## Input
[file] is an caligraphy lesson.
Each header except file title header should contain Kanji.
[KanjiList.md] file with all known by me kanjis.

## What to produce
Update [KanjiList.md] in ObsidianJP directory with Kanjis from headers included in headers in [file].
- If kanji from header is in the [KanjiList.md], don't add to list.

