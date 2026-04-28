# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Analysis

The PR diff handles the case where no threshold parameter is provided via a `None` match arm:

```rust
None => summary,
```

When `params.threshold` is `None` (no query parameter provided), the unfiltered `summary` is returned directly. This preserves the original behavior of returning all severity counts without any modification.

The `SummaryParams` struct defines `threshold` as `Option<String>`, which means the query parameter is optional and defaults to `None` when not provided.

## Evidence

From the diff:
```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

And in the handler:
```rust
let filtered = match &params.threshold {
    Some(threshold) => { /* filtering logic */ }
    None => summary,
};
```

The `None` branch returns the summary unchanged, preserving backward compatibility.
