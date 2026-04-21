---
name: find-skills
description: Use in Codex when the user asks to find relevant Codex skills for a project or idea. Read available SKILL.md metadata and return precise recommendations first.
---

# Find Skills For Codex

Use this Codex skill when the user asks to find skills for the current project, a project idea, or a domain such as CRM, games, agents, RAG, frontend, backend, security, analytics, or deployment.

Do not ask the user to run Python or terminal commands. Inspect files directly.

## Codex Workflow

1. Understand the project intent from the user's request or from lightweight project files.
2. Search Codex skill metadata first:

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

4. Match against `name`, `description`, `When to Use`, headings, and routing tables.
5. Identify candidate clusters before ranking.
6. Run the Clarification Gate below.
7. If enough information is available, group candidates as `Precise`, `Balanced`, and `Recall`.
8. Show `Precise` in the chat. Mention that broader candidates can be reviewed if useful.

## Clarification Gate

Before recommending skills, decide whether the request has enough information to make precise recommendations.

Do not use a fixed question list. Instead, infer the most important missing dimensions from:

- the user's request
- project files, if available
- candidate skill metadata: `name`, `description`, `When to Use`, headings, and routing tables

Ask clarification questions only when the answers would change which skills are recommended.

Look for routing signals such as:

- platform, runtime, or integration target choices
- language, framework, or toolchain choices
- implementation vs design vs testing vs deployment needs
- scope or maturity level
- domain, subdomain, modality, or data/source choices

If one missing answer could move a skill between `Precise` and `Balanced`, ask up to 3 concise clarification questions and do not recommend skills yet.

If the user asks for quick recommendations, says assumptions are fine, or the likely route is obvious from context, proceed with explicit assumptions.

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
