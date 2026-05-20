# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Analysis

The implementation correctly handles the case where no threshold parameter is provided. In the `advisory_summary` handler, `params.threshold` is `Option<String>`. When no `threshold` query parameter is provided, the `match` expression falls through to the `None` arm:

```rust
None => summary,
```

This returns the unmodified `summary` directly, preserving the original behavior with all severity counts included.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `SummaryParams` struct declares `threshold: Option<String>`
- The `None` arm of the match returns the original `summary` unchanged
- The function signature and return type are unchanged from the original
