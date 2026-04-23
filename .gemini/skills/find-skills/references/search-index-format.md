# Search Index Format

When recommendations are produced, create this file under the current project root:

```text
.find-skills/<key>/index.md
```

Choose `<key>` as a short lowercase slug representing the checklist-derived search topic.

The index must be traceable to the completed checklist and must make installation easy.

## Required Content

Include:

- search key and original user request
- checklist path, maturity target, and required answers used
- confirmed assumptions or clarification answers
- checklist-derived search terms, constraints, acceptance criteria, and exclusions
- search scope used, including external discovery status
- external discovery details:
  - sources inspected
  - query terms used
  - candidates found
  - candidates rejected
  - explicit reason external discovery was skipped or limited, if applicable
- bootstrap skill availability in current project's `.gemini/skills/`
- ranked candidates with:
  - index number
  - final score
  - bucket
  - skill name
  - reason
  - project-local `SKILL.md` path when installed
- external candidate metadata:
  - source URL
  - source type
  - install/copy notes
  - license or portability notes when known
  - validation status
- project-local installation status after installation is requested
- verification evidence for installed skills
- gate results
- base score breakdown
- external adjustment
- hard conflict or constraint status
- matched and missing checklist items
- evidence quality notes
- project-local install notes or copy commands
- external candidate expansion notes when one package installs multiple skills
- separate `Precise`, `Balanced`, and `Recall` sections
- excluded candidates only when useful for audit

## Bootstrap Skills

Always report project-local status for:

- `skill-installer`
- `skill-creator`
- `agents-md`
- `agent-orchestrator`
- `antigravity-skill-orchestrator`
- `acceptance-orchestrator`
- `plugin-creator`

## Installation Status

Use:

- `present`
- `required install`
- `candidate to validate`
- `installation failed`
- `not installed`

Global/home-level installs do not count as `present` unless copied or synced into the current project's `.gemini/skills/`.

## Filesystem Fallback

If filesystem writes are unavailable, show the same index content in chat and state that the file could not be written.

