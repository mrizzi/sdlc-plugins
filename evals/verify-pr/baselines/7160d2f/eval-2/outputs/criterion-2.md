# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Analysis

The handler correctly handles the case when no threshold parameter is provided. The `SummaryParams` struct defines `threshold` as `Option<String>`:

```rust
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

In the filtering logic, the `None` branch returns the original `summary` unmodified:

```rust
None => summary,
```

This preserves backward compatibility -- when no `threshold` query parameter is supplied, the endpoint returns the full, unfiltered `AdvisorySummary` with all four severity counts (critical, high, medium, low) and the original total. Existing API consumers will see no change in behavior.

The criterion is satisfied.
