---
name: find-skills
description: Use when the user asks to find relevant Codex skills for a project or idea. Read available SKILL.md metadata and return precise recommendations first.
---

# Find Skills

Use this workflow when the user asks to find skills for the current project, a project idea, or a domain such as CRM, games, agents, RAG, frontend, backend, security, analytics, or deployment.

Do not ask the user to run Python or terminal commands. Inspect files directly.

## Workflow

1. Understand the project intent from the user's request or from lightweight project files.
2. Search available skill metadata first:

```text
~/.codex/skills/**/SKILL.md
<project-root>/.codex/skills/**/SKILL.md
```

3. If the repository also includes portable host folders, optionally inspect:

```text
<project-root>/.claude/skills/**/SKILL.md
<project-root>/.gemini/skills/**/SKILL.md
<project-root>/.cursor/skills/**/SKILL.md
```

4. Match against `name`, `description`, `When to Use`, and headings.
5. Group candidates as `Precise`, `Balanced`, and `Recall`.
6. Show `Precise` in the chat. Mention that broader candidates can be reviewed if useful.

## Output

```text
Precise recommendations

1. <skill-name>
   Why: <short reason>
   Path: <local SKILL.md path>

Broader candidates:
- Balanced: <count or short list>
- Recall: <count or short list>
```

Prefer more recall when the user says they want as many related skills as possible.
