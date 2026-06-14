# General Lessons Learned

<!-- Entries appended by scribe capture — domain: everything not covered by agent or skill design -->

---
## 2026-06-11 — practice-grammar.md (hardcoded session path)

**Classification**: bug-fix
**What happened**: The Calendar sync section referenced a hardcoded Claude session mount path (`/sessions/<name>/mnt/ObsidianJP/`) that is unique to one ephemeral session; replaced with a `VAULT_ROOT` constant pointing to the stable macOS vault root, with a NOTE comment instructing Claude to translate to the active session mount at runtime.
**Rule**: **[Rule]** Never hardcode a session-scoped mount path (e.g. `/sessions/<name>/mnt/`) in any skill or agent file — use a named constant for the stable vault root and add a NOTE comment for any runtime path translation needed.
**Source**: uncommitted — manual

---
