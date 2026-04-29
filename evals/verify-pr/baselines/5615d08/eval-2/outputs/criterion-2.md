# Criterion 2: No threshold returns all severity counts (backward compatible)

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Verdict: PASS**

## Reasoning

The PR diff shows that when `params.threshold` is `None`, the code falls through to the `None =>` arm of the match expression:

```rust
None => summary,
```

This returns the original `summary` object unchanged, which contains all four severity counts (`critical`, `high`, `medium`, `low`) and the original `total`. This preserves backward compatibility -- requests without a `threshold` parameter receive the same response as before the change.

The `SummaryParams` struct correctly defines `threshold` as `Option<String>`, meaning it is not required:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

This satisfies the backward compatibility criterion.

## Evidence

- `SummaryParams.threshold` is `Option<String>` (optional query parameter)
- The `None` match arm returns `summary` unmodified
- The existing `aggregate_severities` method in `advisory.rs` is unchanged
