## Criterion 2

**Text**: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Verdict**: PASS

**Reasoning**:

The backward compatibility requirement is clearly satisfied. In `modules/fundamental/src/advisory/endpoints/get.rs`, the `SummaryParams` struct defines `threshold` as `Option<String>`:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

When no `threshold` query parameter is provided, `params.threshold` is `None`. The match statement handles this case explicitly:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};
```

The `None` arm returns the original `summary` unchanged, which contains all four severity counts (`critical`, `high`, `medium`, `low`) plus the `total`. This preserves the exact pre-existing behavior of the endpoint. Callers that do not supply the `threshold` parameter will receive the same response as before the change.

The `advisory.rs` service file also shows no changes to the `aggregate_severities` method's return structure, confirming that the underlying data retrieval is unmodified.

The endpoint remains fully backward compatible.
