# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Criterion Text
`GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers.

## Evidence from PR Diff

### Service layer change (`modules/fundamental/src/purl/service/mod.rs`)
The recommendation mapping was changed to strip qualifiers before constructing the response:
```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```
The base-branch version serialized the full PURL with qualifiers intact:
```rust
.map(|p| PurlSummary {
    purl: p.to_string(),
})
```

### Endpoint layer change (`modules/fundamental/src/purl/endpoints/recommend.rs`)
The `JoinType` import was removed since qualifier joins are no longer performed. The endpoint continues to return `PaginatedResults<PurlSummary>` at the same route path.

### Test evidence (`tests/api/purl_recommend.rs`)
The `test_recommend_purls_basic` test assertion was updated to verify the versioned-only format:
```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```
This confirms the response now contains `@3.12` (versioned) without any `?` query parameters (no qualifiers).

## Verdict: PASS

The `without_qualifiers()` call in the service layer strips qualifier data, and the test asserts the expected versioned-without-qualifiers format.
