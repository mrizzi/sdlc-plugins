# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Criterion Text
`GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers.

## Evidence from PR Diff

### Service layer change (`modules/fundamental/src/purl/service/mod.rs`)
The recommendation query was modified to strip qualifiers from PURLs before returning them:
```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```
Previously, the code directly serialized the full PURL including qualifiers:
```rust
.map(|p| PurlSummary {
    purl: p.to_string(),
})
```

### Endpoint layer change (`modules/fundamental/src/purl/endpoints/recommend.rs`)
The `JoinType` import for qualifier joins was removed, and the endpoint continues to serve `PaginatedResults<PurlSummary>` through the same route.

### Test evidence (`tests/api/purl_recommend.rs`)
The `test_recommend_purls_basic` test now asserts:
```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```
This confirms the response contains a versioned PURL (`@3.12`) without qualifiers (no `?` suffix).

## Verdict: PASS

The implementation clearly strips qualifiers using `without_qualifiers()` and the test asserts the expected versioned-without-qualifiers format.
