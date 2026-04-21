---
name: find-skills
description: Use in Codex when the user asks to find relevant Codex skills for a project or idea. Read available SKILL.md metadata and return precise recommendations first.
---

# Find Skills For Codex

Use this Codex skill when the user asks to find skills for the current project, a project idea, or a domain such as CRM, games, agents, RAG, frontend, backend, security, analytics, or deployment.

This installed skill must work by itself after being copied to `.codex/skills/find-skills`. Do not depend on the repository root, README files, or sibling host folders being present.

## Operating Rules

- Do not ask the user to run Python, shell, or install commands.
- Inspect local files directly. Prefer `rg` or filesystem search when tools are available.
- Use only skill metadata and lightweight project context unless the user asks for deeper analysis.
- If the request is broad, ask only the clarification questions that would change the recommendation.
- If the user asks for quick recommendations or says assumptions are fine, proceed and state assumptions.
- If no usable `SKILL.md` files are found, say what paths were checked and why recommendations are limited.

## Codex Workflow

1. Understand the project intent from the user's request or from lightweight project files.
2. Search Codex skill metadata first. Start with likely installed locations, then project-local locations:

```text
~/.codex/skills/**/SKILL.md
<project-root>/.codex/skills/**/SKILL.md
```

3. Read candidate metadata, not whole skill bodies by default. Use frontmatter, `name`, `description`, `When to Use`, headings, and routing tables.
4. Identify candidate clusters before ranking.
5. Run the Clarification Gate below.
6. If enough information is available, group candidates as `Precise`, `Balanced`, and `Recall`.
7. Write the Search Index below.
8. Show `Precise` in the chat. Mention the index path and that broader candidates can be reviewed if useful.

## Candidate Ranking

- `Precise`: Directly matches the user's task, platform, stack, scope, or route decision.
- `Balanced`: Likely useful but depends on missing details or supports adjacent work.
- `Recall`: Broadly related, optional, or useful only for specialized follow-up.

Prefer fewer, sharper `Precise` recommendations. Do not pad the list.

## Search Index

When recommendations are produced, create this file under the current project root:

```text
.find-skills/<key>/index.md
```

Choose `<key>` as a short lowercase slug from the user's search intent, for example `web-game`, `crm`, `agent-eval`, or `security-audit`.

The index must make installation easy. Include:

- search key and original user request
- assumptions or clarification answers used
- ranked candidates with index number, score from 0-100, bucket, skill name, reason, and local `SKILL.md` path
- install notes or copy commands when the candidate path is portable or project-local
- separate sections for `Precise`, `Balanced`, and `Recall`

Use scores consistently:

- `90-100`: direct fit
- `75-89`: strong fit with minor assumptions
- `60-74`: useful adjacent skill
- `<60`: recall-only candidate

If filesystem writes are unavailable, show the same index content in chat and say that the file could not be written.

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
