# Criterion 1: `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

## Verdict: PASS

## Reasoning

The PR modifies the service layer in `modules/fundamental/src/purl/service/mod.rs` to strip qualifiers from PURLs before building the response. Specifically, the code now calls `p.without_qualifiers()` on each PURL result before constructing the `PurlSummary`:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

This ensures that the `GET /api/v2/purl/recommend` endpoint returns versioned PURLs without qualifiers.

The test `test_recommend_purls_basic` in `tests/api/purl_recommend.rs` directly verifies this behavior by asserting:

```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This assertion confirms the response contains a versioned PURL (`@3.12`) without any qualifier parameters.

Additionally, the endpoint handler in `modules/fundamental/src/purl/endpoints/recommend.rs` removes the `use sea_orm::JoinType` import, which was only needed for the qualifier join that has been removed from the service layer. The handler's return type remains `Result<Json<PaginatedResults<PurlSummary>>, AppError>`, and it continues to call `PurlService::recommend()` which now returns simplified PURLs.

The new test file `tests/api/purl_simplify.rs` provides additional coverage with edge cases (no version PURLs, mixed PURL types) all asserting the same behavior -- versioned PURLs without qualifiers.

## Evidence

- `modules/fundamental/src/purl/service/mod.rs`: `let simplified = p.without_qualifiers();` followed by `PurlSummary { purl: simplified.to_string() }`
- `tests/api/purl_recommend.rs`: `assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");`
- `tests/api/purl_simplify.rs`: Multiple tests asserting simplified PURLs
- CI: All checks pass
