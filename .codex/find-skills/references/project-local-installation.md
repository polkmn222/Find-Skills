# Project-Local Installation

For project-specific work, a skill counts as installed only when it exists under the current project root:

```text
.codex/skills/<skill-name>/SKILL.md
```

Home-level or global locations do not count as installed for the current project:

- `~/.codex/skills`
- `~/.agents/skills`
- tool-managed global stores

These paths may be used only as sources, caches, or temporary global installs. If a skill is installed globally first, copy or sync it into the current project's `.codex/skills/` directory before marking it installed.

## Verification

After installing or copying a skill, verify:

```bash
test -f .codex/skills/<skill-name>/SKILL.md
```

If verification fails, do not mark the skill as `present` or installed.

## Installation Status Values

Use these statuses in search indexes when installation is relevant:

- `present`
- `required install`
- `candidate to validate`
- `installation failed`
- `not installed`

## External Packages With Multiple Skills

When one external package installs multiple concrete skills, record:

- original external candidate name
- source URL
- actual project-local skill names installed
- verification evidence for each installed `SKILL.md`

