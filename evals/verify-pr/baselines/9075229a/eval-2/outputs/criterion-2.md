# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Analysis

The task requires that omitting the `threshold` query parameter returns all severity counts, preserving backward compatibility with existing clients.

### Code Inspection

In `modules/fundamental/src/advisory/endpoints/get.rs`, the `SummaryParams` struct defines threshold as `Option<String>`:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

The match expression handles the `None` case by returning the unfiltered summary:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};
```

When no `threshold` parameter is provided, `params.threshold` is `None`, and the original `summary` (containing all severity counts) is returned directly via `Ok(Json(filtered))`.

### Evidence

- **File:** `modules/fundamental/src/advisory/endpoints/get.rs`, lines 20-23 (SummaryParams struct) and line 55 (None branch)
- **Behavior:** The `None` arm passes through the complete summary unchanged, preserving all four severity counts (critical, high, medium, low) and the original total
- **Backward compatibility:** Existing clients that do not send a `threshold` parameter will receive the same response structure and values as before this change
