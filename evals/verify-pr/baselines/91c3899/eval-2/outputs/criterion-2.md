## Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

### Analysis

The diff in `modules/fundamental/src/advisory/endpoints/get.rs` adds the `threshold` as an `Option<String>` in the `SummaryParams` struct:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

In the handler, when `params.threshold` is `None`, the code falls through to:

```rust
None => summary,
```

This preserves the original behavior -- when no threshold parameter is provided, the full unfiltered `AdvisorySummary` is returned unchanged. The existing aggregation logic in `advisory.rs` is not modified for this case.

## Verdict: PASS

When no threshold parameter is provided, the endpoint returns the complete unfiltered summary, preserving backward compatibility.
