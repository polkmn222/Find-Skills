# Recommendation Output

Scores are request-relative fit scores, not general skill quality scores.

Keep normal chat output concise. Show detailed scoring only when useful for routing, audit, debugging, or when the user asks.

## Buckets

Group candidates by:

- `Precise`
- `Balanced`
- `Recall`
- `Excluded`, only when useful for audit or conflict explanation

## Recommended Chat Format

```text
Precise

1. <skill-name> - <final_score> final / <base_score> base
   Reason: <one-line request-relative fit reason>
   Coverage: <matched checklist topics>
   Evidence: <strong evidence item>
   External: <external_adjustment, only if nonzero>

Balanced

1. <skill-name> - <final_score> final / <base_score> base
   Reason: <one-line reason>
   Coverage: <matched and missing checklist topics when useful>
   Evidence: <strong or medium evidence item>
   Why not precise: <missing detail, adjacent scope, weaker actionability, or lower evidence>

Recall

1. <skill-name> - <final_score> final / <base_score> base
   Reason: <fallback, exploration, or follow-up value>
   Breadth: <adjacent workflow, modality, platform, ecosystem, or future enhancement relevance>
   Coverage: <broadly related checklist topics>
   Evidence: <medium or weak evidence item>
   Caveat: <why broad or conditional>

Excluded

1. <skill-name> - Excluded
   Reason: <hard conflict, contradicted constraint, or out-of-scope explanation>
```

If there are no `Precise` matches, say so directly and show the best `Balanced` or `Recall` candidates.

Prefer more recall when the user asks for as many related skills as possible.

