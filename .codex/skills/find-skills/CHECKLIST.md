# Find Skills Checklist

This document defines the general checklist standard used by `find-skills` before searching for relevant Codex skills. The checklist is mandatory and user-first: receive, read, or confirm the request-specific checklist before searching skill metadata.

Keep this source document in English. The request-specific checklist files written under `docs/checklist-###.md` may use the user's language, so the generated checklist is easy for the user to read and maintain.

Do not hardcode topic-specific examples into this document. The agent should generate request-specific examples, search terms, assumptions, and checklist wording from the user's actual request and the local project context.

## Purpose

The checklist is a search-indexing instrument and the required basis for the generated search index. A raw "find skills" request is not enough to search. The checklist turns the request into routing signals that can be matched against skill metadata such as:

- `name`
- `description`
- `When to Use`
- headings
- routing tables
- examples inside candidate skill files

The completed checklist should make skill discovery more precise by capturing:

- the user's goal in searchable language
- the task type and lifecycle stage
- domain and subdomain
- platform, runtime, framework, modality, and integrations
- input materials and expected output
- hard constraints, exclusions, and recorded assumptions
- acceptance criteria
- maturity target: production, MVP, demo, prototype, experiment, learning, or unresolved
- search scope and evidence location

The agent must review the completed checklist before writing `.find-skills/<key>/index.md`. The index should be traceable to the checklist's captured answers, recorded assumptions, constraints, maturity target, and acceptance criteria.

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
- Do not write request checklists inside the installed `.codex/skills/find-skills` folder unless that folder is the project root.
- If filesystem writes are unavailable, show the same checklist in chat and state that it could not be written.

## Language Policy

Write this source file in English.

Write generated `docs/checklist-###.md` files in the user's language when the user has clearly used a non-English language. If the user mixes languages, choose the language that makes the checklist easiest for the user to review. Keep technical identifiers, skill names, file paths, commands, framework names, and metadata field names unchanged.

The search terms inside the generated checklist may include multiple languages when useful. Prefer including both the user's natural-language terms and implementation-facing English terms when that improves skill retrieval.

## User-First Gate

Standard workflow for every skill search:

1. Write the request-specific checklist under `docs/checklist-###.md`.
2. Ask the user to review, fill, or confirm the checklist.
3. Search local installed skills first, then search external Git/community/SNS sources when the checklist allows or requires external discovery.
4. Write `.find-skills/<key>/index.md` from the completed checklist.
5. Summarize precise recommendations in chat and point to the index for broader candidates.

Before searching skill metadata, obtain a complete request-specific checklist for the current request. If the user provides or points to a checklist, read it first and use it as the source of truth. If no checklist is provided, draft the request-specific checklist questions and ask the user to answer or confirm them before searching. High-impact fields are details that could change the recommended skill, bucket, search scope, implementation route, dependencies, cost, data access, or safety posture.

If the request is already specific enough, or the user asks for quick recommendations / says assumptions are fine, still get checklist confirmation before searching. The checklist should use plain answer text after `->`; do not prefix answers with source, assumption, missing-detail, or applicability status labels. When a detail is missing, put the missing-detail guidance on the numbered item line and leave the `->` line as the user's answer slot. When a detail is inferred from the user's request, the inferred answer may be written after `->` in natural language.

The checklist must be completed, user-supplied or user-confirmed, and reviewed before writing a search index. If the user changes the goal after an index was created, update or create the checklist first, then rewrite the index from the updated checklist.

## Maturity Target

Every checklist must capture the intended maturity level. Use `production` as the default when the user does not explicitly ask for MVP, demo, prototype, experiment, or learning scope.

Production-oriented checklists should capture acceptance criteria that affect real-world use, such as:

- reliability and failure handling
- maintainability and code quality
- performance and scalability
- accessibility and inclusive UX
- security, privacy, and data safety
- testing and verification expectations
- deployment, release, rollback, and operational readiness
- cost, dependency, and compliance constraints when relevant

MVP/demo/prototype scopes are allowed only when user-provided or clearly requested. When using a non-production maturity target, record it explicitly and keep the ranking scoped to that target. Do not assume "small" means "demo"; a small project can still be production-intended.

## Answer Format

Generated checklist files must be easy for the user and future agents to scan. Use a complete but focused Markdown checklist made of request-specific topics or questions generated by the agent from the user's request and lightweight project context. Do not use a table as the primary checklist format because every item must include a visible user-answer line.

Each generated checklist item must include both the prompt or label and concise guidance on the numbered item line. Put the user's answer slot directly below it on a line that starts with `->`. For initial checklist drafts, leave the answer slot blank after `->` so the user can fill it. After the user answers or confirms the checklist, update the same checklist file by writing the confirmed answer after `->`. If the agent is inferring an answer, keep the inference brief and natural without status-label prefixes and use it only after user confirmation.

Required item shape:

```text
1. <agent-generated checklist topic or question>: <short guidance, examples, or what should be decided>
   ->
```

Rules for `->` answer lines:

- Every checklist topic or question must have exactly one immediate `->` answer line.
- The numbered item line should carry the question, explanation, examples, or missing-detail guidance.
- The `->` line is the answer slot. Keep it visually distinct from the question text.
- In initial drafts, leave `->` blank even when the numbered item line contains request-derived context.
- After the user fills or confirms the checklist, write the confirmed answer after `->`.
- Do not write placeholders such as `(사용자가 작성)` or `(user to fill)`.
- If the agent is inferring an answer, state it in natural language after `->` only after the user confirms that inference.
- If the answer is missing but does not block routing, keep the missing-detail explanation on the numbered item line and leave the `->` line as the user's answer slot.
- If the item does not apply, state that it does not apply in natural language, without a status prefix.
- Do not use status-label prefixes. Write the answer itself in natural language.
- If the missing answer would materially affect routing, ask the user before searching skill metadata, writing recommendations, or writing the search index.
- Additional notes may be added under the `->` line, but they must not replace the `->` answer.

## Required Bootstrap Question

Every skill-discovery checklist must ask whether project folder/workspace setup should be included when the request may lead to implementation, scaffolding, installation, or a runnable project. Keep this question project-scoped, not agent-process scoped: ask whether the user wants the agent to set up the folder/file structure needed for the requested project.

Use request-appropriate wording in the user's language. When relevant, mention that this may include skills that help create or maintain a Codex-friendly folder and instruction structure, such as `skill-installer`, `skill-creator`, `plugin-creator`, `agents-md`, or project workspace bootstrap skills.

If the user only wants recommendations and does not want setup, record that answer in the checklist and demote setup/bootstrap skills. If the answer could affect recommendations, ask the user before searching.

## Checklist Composition

Do not use a fixed field list. The agent must compose each request-specific checklist from the user's actual request, the project context, and the task intent. The generated topics should represent what the agent believes matters for routing and ranking this specific request.

A normal skill-discovery checklist should usually contain 10-16 request-specific topics. Use fewer only when the request is genuinely narrow and all routing signals are obvious. Use more when the request is broad, cross-stack, safety-sensitive, production-bound, or asks for external discovery. A checklist with fewer than 10 topics should be treated as suspect unless the document explains why additional routing dimensions would not affect ranking.

For skill recommendation requests, the generated checklist should usually capture enough information to determine the user's project goal, domain, lifecycle stage, search scope, search terms, candidate inclusion and exclusion criteria, output depth, recommendation index path, recorded assumptions that affect ranking, whether external discovery is allowed, and whether project folder/workspace setup is part of the likely next step.

The generated checklist should contain only the user's project, product, task, domain, constraints, and acceptance criteria. Do not include agent workflow steps or process reminders in `docs/checklist-###.md`; those belong in this `CHECKLIST.md` workflow or in the search index.

For implementation requests, the generated checklist should usually capture what will be created or changed, who it is for, required and excluded behavior, preferred or existing stack, integrations or data access, scope level, verification criteria, folder/file setup expectations, examples or references the user wants the agent to follow, and material assumptions that must be recorded in the artifact.

For creative, product, UI, game, website, or app requests, ask whether the user has examples, reference projects, screenshots, URLs, gameplay clips, style references, or existing assets. These references materially improve skill routing and later implementation quality.

For review requests, the generated checklist should usually capture the review target, review lens, whether fixes may be applied, severity standard, and evidence sources.

These are coverage expectations, not required headings. The generated checklist should use the user's language when appropriate, but it must preserve the required `->` answer-line format for every item.

## Search Vocabulary Guidance

When filling the generated checklist, translate the user request into searchable vocabulary. Include both user-facing words and implementation-facing terms.

Consider these dimensions when relevant:

- Domain: industry, product area, problem area, user workflow.
- Modality: text, image, audio, video, 2D, 3D, voice, data, UI, CLI, API.
- Platform: browser, mobile, desktop, server, cloud, local workspace, CI/CD.
- Stack: language, framework, database, provider, library, protocol.
- Lifecycle: ideation, design, implementation, testing, deployment, monitoring, optimization, migration, incident response.
- Capability: generation, retrieval, automation, orchestration, validation, analytics, scraping, transformation, security hardening.
- Quality attributes: accessibility, performance, reliability, scalability, maintainability, privacy, compliance, cost.
- Maturity: production, production-ready, release-ready, MVP, demo, prototype, proof of concept, experiment, learning.
- Constraints: offline, no network, local only, official docs only, no install, no external API, low budget, production safe.

Do not store a fixed example mapping in this file. For each request, the agent should derive the relevant mapping from the user's words and the project context.

## Clarification Policy

Do not ask every checklist question mechanically. Ask only for checklist items that affect routing, scoring, search scope, or whether work can proceed. However, every skill search must still start from a user-provided or user-confirmed checklist.

Ask a clarification when it could change:

- which skill becomes `Precise`
- whether a candidate is excluded
- whether external discovery is allowed
- whether implementation or installation should proceed
- whether the target is production versus MVP/demo/prototype when that would change candidate ranking
- platform, runtime, language, framework, provider, or integration target
- safety, privacy, legal, financial, or destructive-action risk
- acceptance criteria or verification method

Do not ask extra clarification questions when:

- the user already provided a complete checklist
- a missing answer can be recorded as an explicitly confirmed assumption without changing the top candidates
- the requested output is explicitly broad recall and the checklist confirms that scope

For recommendation-only requests, proceed only after checklist confirmation. For implementation or installation, confirm assumptions that materially affect files, dependencies, cost, data access, or irreversible actions.

## Candidate Scoring Signals

The completed checklist should feed candidate scoring. Use it to identify evidence for these dimensions:

- Task match: the skill directly supports the user's goal, domain, or lifecycle stage.
- Routing fit: the skill matches platform, framework, modality, provider, or route table.
- Actionability: the skill can be used now with available context and constraints.
- Specificity: the skill is the narrowest useful match, not a generic parent when a better child skill exists.
- Confidence: metadata evidence is explicit and not inferred from weak keyword overlap.
- Production fit: when the maturity target is production, the skill supports release-quality concerns such as testing, performance, accessibility, security, maintainability, deployment, or operations.

Demote candidates when:

- they only match a broad word but not the user's actual task
- they require a platform or framework not requested
- they are implementation-heavy but the user only asked for recommendations
- they are setup/bootstrap skills and the user did not ask for setup
- they create external dependency, cost, or safety risk not accepted by the checklist
- they are prototype/demo-oriented while the checklist maturity target is production

## Generated Examples

Do not keep static examples in this source document.

When an example would help, generate it inside the request-specific `docs/checklist-###.md` file from the user's actual topic. The generated example should be short, clearly marked as request-specific, and should not replace the required fields.

## Output Quality Bar

A good completed checklist should make these easy to answer:

- What is the user trying to accomplish?
- Which words should be searched in skill metadata?
- Which candidate types are in scope or out of scope?
- Is the search local-only or external as well?
- What assumptions or inferences were made?
- What would change the recommendation if clarified?
- Where will the recommendation index be written?
- Is the recommendation intended for production or for MVP/demo/prototype work?
- Which checklist fields materially drive candidate ranking?

If those answers are not visible, the checklist is too thin.
