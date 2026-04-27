# Criterion 2

**Text**: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Evidence from diff**:

The diff in `get.rs` shows:

```rust
let filtered = match &params.threshold {
    // ...
    None => summary,
};

Ok(Json(filtered))
```

When `params.threshold` is `None` (no threshold query parameter provided), the code returns the original `summary` unchanged. The `SummaryParams` struct uses `Option<String>` for the threshold field, so omitting it defaults to `None`.

This preserves backward compatibility -- the response is identical to the previous behavior before the change.

**Verdict**: PASS
