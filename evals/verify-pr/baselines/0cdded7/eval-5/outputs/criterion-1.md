# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Criterion Text
`GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

## Verdict: PASS

## Reasoning

The PR implements this criterion through changes in two source files:

### Service Layer (`modules/fundamental/src/purl/service/mod.rs`)

The service layer change removes the qualifier join and applies `without_qualifiers()` to each result:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

Previously, PURLs were serialized with `p.to_string()` which included qualifiers. Now `p.without_qualifiers()` is called first, stripping qualifiers before serialization. The task's Implementation Notes confirm that `PackageUrl` builder in `common/src/purl.rs` supports the `without_qualifiers()` method.

### Endpoint Layer (`modules/fundamental/src/purl/endpoints/recommend.rs`)

The endpoint removes the `use sea_orm::JoinType;` import since the qualifier join is no longer needed. The endpoint itself still calls `PurlService::recommend()` and returns `Json<PaginatedResults<PurlSummary>>`, so the response path is unchanged.

### Test Evidence

The `test_recommend_purls_basic` test in `tests/api/purl_recommend.rs` seeds PURLs with qualifiers but asserts the response contains versioned PURLs without qualifiers:

```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This confirms the endpoint returns `pkg:maven/org.apache/commons-lang3@3.12` instead of `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`.

The criterion is satisfied by the code changes.
