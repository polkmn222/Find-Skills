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

## What The Agent Does

The agent should:

1. Read `SKILL.md`.
2. Understand the project or idea.
3. Search available `SKILL.md` files.
4. Infer whether missing context would change the recommendation.
5. Ask up to 3 clarification questions only when needed.
6. Rank candidates into `Precise`, `Balanced`, and `Recall`.
7. Show only `Precise` recommendations in chat unless the user asks for more.
8. Mention broader candidates when useful.

## Output Format

```text
Precise recommendations

1. <skill-name>
   Why: <short reason>
   Path: <local path if available>

Broader candidates:
- Balanced: <short list or count>
- Recall: <short list or count>
```

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
