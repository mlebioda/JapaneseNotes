# Documentation Agent — Tasks

- [x] Create `.cowork/skills/generate-diagram.md` — skill file with trigger phrases, extraction protocol (including fallback name derivation rule, deprecated-agent rule, script invocation note rule), PlantUML notation style reference (canonical example from plan), scribe A2A call, and "never touch" list
- [x] Create `.claude/agents/documentation.md` — agent file with YAML frontmatter (tools: Read, Write, Edit, Bash, Agent), access rules table, trigger phrases, workflow (load generate-diagram skill), hard rules (including named SCRIBE CALL RULE), and error handling
- [x] Add `documentation` agent entry to `.cowork/instructions.md` agent system section (requires explicit user confirmation before writing)
- [x] Modify `.claude/agents/skill-implementer.md` to add auto-trigger step: after writing/editing/deleting any file under `.claude/agents/` or `.cowork/skills/`, call `documentation` agent A2A once per run to regenerate `docs/vault-system-diagram.puml` (requires explicit user confirmation before writing)
- [ ] Verify generate-diagram.md includes a hard rule: "only write vault-system-diagram.puml — never touch other files in docs/"
