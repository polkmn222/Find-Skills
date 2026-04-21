---
name: find-skills
description: Use in Codex when the user asks to find relevant Codex skills for a project or idea. Read available SKILL.md metadata and return precise recommendations first.
---

# Find Skills For Codex

Use this Codex skill when the user asks to find skills for the current project, a project idea, or a domain such as CRM, games, agents, RAG, frontend, backend, security, analytics, or deployment.

This installed skill is used from a project workspace. For every user request, find or create the current project root's `docs/` directory and write a request-specific checklist as a new numbered file before skill search or implementation. Do not write the checklist inside the installed `.codex/skills/find-skills` folder unless the project root itself is that folder.

## Operating Rules

- Do not ask the user to run Python, shell, or install commands.
- Inspect local files directly. Prefer `rg` or filesystem search when tools are available.
- Use only skill metadata and lightweight project context unless the user asks for deeper analysis.
- Search local installed skills under `.codex/skills/**/SKILL.md` first.
- When the user requests broader discovery, or when local skills do not cover required capabilities, also search external sources such as public GitHub repositories, Git skill collections, official skill/plugin registries, issue/discussion threads, blogs, and SNS/community posts.
- Treat external candidates as `candidate to validate` until their source, license/install path, and skill metadata or equivalent documentation are inspected.
- Distinguish installed local skills from external candidates in chat and in the search index.
- Run the Checklist Gate below for every user request before recommending skills or implementing.
- Ask only the checklist questions that would change the recommendation or implementation.
- If the user asks for quick recommendations or says assumptions are fine, record proposed assumptions in the current request's numbered checklist file and ask for confirmation before proceeding.
- If no usable `SKILL.md` files are found, say what paths were checked and why recommendations are limited.

## Request Intent Rules

Separate skill discovery from implementation.

- If the user only asks to find, recommend, choose, or compare skills, stop at skill recommendations and the search index. Do not install skills or implement artifacts unless the user asks for that next.
- If the user asks to implement, build, create, make, install, scaffold, or otherwise execute work, move beyond recommendation only after the Checklist Gate below.
- If required checklist details are missing, ask concise clarification questions and wait for user answers before recommending skills or implementing.
- If the user says "you decide", "make reasonable assumptions", "no questions", "proceed without questions", "quick prototype", or equivalent, record proposed assumptions in the checklist and ask the user to confirm them before proceeding.
- Any implementation artifact must include an `Assumptions` note covering material choices the agent made because the user confirmed them or specified them directly.

## Checklist Gate

Use this gate for every user request. Most requests leave out details that affect skill routing, implementation scope, or output quality.

Write each request-specific checklist to a new numbered file:

```text
docs/checklist-001.md
docs/checklist-002.md
docs/checklist-003.md
```

This path is relative to the current project root, not relative to the installed `.codex/skills/find-skills` folder. If `docs/` does not exist in the project root, create it. Do not overwrite an existing checklist. Find the next available number by scanning existing `docs/checklist-*.md` files and write the new checklist there. If legacy `docs/checklist.md` exists, preserve it and continue with numbered files. If filesystem writes are unavailable, show the checklist in chat instead.

Fill answers already present in the user request or lightweight project context. Ask the user only for missing items that would affect routing, scope, or output.

When writing checklist questions, put an answer prompt directly under each question so users and agents know where the answer belongs:

```text
1. 앱의 한 문장 목표는 무엇인가?
   ->
```

Use this `->` answer line for every question in the checklist. If an answer is already known, write it after `->` instead of leaving it blank.

Every skill-discovery checklist must include this question before searching:

```text
1. Git에서 Codex 폴더 구성을 잡아주는 skill들도 설치해드릴까요? 예: skill-installer, skill-creator, plugin-creator, agents-md, codex workspace bootstrap 계열.
   ->
```

Ask it even when the user's main request is about another domain, because the answer affects whether to include workspace/bootstrap/setup skills alongside domain skills.

Required for every request:

- goal
- task type: skill recommendation, implementation, installation, review, or other
- context: project, domain, user, or workflow
- must-have requirements
- constraints: technologies, files, APIs, budget, timeline, or policies
- ambiguities: unclear or risky parts
- acceptance criteria

Required for skill recommendations:

- host or agent environment
- search scope: local only, local plus external Git/community/SNS, or external only
- allowed external sources: GitHub/Git repos, official registries, docs sites, issue/discussion threads, blogs, and SNS/community posts
- output depth: precise only, balanced candidates, or broad recall

Required for implementation:

- what to build
- who will use it
- must-have features
- preferred technology stack
- inputs, outputs, or data
- scope: demo, MVP, or production
- external integrations, APIs, or databases
- verification criteria

Do not ask every question mechanically. Ask only the highest-impact missing details. Do not proceed to skill recommendation or implementation until the checklist is written and the required answers are collected or confirmed. If the user requests a fast prototype or explicitly delegates choices, write proposed assumptions in the current numbered checklist file and ask for confirmation before continuing.

## Codex Workflow

1. Understand the project intent from the user's request or from lightweight project files.
2. Run the Checklist Gate above and write the next numbered checklist file in the current project root's `docs/` directory.
3. Search local Codex skill metadata in this repository's skills directory:

```text
.codex/skills/**/SKILL.md
```

4. If local skills do not cover the request, or the checklist requests external discovery, search external Git/community/SNS sources for additional candidate skills or skill-like agent instructions.
5. For local candidates, read candidate metadata, not whole skill bodies by default. Use frontmatter, `name`, `description`, `When to Use`, headings, and routing tables.
6. For external candidates, inspect source title, repository or post URL, summary, install/copy path when available, license or portability notes when available, recency, and any skill metadata or equivalent README instructions. Do not treat social mentions alone as installable skills.
7. Identify candidate clusters before ranking.
8. If enough information is available, group candidates as `Precise`, `Balanced`, and `Recall`.
9. Write the Search Index below.
10. Show `Precise` in the chat. Mention the index path and that broader candidates can be reviewed if useful.

## Candidate Scoring

Scoring is primarily rubric-based. External data can adjust a candidate, but only inside the bounded adjustment rules below. External data must never override hard conflicts, explicit user constraints, or out-of-scope skills.

Score each candidate with this record:

```yaml
skill: <name>
bucket: Precise | Balanced | Recall | Exclude
base_score:
  task_match: 0-35
  routing_fit: 0-25
  actionability: 0-20
  specificity: 0-10
  confidence: 0-10
external_signals:
  prior_success: -5..5
  project_stack_evidence: -5..5
  user_or_repo_preference: -5..5
  recent_usage_pattern: -3..3
  freshness: -3..3
  retrieval_score: -5..5
community_signals:
  recent_mentions: <number>
  practical_examples: <number>
  relevance: 0-1
  credibility: 0-1
  noise_penalty: 0-1
  source_types:
    - github_discussion | github_issue | reddit | hackernews | x | blog | discord | slack
  adjustment: -5..8
external_adjustment: -15..15
final_score: 0-100
hard_conflict: true | false
constraint_status: satisfied | missing_detail | contradicted | out_of_scope
evidence:
  metadata:
    - <frontmatter, description, When to Use, heading, or routing evidence>
  project:
    - <optional local stack/tool/domain evidence>
  external:
    - <optional usage, preference, freshness, retrieval, or community evidence>
bucket_reason: <short audit note>
```

Base score is the sum of:

- `Task Match` (`0-35`): how directly the skill supports the user's task or domain.
- `Routing Fit` (`0-25`): how well the skill matches the named platform, framework, modality, lifecycle phase, or route decision.
- `Actionability` (`0-20`): whether the skill can be used immediately with the available request and project context.
- `Specificity` (`0-10`): whether the skill is the narrow, intended tool instead of a generic parent.
- `Confidence` (`0-10`): strength and clarity of metadata evidence.

Compute adjustments conservatively:

- `external_adjustment = clamp(non_community_adjustments + community_adjustment, -15, 15)`.
- `community_adjustment` is separately bounded to `-5..8`.
- `final_score = clamp(base_score + external_adjustment, 0, 100)`.
- If no external data exists, use `external_adjustment: 0`.
- If `base_score < 70`, external data alone cannot promote the candidate to `Precise`.
- Treat retrieval scores as evidence hints, not ranking authority.

Optional external signals can include prior successful use for similar requests, project-local stack or tool evidence, user or repo preferences, recent usage patterns, skill freshness or maintenance status, and keyword or semantic retrieval scores.

Optional SNS/community signals can support candidate expansion, trend detection, practical usage evidence, confidence adjustment, and freshness signals. They must not directly create a `Precise` recommendation, override hard constraints, override explicit repository metadata, override the base rubric, or promote weak base matches to `Precise`. Candidate skills discovered from community sources still need normal metadata inspection and rubric scoring. If repository metadata does not support the candidate, show it at most as `Recall` or as a `candidate to validate`.

Community signal source types are:

```text
github_discussion, github_issue, reddit, hackernews, x, blog, discord, slack
```

Apply bucket rules after scoring. Bucket assignment must not depend on final score alone:

- `Precise`: `final_score >= 90`, `base_score >= 70`, direct task support, no hard conflict, immediately actionable, and explicit metadata evidence.
- `Balanced`: `final_score >= 75`, relevant and likely useful, but it may require one missing detail or be adjacent/supportive.
- `Recall`: `final_score >= 50`, broadly related and useful for exploration, fallback, or follow-up.
- `Exclude`: `final_score < 50`, hard conflict, contradicted user constraints, or out of scope.

Hard conflicts always force `Exclude`, regardless of final score. Examples include a contradicted user constraint, incompatible platform, excluded language/framework, unsafe or unauthorized route, or a skill whose scope does not cover the task.

Tie-breaking order:

1. Prefer stronger `When to Use` evidence.
2. Prefer a more specific skill over a generic parent skill.
3. Prefer immediately actionable skills.
4. Prefer skills matching the user's named tool, platform, framework, or domain.
5. Demote generic helper skills unless required for execution.

Generic skills should be demoted when a better sibling skill exists. Keep fewer, sharper `Precise` recommendations. Do not pad the list.

## Search Index

When recommendations are produced, create this file under the current project root:

```text
.find-skills/<key>/index.md
```

Choose `<key>` as a short lowercase slug from the user's search intent, for example `web-game`, `crm`, `agent-eval`, or `security-audit`.

The index must make installation easy. Include:

- search key and original user request
- checklist path and required answers used
- confirmed assumptions or clarification answers used
- search scope used, including whether external Git/community/SNS discovery was performed
- ranked candidates with index number, final score from 0-100, bucket, skill name, reason, and local `SKILL.md` path
- for external candidates: source URL, source type, install/copy notes when known, license/portability notes when known, and validation status
- base score breakdown, external adjustment, hard conflict or constraint status, and short evidence notes for auditability
- install notes or copy commands when the candidate path is portable or project-local
- separate sections for `Precise`, `Balanced`, and `Recall`
- excluded candidates only when useful for audit, with the hard conflict or out-of-scope reason

Use the Candidate Scoring rules consistently. The final score is informative, but the bucket must also reflect constraints, actionability, and evidence.

If filesystem writes are unavailable, show the same index content in chat and say that the file could not be written.

## Recommendation Clarification

Before recommending skills, decide whether the request has enough information to make precise recommendations.

Do not use a fixed question list. Instead, infer the most important missing dimensions from:

- the user's request
- project files, if available
- candidate skill metadata: `name`, `description`, `When to Use`, headings, and routing tables

Ask checklist questions only when the answers would change which skills are recommended.

Look for routing signals such as:

- platform, runtime, or integration target choices
- language, framework, or toolchain choices
- implementation vs design vs testing vs deployment needs
- scope or maturity level
- domain, subdomain, modality, or data/source choices

If one missing answer could move a skill between `Precise` and `Balanced`, ask concise checklist questions and do not recommend skills yet.

If the user asks for quick recommendations, says assumptions are fine, or the likely route is obvious from context, record the proposed assumptions in the checklist and ask for confirmation before recommending skills.

## Recommendation Output

Scores are request-relative fit scores, not general skill quality scores. Keep normal chat output concise. Show detailed scoring breakdowns only when useful for routing, audit/debug, or when the user asks for them.

Group candidates by bucket:

- `Precise`
- `Balanced`
- `Recall`
- `Excluded`, only when useful for audit/debug or to explain an important conflict

Each recommended skill should include:

- skill name
- bucket
- final score
- base score
- external adjustment, only when nonzero
- one-line reason
- evidence from `name`, `description`, `When to Use`, routing tables, or lightweight project context
- caveat or `why_not_precise` when relevant

Use this concise chat format:

```text
Precise

1. <skill-name> - <final_score> final / <base_score> base
   Reason: <one-line request-relative fit reason>
   Evidence: <metadata or project-context evidence>
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

If there are no `Precise` matches, say so directly and show the best `Balanced` or `Recall` candidates. If the request is ambiguous, recommend likely candidates when possible and state the missing detail that would improve routing. Excluded candidates should not normally be shown unless they explain an important conflict.

Prefer more recall when the user says they want as many related skills as possible.
