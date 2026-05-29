## Criterion 2

**Text:** `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**What I checked:** The `None` branch of the `match &params.threshold` block in `modules/fundamental/src/advisory/endpoints/get.rs`.

**Code evidence:**

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};

Ok(Json(filtered))
```

When no `threshold` query parameter is provided, `params.threshold` is `None`, and the original `summary` is returned unmodified. The `SummaryParams` struct uses `Option<String>` for the threshold field:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

This means the parameter is optional, and omitting it preserves backward compatibility by returning all severity counts.

**Verdict: PASS**

The `None` branch correctly returns the unmodified summary, preserving backward compatibility.
