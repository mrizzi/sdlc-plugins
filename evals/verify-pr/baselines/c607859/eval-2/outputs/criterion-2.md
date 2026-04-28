# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Reasoning

The PR diff adds the `threshold` parameter as `Option<String>` in the `SummaryParams` struct:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

In the handler, when no threshold is provided, the code follows the `None` branch of the match:

```rust
None => summary,
```

This returns the unmodified `summary` directly, preserving all severity counts as they were before the change. The `Query(params): Query<SummaryParams>` extractor with `Option<String>` means that when no `threshold` query parameter is present, `params.threshold` is `None`, and the original summary (with all four severity levels) is returned unchanged.

This is backward compatible -- the endpoint behaves identically to its previous behavior when no threshold parameter is supplied.

**Conclusion:** This criterion IS satisfied. The backward compatibility is correctly preserved.
