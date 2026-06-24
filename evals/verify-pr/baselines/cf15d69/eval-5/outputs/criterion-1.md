# Criterion 1: `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

## Verdict: PASS

## Reasoning

The service layer in `modules/fundamental/src/purl/service/mod.rs` now calls `p.without_qualifiers()` on each PURL before constructing the `PurlSummary` response object:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

This replaces the previous implementation that called `p.to_string()` directly, which included qualifiers in the output. The `without_qualifiers()` method (referenced in the task's Implementation Notes as existing in `common/src/purl.rs`) strips all query parameters from the PURL, producing a versioned PURL like `pkg:maven/org.apache/commons-lang3@3.12` instead of `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`.

The `test_recommend_purls_basic` test confirms this behavior by asserting `assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12")` -- a versioned PURL without qualifiers.

The endpoint handler in `recommend.rs` still returns `Result<Json<PaginatedResults<PurlSummary>>, AppError>`, so the API contract is preserved while the PURL content is simplified.
