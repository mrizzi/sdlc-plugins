# Criterion 2: Backward compatibility without threshold parameter

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Verdict:** PASS

## Analysis

The PR diff adds the threshold parameter as `Option<String>` in the `SummaryParams` struct:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

In the handler, when `params.threshold` is `None`, the code falls through to the `None =>` branch:

```rust
None => summary,
```

This returns the original `summary` object unmodified, which contains all severity counts as they were before the change.

The `SummaryParams` struct is added as a new `Query` extractor parameter to the handler. Since all fields are `Option`, a request without any query parameters will deserialize successfully with `threshold: None`, preserving the original behavior.

**Conclusion:** When no threshold parameter is provided, the endpoint returns all severity counts unchanged. Backward compatibility is preserved. This criterion IS met.
