# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Result: PASS

## What was checked

Verified whether the endpoint without a `threshold` query parameter continues to return all four severity counts (critical, high, medium, low), preserving backward compatibility.

## Evidence from the diff

The `SummaryParams` struct defines threshold as `Option<String>`:

```rust
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

The handler's match statement in `get.rs` handles the `None` case by returning the original summary unchanged:

```rust
let filtered = match &params.threshold {
    Some(threshold) => { ... },
    None => summary,
};

Ok(Json(filtered))
```

## Gap identified

None. When no `threshold` parameter is provided, `params.threshold` is `None`, and the unmodified `summary` is returned directly. This preserves the existing behavior and maintains backward compatibility.
