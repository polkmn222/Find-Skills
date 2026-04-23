# Implementation Traceability

When implementation begins after checklist and index gates, keep the work traceable to the checklist and index.

The final response or generated implementation documentation should identify:

- checklist path used
- search index path used
- selected project-local skills used for implementation
- main files or folders created or changed
- verification commands that passed
- verification commands that could not run, with concrete reason
- local server URL started for a runnable app or dashboard
- remaining assumptions, safety limits, or excluded scope

Keep this focused on checklist-derived requirements and files changed for the requested work. Do not use it to justify unrelated refactors.

## Implementation Gate

Before implementation begins:

1. Confirm the completed checklist.
2. Confirm the generated search index.
3. Verify selected or required skills under `.gemini/skills/<skill-name>/SKILL.md`.
4. Confirm any assumptions that affect files, dependencies, cost, data access, or irreversible actions.

## Install-Only Requests

If the user asks only to install skills:

- install/copy only the requested or indexed skills
- use project-local `.gemini/skills/`
- verify each `SKILL.md`
- update index installation status when an index exists
- do not implement, scaffold, refactor, or create unrelated artifacts

