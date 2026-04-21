# Scoring Guardrail Examples

These examples are lightweight regression cases for the Markdown-first scoring workflow. They use mock signal values only; no external service, crawler, or database is required.

The machine-readable companion file is `examples/scoring-cases.yaml`. Keep it aligned with these scenarios so future scripts or tests can consume the same expected outcomes.

## External Signals

### Strong Candidate Boosted

Request: "Find skills for a React accessibility audit."

Candidate: `accessibility-compliance-accessibility-audit`

```yaml
base_score:
  task_match: 34
  routing_fit: 23
  actionability: 19
  specificity: 9
  confidence: 9
external_signals:
  project_stack_evidence: 4
  prior_success: 3
external_adjustment: 7
final_score: 100
hard_conflict: false
constraint_status: satisfied
bucket: Precise
bucket_reason: Direct accessibility audit support, explicit metadata evidence, actionable immediately, and bounded external signals only reinforce a strong rubric score.
```

Expected: `Precise`.

### Weak Match Not Promoted To Precise

Request: "Find skills for a PostHog product analytics event plan."

Candidate: `ai-product`

```yaml
base_score:
  task_match: 18
  routing_fit: 14
  actionability: 12
  specificity: 4
  confidence: 7
external_signals:
  prior_success: 5
  recent_usage_pattern: 3
  retrieval_score: 5
external_adjustment: 13
final_score: 68
hard_conflict: false
constraint_status: missing_detail
bucket: Recall
bucket_reason: External data helps discovery, but base score is below 70 and the skill is generic compared with analytics-specific siblings.
```

Expected: `Recall`, not `Precise`.

### Hard Conflict Overrides External Signal

Request: "Find Python backend deployment skills. Do not recommend frontend-only skills."

Candidate: `angular`

```yaml
base_score:
  task_match: 10
  routing_fit: 0
  actionability: 5
  specificity: 5
  confidence: 8
external_signals:
  prior_success: 5
  retrieval_score: 5
  freshness: 3
community_signals:
  adjustment: 8
external_adjustment: 15
final_score: 43
hard_conflict: true
constraint_status: contradicted
bucket: Exclude
bucket_reason: The user explicitly excluded frontend-only routes, so the hard conflict forces exclusion despite positive external signals.
```

Expected: `Exclude`.

### Better Sibling Demotes Generic Skill

Request: "Find skills for implementing Algolia search in React."

Candidate A: `algolia-search`

```yaml
base_score:
  task_match: 35
  routing_fit: 24
  actionability: 19
  specificity: 10
  confidence: 9
external_adjustment: 2
final_score: 99
hard_conflict: false
constraint_status: satisfied
bucket: Precise
bucket_reason: Named platform match, specific implementation support, and explicit metadata evidence.
```

Candidate B: `ai-engineer`

```yaml
base_score:
  task_match: 19
  routing_fit: 12
  actionability: 12
  specificity: 3
  confidence: 7
external_adjustment: 6
final_score: 59
hard_conflict: false
constraint_status: satisfied
bucket: Recall
bucket_reason: Broad engineering relevance, but a more specific sibling directly covers Algolia search.
```

Expected: `algolia-search` is `Precise`; generic helper skill is demoted to `Recall`.

## Community Signals

### Community Boosts Strong Candidate

Request: "Find skills for evaluating AI agents."

Candidate: `agent-evaluation`

```yaml
base_score:
  task_match: 34
  routing_fit: 23
  actionability: 18
  specificity: 9
  confidence: 9
community_signals:
  recent_mentions: 14
  practical_examples: 6
  relevance: 0.9
  credibility: 0.8
  noise_penalty: 0.1
  source_types:
    - github_issue
    - blog
  adjustment: 6
external_adjustment: 6
final_score: 99
hard_conflict: false
constraint_status: satisfied
bucket: Precise
bucket_reason: Community evidence reinforces an already strong metadata-backed match.
```

Expected: `Precise`.

### Community Does Not Promote Weak Match

Request: "Find skills for Stripe billing integration."

Candidate: `analytics-product`

```yaml
base_score:
  task_match: 14
  routing_fit: 8
  actionability: 8
  specificity: 3
  confidence: 6
community_signals:
  recent_mentions: 30
  practical_examples: 2
  relevance: 0.4
  credibility: 0.5
  noise_penalty: 0.2
  source_types:
    - reddit
    - x
  adjustment: 5
external_adjustment: 5
final_score: 44
hard_conflict: false
constraint_status: out_of_scope
bucket: Exclude
bucket_reason: Mentions do not overcome weak task match or missing repository metadata support.
```

Expected: `Exclude`, not `Precise`.

### Noisy Promotional Mentions Penalized

Request: "Find skills for Kubernetes compliance hardening."

Candidate: `aegisops-ai`

```yaml
base_score:
  task_match: 28
  routing_fit: 21
  actionability: 16
  specificity: 8
  confidence: 8
community_signals:
  recent_mentions: 50
  practical_examples: 1
  relevance: 0.6
  credibility: 0.3
  noise_penalty: 0.8
  source_types:
    - x
    - reddit
  adjustment: -4
external_adjustment: -4
final_score: 77
hard_conflict: false
constraint_status: missing_detail
bucket: Balanced
bucket_reason: The base match is useful, but noisy promotional mentions reduce confidence and leave one missing detail.
```

Expected: `Balanced`.

### Trending Unsupported Candidate To Validate

Request: "Find skills for a new community-hyped vector database integration."

Candidate: `community-vector-db-x`

```yaml
base_score:
  task_match: 20
  routing_fit: 12
  actionability: 7
  specificity: 5
  confidence: 2
community_signals:
  recent_mentions: 120
  practical_examples: 8
  relevance: 0.8
  credibility: 0.6
  noise_penalty: 0.2
  source_types:
    - github_discussion
    - hackernews
    - blog
  adjustment: 8
external_adjustment: 8
final_score: 54
hard_conflict: false
constraint_status: missing_detail
bucket: Recall
bucket_reason: Community trend suggests a candidate to validate, but repository metadata is weak or absent, so it cannot be Precise.
```

Expected: `Recall` or label as `candidate to validate`.
