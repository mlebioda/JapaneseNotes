# General Lessons Learned

<!-- Entries appended by scribe capture — domain: everything not covered by agent or skill design -->

---
## 2026-06-15 — docs/vault-system-diagram.puml

**Classification**: improvement
**What happened**: Diagram notes for practice-grammar, kanji-file, and templates-update were updated to include specific mechanic names (named repair steps, decimal Unicode URL format, score-buffer write timing, Study Mode batch interlude) that had been added to the skills since the last diagram regeneration.
**Rule**: **[Rule]** After each skill improvement pass, update the diagram note for that skill with the specific mechanic names and behavioural contracts added — a diagram note that omits implementation details (named steps, encoding schemes, write-timing rules) drifts from reality and becomes less useful than reading the skill file directly.
**Source**: uncommitted — documentation agent

---
## 2026-06-15 — docs/vault-system-diagram.puml (wording sanitisation)

**Classification**: improvement
**What happened**: Diagram source was refined to replace Unicode em-dashes in comment arrows with ASCII `->`, Japanese passage-type labels with English equivalents, and non-ASCII characters in note blocks — changes needed because Unicode content survives PlantUML rendering but breaks grep, diff, and tool-based reads.
**Rule**: **[Rule]** In a documentation diagram source file, use only ASCII characters in comment lines, arrow labels, and note blocks — Unicode arrows and non-ASCII labels survive rendering but silently break diff readability, grep, and any tool that expects plain-text content.
**Source**: uncommitted — documentation agent

---

## 2026-06-11 — practice-grammar.md (hardcoded session path)

**Classification**: bug-fix
**What happened**: The Calendar sync section referenced a hardcoded Claude session mount path (`/sessions/<name>/mnt/ObsidianJP/`) that is unique to one ephemeral session; replaced with a `VAULT_ROOT` constant pointing to the stable macOS vault root, with a NOTE comment instructing Claude to translate to the active session mount at runtime.
**Rule**: **[Rule]** Never hardcode a session-scoped mount path (e.g. `/sessions/<name>/mnt/`) in any skill or agent file — use a named constant for the stable vault root and add a NOTE comment for any runtime path translation needed.
**Source**: uncommitted — manual

---
