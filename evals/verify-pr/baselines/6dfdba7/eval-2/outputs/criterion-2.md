# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Result: PASS

## Reasoning

When no `threshold` query parameter is provided, the `params.threshold` field is `None`. The code handles this case in the `None` branch of the match expression:

```rust
None => summary,
```

This returns the original `AdvisorySummary` unchanged, preserving the existing response shape and values. The SBOM fetch, severity aggregation, and response serialization all remain unchanged from the pre-PR behavior for requests without a threshold parameter.

The one caveat is that criterion 5 requires a `threshold_applied` boolean field in the response, which is entirely absent. If that field were required for backward compatibility (returning `false` when no threshold is specified), the response shape would technically differ from the pre-PR version. However, criterion 2 specifically asks about returning "all severity counts," which is satisfied. The missing `threshold_applied` field is tracked separately under criterion 5.

The backward compatibility of the existing fields and their values is preserved.
