# Find Skills

Markdown-only skill discovery guide for agents.

Use this repository when you want an agent to read available `SKILL.md` files and recommend relevant Codex skills for a project or idea. Python execution is not required.

Repository URL:

```text
https://github.com/polkmn222/Find-Skills.git
```

## Choose Your Tool

Use the same repository, but install or invoke it in the way your host expects.

| Tool | Install Target | First Use |
| --- | --- | --- |
| Codex CLI | `.codex/skills/find-skills` | `Use find-skills to find relevant skills for this project.` |
| Claude Code | `.claude/skills/find-skills` | `Use find-skills to find relevant skills for this project.` |
| Cursor | `.cursor/skills/find-skills` | `@find-skills find relevant skills for this project.` |
| Gemini CLI | `.gemini/skills/find-skills` | `Use find-skills to find relevant skills for this project.` |

## Install

Install for Codex CLI:

```bash
tmp=$(mktemp -d)
git clone https://github.com/polkmn222/Find-Skills.git "$tmp/find-skills"
mkdir -p .codex/skills
cp -R "$tmp/find-skills/.codex/skills/find-skills" .codex/skills/
```

Install for Claude Code:

```bash
tmp=$(mktemp -d)
git clone https://github.com/polkmn222/Find-Skills.git "$tmp/find-skills"
mkdir -p .claude/skills
cp -R "$tmp/find-skills/.claude/skills/find-skills" .claude/skills/
```

Install for Cursor:

```bash
tmp=$(mktemp -d)
git clone https://github.com/polkmn222/Find-Skills.git "$tmp/find-skills"
mkdir -p .cursor/skills
cp -R "$tmp/find-skills/.cursor/skills/find-skills" .cursor/skills/
```

Install for Gemini CLI:

```bash
tmp=$(mktemp -d)
git clone https://github.com/polkmn222/Find-Skills.git "$tmp/find-skills"
mkdir -p .gemini/skills
cp -R "$tmp/find-skills/.gemini/skills/find-skills" .gemini/skills/
```

Install all hosts:

```bash
tmp=$(mktemp -d)
git clone https://github.com/polkmn222/Find-Skills.git "$tmp/find-skills"
mkdir -p .codex/skills .claude/skills .cursor/skills .gemini/skills
cp -R "$tmp/find-skills/.codex/skills/find-skills" .codex/skills/
cp -R "$tmp/find-skills/.claude/skills/find-skills" .claude/skills/
cp -R "$tmp/find-skills/.cursor/skills/find-skills" .cursor/skills/
cp -R "$tmp/find-skills/.gemini/skills/find-skills" .gemini/skills/
```

## Direct Use Without Installing

Point your agent at the host-specific skill file.

Codex:

```text
Read `/path/to/Find-Skills/.codex/skills/find-skills/SKILL.md` and find relevant skills for this project.
```

Claude Code:

```text
Read `/path/to/Find-Skills/.claude/skills/find-skills/SKILL.md` and find relevant skills for this project.
```

Cursor:

```text
Read `/path/to/Find-Skills/.cursor/skills/find-skills/SKILL.md` and find relevant skills for this project.
```

Gemini CLI:

```text
Read `/path/to/Find-Skills/.gemini/skills/find-skills/SKILL.md` and find relevant skills for this project.
```

## Installed Files

Each host gets a self-contained skill:

```text
.codex/skills/find-skills/SKILL.md
.claude/skills/find-skills/SKILL.md
.cursor/skills/find-skills/SKILL.md
.gemini/skills/find-skills/SKILL.md
```

Each installed skill is self-contained. Installing only one host folder is enough.

The installed `find-skills/SKILL.md` is the runtime entrypoint. It does not require the repository root `SKILL.md`, README files, or other host folders after installation.

## Maintainer Checks

Run all lightweight checks before committing:

```bash
./scripts/check-all.sh
```

This runs the host-copy sync check and the structured scoring-case guardrail check.

## Maintaining Host Copies

The host-specific `SKILL.md` files should stay aligned except for host names, workflow headings, and install/search paths. Use the Codex copy as the comparison baseline when editing shared content:

```text
.codex/skills/find-skills/SKILL.md
```

Safe update flow:

1. Edit the shared content in all host-specific `SKILL.md` files.
2. Keep only the host-specific labels and paths different.
3. Run the drift check:

```bash
./scripts/check-skill-sync.sh
```

The check normalizes expected host differences and fails when any shared content drifts. It has no external dependencies beyond standard shell tools, so it can also be used as a lightweight CI check.

## What The Agent Does

The agent should:

1. Read `SKILL.md`.
2. Understand the project or idea.
3. Search available `SKILL.md` files.
4. Infer whether missing context would change the recommendation.
5. Ask up to 3 clarification questions only when needed.
6. Score candidates and bucket them into `Precise`, `Balanced`, `Recall`, or `Exclude`.
7. Show only `Precise` recommendations in chat unless the user asks for more.
8. Mention broader candidates when useful.

## Scoring Model

Candidate scoring is rubric-first. The installed `SKILL.md` files define a base score from `0-100` using task match, routing fit, actionability, specificity, and confidence. Optional external signals can adjust that score, but the total external adjustment is bounded to `-15..15`.

External signals may include prior successful use, project-local stack evidence, user or repo preferences, recent usage patterns, skill freshness, retrieval scores, and optional SNS/community evidence. Community signals are conservative by design: they can support candidate expansion, trend detection, practical usage evidence, confidence adjustment, and freshness checks, but they cannot override repository metadata, hard constraints, or the base rubric.

Bucket assignment is not score-only. `Precise` requires a strong final score, base score at least `70`, direct task support, no hard conflict, immediate actionability, and explicit metadata evidence. Hard conflicts always force `Exclude`.

Human-readable and machine-readable scoring cases are in:

```text
examples/scoring-cases.md
examples/scoring-cases.yaml
```

Validate the structured cases with:

```bash
./scripts/check-scoring-cases.py
```

## Output Format

Scores are request-relative fit scores, not general skill quality scores. Normal user-facing output should stay concise, with detailed scoring breakdowns reserved for audit/debug or when requested.

```text
Precise

1. <skill-name> - <final_score> final / <base_score> base
   Reason: <one-line request-relative fit reason>
   Evidence: <name, description, When to Use, routing table, or project-context evidence>
   External: <external_adjustment, only if nonzero>

Balanced

1. <skill-name> - <final_score> final / <base_score> base
   Reason: <one-line reason>
   Evidence: <metadata or project-context evidence>
   Why not precise: <missing detail, adjacent scope, weaker actionability, or lower evidence>

Recall

1. <skill-name> - <final_score> final / <base_score> base
   Reason: <fallback, exploration, or follow-up value>
   Evidence: <metadata or project-context evidence>
   Caveat: <why it is broad or conditional>

Excluded

1. <skill-name> - Excluded
   Reason: <hard conflict, contradicted constraint, or out-of-scope explanation>
```

If there are no `Precise` matches, say so and show the best `Balanced` or `Recall` candidates. If the request is ambiguous, state the missing detail that would improve routing. Excluded candidates should only be shown when they explain an important conflict.

The agent also writes a local index under the current project root:

```text
.find-skills/<key>/index.md
```

`<key>` is a short lowercase slug for the user's search, such as `web-game`, `crm`, or `agent-eval`.

The index should include ranked candidates with bucket, score, reason, source path, and install notes.

## Example Domains

CRM project:

```text
revops
hubspot-automation
salesforce-automation
pipedrive-automation
zoho-crm-automation
odoo-sales-crm-expert
```

Small game project:

```text
game-development
2d-games
web-games
game-design
game-art
game-audio
godot-gdscript-patterns
unity-developer
```

Agent project:

```text
agents-md
agent-tool-builder
ai-agents-architect
agent-evaluation
multi-agent-patterns
skill-creator
skill-installer
```

## Search Index

Use key-based folders under the current project root:

```text
.find-skills/<key>/index.md
```

`.find-skills/` is disposable. It can be deleted and recreated.
