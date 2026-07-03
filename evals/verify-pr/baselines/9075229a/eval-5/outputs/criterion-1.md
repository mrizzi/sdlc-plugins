# Criterion 1: `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

## Verdict: PASS

## Reasoning

The PR modifies the service layer (`modules/fundamental/src/purl/service/mod.rs`) to strip qualifiers from PURLs before returning them. Specifically, the code now calls `p.without_qualifiers()` on each PURL result before converting to string:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

This ensures that the endpoint returns versioned PURLs without qualifiers (e.g., `pkg:maven/org.apache/commons-lang3@3.12` instead of `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`).

The endpoint handler in `modules/fundamental/src/purl/endpoints/recommend.rs` still calls the same `recommend` method on `PurlService`, and the function signature still returns `Result<Json<PaginatedResults<PurlSummary>>, AppError>`, confirming the endpoint path and response type are unchanged.

The qualifier join (`JoinType::LeftJoin, purl::Relation::PurlQualifier.def()`) has been removed from the query since qualifier data is no longer needed for the response, which is consistent with the change.

The test `test_recommend_purls_basic` confirms this behavior by asserting:
```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This assertion verifies the endpoint returns a versioned PURL without qualifiers for the same seed data that previously returned fully qualified PURLs.
