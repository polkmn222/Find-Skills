# Find Skills Checklist

This document defines the checklist standard used by `find-skills` before searching for relevant project skills. The checklist is mandatory and user-first: receive, read, or confirm the request-specific checklist before searching skill metadata.

Keep this source document in English. Request-specific checklist files written under `docs/checklist-###.md` may use the user's language.

## Purpose

The checklist is the required basis for the generated search index. It converts a raw request into routing signals that can be matched against skill metadata such as:

- `name`
- `description`
- `When to Use`
- headings
- routing tables
- examples

The completed checklist should capture:

- user goal and searchable vocabulary
- task type and lifecycle stage
- domain, subdomain, modality, platform, runtime, stack, and integrations
- input materials and expected output
- hard constraints, exclusions, and assumptions
- acceptance criteria and verification expectations
- maturity target
- setup, installation, or implementation expectations when relevant
- search scope and evidence location when material

## File Location

For every request, write a numbered checklist under the current project root:

```text
docs/checklist-001.md
docs/checklist-002.md
docs/checklist-003.md
```

Rules:

- Create `docs/` if it does not exist.
- Never overwrite an existing checklist.
- Preserve legacy `docs/checklist.md` if present and continue with numbered files.
- Do not write request checklists inside the installed `.cursor/skills/find-skills` folder unless that folder is the project root.
- If filesystem writes are unavailable, show the same checklist in chat and state that it could not be written.

## Answer Format

Generated checklist files must use request-specific numbered items. Do not use a table as the primary checklist format.

Required item shape:

```text
1. <agent-generated checklist topic or question>: <short guidance, examples, or what should be decided>
   ->
```

Rules:

- Every item must have exactly one immediate `->` answer line.
- In initial drafts, leave `->` blank.
- After user answers or confirms, update the same checklist file by writing the confirmed answer after `->`.
- Do not use placeholders such as `(user to fill)`.
- Do not use status-label prefixes in answers.
- If the item does not apply, state that naturally after `->`.
- Ask the user before searching when a missing answer would materially affect routing, scoring, search scope, implementation route, dependencies, cost, data access, or safety posture.

## Required Topics

Do not use a fixed checklist template. Compose each checklist from the user's request and project context. A normal skill-discovery checklist should usually contain 10-16 request-specific topics.

Capture the dimensions that matter for the request:

- goal and desired artifact
- target audience or user journey when relevant
- task lifecycle: ideation, design, implementation, testing, deployment, monitoring, optimization, migration, review, or incident response
- platform, runtime, framework, provider, language, library, protocol, or integration target
- inputs, examples, references, screenshots, URLs, datasets, files, or existing assets
- required behavior, excluded behavior, and safety constraints
- maturity target, using `production` by default unless the user states another scope
- acceptance criteria and verification commands/checks
- project folder/workspace setup expectations when relevant
- project-local skill installation expectations when relevant
- search scope, using local skills plus external candidates by default
- additional requests to preserve in the index

## Bootstrap And Setup

Every checklist must ask whether project folder/workspace setup should be included when the request may lead to implementation, scaffolding, installation, or a runnable project.

When relevant, ask whether the user wants a Cursor-friendly folder and instruction layout. Mention setup/support skills only when useful, such as:

- `skill-installer`
- `skill-creator`
- `plugin-creator`
- `agents-md`
- project workspace bootstrap skills

If the user only wants recommendations and does not want setup, record that answer and demote setup/bootstrap skills.

## Project-Local Installation Capture

When the request may lead to skill installation, project setup, implementation, scaffolding, or a runnable project, capture the intended skill installation location as a project requirement.

The normal answer should state that project-specific skills must be installed or copied into:

```text
.cursor/skills/<skill-name>/SKILL.md
```

Home-level or global locations such as `~/.cursor/skills`, `~/.agents/skills`, or tool-managed global stores do not count as installed for the current project. They may be recorded only as source locations, caches, or temporary installation locations.

## Search Scope

The default required search scope is:

1. Search installed project-local skills first.
2. Inspect external candidates from sources such as GitHub repositories, community posts, official documentation, registries, issues, or discussions.

Do not ask the user to choose this default scope. Record the default directly in the checklist answer unless the user explicitly requests a narrower or broader scope.

Only ask about search scope when the user signals a constraint such as:

- local-only discovery
- no network
- official-docs-only
- private-source restriction
- no external candidates

When external discovery cannot be performed, record the limitation in the generated checklist and search index.

## Implementation Readiness

For implementation requests, capture readiness and completion criteria when they materially affect the work:

- files, folders, or modules to create or modify
- project-local skill installation required before implementation
- external dependencies, network access, paid services, API keys, or local servers
- minimum verification commands or checks
- unavailable tooling versus failed verification
- required assumptions, disclaimers, acknowledgements, or traceability notes

Do not turn these into generic boilerplate fields. Include them only when relevant to the user's request, acceptance criteria, or likely implementation path.

## Additional Request Notes

Every generated checklist must include a final item for additional requests. Use it for anything the user wants preserved in the final `.find-skills/<key>/index.md`, including:

- output format
- follow-up implementation or installation preferences
- exclusions
- special handling
- notes that do not fit cleanly elsewhere

If there are no additional requests, record that none were provided.

## Clarification Policy

Ask only for checklist items that affect routing, scoring, search scope, installation, implementation, cost, data access, dependencies, or safety.

Ask a clarification when it could change:

- which skill becomes `Precise`
- whether a candidate is excluded
- whether external discovery is allowed
- whether implementation or installation should proceed
- maturity target
- platform, runtime, language, framework, provider, or integration target
- safety, privacy, legal, financial, or destructive-action risk
- acceptance criteria or verification method

Do not ask extra questions when:

- the user already provided a complete checklist
- a missing answer can be recorded as a confirmed assumption without changing top candidates
- the requested output is broad recall and the checklist confirms that scope

## Search Vocabulary Guidance

Translate the user request into searchable vocabulary. Include both user-facing words and implementation-facing English terms when useful.

Consider:

- domain and subdomain
- modality
- platform
- stack
- lifecycle
- capability
- quality attributes
- maturity
- constraints

## Output Quality Bar

A completed checklist should make these easy to answer:

- What is the user trying to accomplish?
- Which words should be searched in skill metadata?
- Which candidate types are in or out of scope?
- Is the search local-only or external as well?
- What assumptions were made?
- What would change the recommendation if clarified?
- Where will the index be written?
- Is the recommendation intended for production or another maturity target?
- Are project-local skill installation and implementation gates relevant?

