---
name: find-skills
description: Use in Cursor when the user asks to find relevant Codex skills for a project or idea. Read available SKILL.md metadata and return precise recommendations first.
---

# Find Skills For Cursor

Use this Cursor skill when the user asks to find skills for the current project, a project idea, or a domain such as CRM, games, agents, RAG, frontend, backend, security, analytics, or deployment.

This installed skill must work by itself after being copied to `.cursor/skills/find-skills`. Do not depend on the repository root, README files, or sibling host folders being present.

## Operating Rules

- Do not ask the user to run Python, shell, or install commands.
- Inspect local files directly. Prefer `rg` or filesystem search when tools are available.
- Use only skill metadata and lightweight project context unless the user asks for deeper analysis.
- If the request is broad, ask only the clarification questions that would change the recommendation.
- If the user asks for quick recommendations or says assumptions are fine, proceed and state assumptions.
- If no usable `SKILL.md` files are found, say what paths were checked and why recommendations are limited.

## Cursor Workflow

1. Understand the project intent from the user's request or from lightweight project files.
2. Search available skill metadata first. Start with likely installed locations, then project-local locations:

```text
~/.cursor/skills/**/SKILL.md
<project-root>/.cursor/skills/**/SKILL.md
```

3. Read candidate metadata, not whole skill bodies by default. Use frontmatter, `name`, `description`, `When to Use`, headings, and routing tables.
4. Identify candidate clusters before ranking.
5. Run the Clarification Gate below.
6. If enough information is available, group candidates as `Precise`, `Balanced`, and `Recall`.
7. Write the Search Index below.
8. Show `Precise` in the chat. Mention the index path and that broader candidates can be reviewed if useful.

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
- assumptions or clarification answers used
- ranked candidates with index number, final score from 0-100, bucket, skill name, reason, and local `SKILL.md` path
- base score breakdown, external adjustment, hard conflict or constraint status, and short evidence notes for auditability
- install notes or copy commands when the candidate path is portable or project-local
- separate sections for `Precise`, `Balanced`, and `Recall`
- excluded candidates only when useful for audit, with the hard conflict or out-of-scope reason

Use the Candidate Scoring rules consistently. The final score is informative, but the bucket must also reflect constraints, actionability, and evidence.

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
