# Find Skills

Markdown-only skill discovery guide for agents.

Use this repository when you want an agent to read available `SKILL.md` files and recommend relevant Codex skills for a project or idea. Python execution is not required.

Repository URL:

```text
https://github.com/polkmn222/Find-Skills.git
```

## Choose Your Tool

Use the same repository, but install or invoke it in the way your host expects.

| Tool | Install | First Use |
| --- | --- | --- |
| Claude Code | `tmp=$(mktemp -d) && git clone https://github.com/polkmn222/Find-Skills.git "$tmp/find-skills" && mkdir -p .claude/skills && cp -R "$tmp/find-skills/.claude/skills/find-skills" .claude/skills/` | `Use find-skills to find skills for a CRM web project` |
| Cursor | `tmp=$(mktemp -d) && git clone https://github.com/polkmn222/Find-Skills.git "$tmp/find-skills" && mkdir -p .cursor/skills && cp -R "$tmp/find-skills/.cursor/skills/find-skills" .cursor/skills/` | `@find-skills find skills for a CRM web project` |
| Gemini CLI | `tmp=$(mktemp -d) && git clone https://github.com/polkmn222/Find-Skills.git "$tmp/find-skills" && mkdir -p .gemini/skills && cp -R "$tmp/find-skills/.gemini/skills/find-skills" .gemini/skills/` | `Use find-skills to find skills for a small game project` |
| Codex CLI | `tmp=$(mktemp -d) && git clone https://github.com/polkmn222/Find-Skills.git "$tmp/find-skills" && mkdir -p .codex/skills && cp -R "$tmp/find-skills/.codex/skills/find-skills" .codex/skills/` | `Use find-skills to find skills for an agent project` |

Install all hosts at once:

```bash
tmp=$(mktemp -d) && \
git clone https://github.com/polkmn222/Find-Skills.git "$tmp/find-skills" && \
mkdir -p .codex/skills .claude/skills .cursor/skills .gemini/skills && \
cp -R "$tmp/find-skills/.codex/skills/find-skills" .codex/skills/ && \
cp -R "$tmp/find-skills/.claude/skills/find-skills" .claude/skills/ && \
cp -R "$tmp/find-skills/.cursor/skills/find-skills" .cursor/skills/ && \
cp -R "$tmp/find-skills/.gemini/skills/find-skills" .gemini/skills/
```

## Direct Use Without Installing

Point your agent at this folder:

```text
Read `/path/to/Find-Skills/SKILL.md` and find appropriate Codex skills for this project.
```

For a project idea:

```text
Read `/path/to/Find-Skills/SKILL.md` and find Codex skills for: small game project.
```

If this folder is copied into a project as `find-skills/`, ask:

```text
Read `find-skills/SKILL.md` and find appropriate Codex skills for this project.
```

The agent should read:

```text
SKILL.md
```

## Installed Files

Each host gets a self-contained skill:

```text
.codex/skills/find-skills/SKILL.md
.claude/skills/find-skills/SKILL.md
.cursor/skills/find-skills/SKILL.md
.gemini/skills/find-skills/SKILL.md
```

Each skills folder also includes a README:

```text
.codex/skills/README.md
.claude/skills/README.md
.cursor/skills/README.md
.gemini/skills/README.md
```

Each installed skill is self-contained. Installing only one host folder is enough.

The root copy is also available at:

```text
SKILL.md
```

## What The Agent Does

The agent should:

1. Read `SKILL.md`.
2. Understand the project or idea.
3. Search available `SKILL.md` files.
4. Rank candidates into `Precise`, `Balanced`, and `Recall`.
5. Show only `Precise` recommendations in chat unless the user asks for more.
6. Mention broader candidates when useful.

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

## Optional Reports

If the agent writes files, use key-based folders:

```text
.find-skills/<key>/reports/precise.md
.find-skills/<key>/reports/balanced.md
.find-skills/<key>/reports/recall.md
```

`.find-skills/` is disposable. It can be deleted and recreated.

## No Runtime Required

This repository is Markdown-only. There is no required Python, Node, or shell runtime.

The expected behavior is for the agent to read `SKILL.md` and perform discovery directly from skill metadata.
