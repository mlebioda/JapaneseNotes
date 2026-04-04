# Skill: git-commit

## Purpose
Stage, commit, and push accepted changes to GitHub after any skill
has modified lesson files in the vault.

## Trigger phrases
User says: "commit", "push", "save to git", "commit [filename]"

#

0# Vault git repo
/Users/michallebioda/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianJP/

## Workflow

### 1. Show what changed
Run:
```
git -C "[vault path]" status
git -C "[vault path]" diff --stat
```
Show the user a clean summary: which files changed and how many lines.

### 2. Suggest a commit message
Write a short, descriptive commit message based on what changed.
Follow this format:
```
[skill] filename — short description

Examples:
fill-templates UNGL15 — verb and adjective forms filled
fill-templates UNGL15 UNGL16 — batch fill verb and adjective forms
```

Show the message to the user and ask: "Commit with this message?"

### 3. Wait for confirmation
Never commit or push without explicit user confirmation.
Accepted responses: "yes", "ok", "go ahead", "push it"

### 4. Commit and push
On confirmation run:
```
git -C "[vault path]" add [changed files only]
git -C "[vault path]" commit -m "[message]"
git -C "[vault path]" push origin main
```

Report: "Pushed to GitHub ✓"

## Rules
- Never use `git add .` — only stage files that were explicitly modified in this session
- Never commit .obsidian/ files, .DS_Store, or .md.bak backup files
- Never force push
- If push fails, report the exact error and stop — do not retry automatically
- Always show diff summary before asking for confirmation
- Commit message must reference which skill made the change