# preprocess-templates — Tasks

- [x] Component 1: Create `.cowork/skills/references/label-aliases.json` with all 31 alias-table entries from `card-templates.md`
- [x] Component 2: Create `.cowork/scripts/preprocess-templates.py` (loads `label-aliases.json`, processes lines below `# Summary`, atomic write via `os.replace`, prints replacement summary)
- [x] Component 3a: Update `.cowork/skills/references/card-templates.md` — replace alias table body with pointer to `label-aliases.json`; fix `#wp` canonical template (`そう: [value]` → `そう (looks): [value]`)
- [x] Component 3b: Update `.cowork/skills/references/adj-forms.md` — rename `そう:` to `そう (looks):` in all four code blocks (い-adjective, いい/よい special case, な-adjective, non-adjective); leave prose/heading references to `そう` unchanged
- [x] Component 4: Update `.cowork/skills/templates-update.md` — add Step 0 script call before Repair 1; update Repair 1 description to note alias renames are pre-handled; update skill intro/description
- [x] Component 5: Read `.cowork/skills/fill-templates.md` and update any alias-table reference to point to `label-aliases.json` (skip if no such reference exists)
