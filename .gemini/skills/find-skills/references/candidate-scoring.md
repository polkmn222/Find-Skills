# Candidate Scoring

Scoring uses broad retrieval plus strict reranking. Preserve a wide candidate set across direct skills, adjacent workflows, support skills, verification skills, setup skills, and external candidates, then rank by checklist coverage, actionability, evidence quality, and constraint fit.

## Score Record

```yaml
skill: <name>
bucket: Precise | Balanced | Recall | Exclude
gates:
  checklist_confirmed: true | false
  no_hard_conflict: true | false
  supports_requested_lifecycle: true | false
  usable_with_available_context: true | false
  explicit_metadata_evidence: true | false
base_score:
  retrieval_breadth: 0-20
  task_match: 0-20
  checklist_coverage: 0-25
  routing_fit: 0-15
  actionability: 0-10
  specificity: 0-5
  evidence_quality: 0-5
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
coverage_notes:
  matched_checklist_items:
    - <item number, topic, or checklist-derived requirement>
  missing_checklist_items:
    - <item number, topic, or checklist-derived requirement>
evidence:
  strong:
    - <direct frontmatter description, When to Use, routing table, or workflow evidence>
  medium:
    - <heading, example, project stack, or file-structure evidence>
  weak:
    - <keyword-only or inferred evidence>
bucket_reason: <short audit note>
```

## Base Score

- `Retrieval Breadth` (`0-20`): useful across direct work, adjacent workflows, modality, platform, verification, setup, future enhancement, or ecosystem relevance.
- `Task Match` (`0-20`): direct support for the user's task or domain.
- `Checklist Coverage` (`0-25`): coverage of checklist-derived requirements.
- `Routing Fit` (`0-15`): match to platform, framework, modality, lifecycle, or route decision.
- `Actionability` (`0-10`): usable now with current context.
- `Specificity` (`0-5`): narrow intended tool versus generic parent.
- `Evidence Quality` (`0-5`): strength and clarity of evidence.

## Gates

- `checklist_confirmed`: candidate must be scored from a completed, user-supplied, or user-confirmed checklist.
- `no_hard_conflict`: required for every non-`Exclude` bucket.
- `supports_requested_lifecycle`: required for `Precise`; otherwise demote when still useful.
- `usable_with_available_context`: required for `Precise`; otherwise demote when still useful.
- `explicit_metadata_evidence`: required for `Precise`; otherwise demote to `Balanced` or `Recall`.

## Evidence Quality

- `Strong`: frontmatter description, explicit `When to Use`, routing table, or workflow instructions directly match.
- `Medium`: headings, examples, project stack evidence, file structure, or adjacent workflow notes.
- `Weak`: skill name, broad keyword overlap, or inferred similarity.

`Precise` candidates must include at least one `Strong` evidence item.

## External Adjustment

Compute conservatively:

- `external_adjustment = clamp(non_community_adjustments + community_adjustment, -15, 15)`
- `community_adjustment` is bounded to `-5..8`
- `final_score = clamp(base_score + external_adjustment, 0, 100)`
- if external discovery is forbidden or unavailable, use `external_adjustment: 0`
- if `base_score < 72`, external data alone cannot promote to `Precise`

## Buckets

- `Precise`: `final_score >= 88`, no hard conflict, strong checklist coverage, high actionability, direct task support, and strong evidence.
- `Balanced`: `final_score >= 72`, no hard conflict, and supports one or more important checklist needs.
- `Recall`: `final_score >= 45`, no hard conflict, and related by adjacent workflow, modality, platform, ecosystem, future enhancement, external candidate value, or fallback use.
- `Exclude`: hard conflict, incompatible platform with no reusable value, unsafe route, out of scope, or `final_score < 45`.

Hard conflicts always force `Exclude`.

## Tie-Breaking

1. Prefer stronger `When to Use` evidence.
2. Prefer more specific skills.
3. Prefer immediately actionable skills.
4. Prefer skills matching named platform, framework, or domain.
5. Keep adjacent/generic helper skills in `Recall` when useful later.

