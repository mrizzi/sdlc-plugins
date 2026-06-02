# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Criterion Text
`GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

## Verdict: PASS

## Reasoning

The PR diff shows changes in two layers that work together to satisfy this criterion:

### Service Layer (`modules/fundamental/src/purl/service/mod.rs`)

The service layer change removes the qualifier join and applies `without_qualifiers()` to strip qualifiers from the PURL before serialization:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

Previously, the code mapped directly to `p.to_string()` which included qualifiers. Now it calls `p.without_qualifiers()` first, which (per the task's implementation notes) is a method on the `PackageUrl` builder in `common/src/purl.rs` that constructs PURLs without qualifiers. The resulting `.to_string()` produces a versioned PURL like `pkg:maven/org.apache/commons-lang3@3.12` instead of `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`.

### Endpoint Layer (`modules/fundamental/src/purl/endpoints/recommend.rs`)

The endpoint removes the `use sea_orm::JoinType;` import (no longer needed since the qualifier join was removed) and the handler continues to return the result via `PurlService::recommend()`. The return type remains `Json<PaginatedResults<PurlSummary>>`, confirming that the endpoint still returns the expected structure with the simplified PURLs.

### Test Evidence

The updated `test_recommend_purls_basic` test seeds PURLs with qualifiers but asserts the response contains versioned PURLs without qualifiers:

```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This directly confirms the criterion is met. The new `test_simplified_purl_no_version` in `purl_simplify.rs` also verifies PURLs without versions are returned correctly without qualifiers.

### Conclusion

The code changes in the service layer strip qualifiers using `without_qualifiers()`, and the tests assert the expected simplified format. This criterion is satisfied.
