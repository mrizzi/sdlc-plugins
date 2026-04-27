# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Criterion Text
`GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers.

## Evidence from PR Diff

### Service layer change (`modules/fundamental/src/purl/service/mod.rs`)
The recommendation query pipeline was modified to strip qualifiers from each PURL before constructing the response. The previous code serialized the full PURL including qualifiers:
```rust
.map(|p| PurlSummary {
    purl: p.to_string(),
})
```
The new code calls `without_qualifiers()` before serialization:
```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```
This ensures every PURL in the response is versioned but free of qualifier parameters.

### Endpoint layer change (`modules/fundamental/src/purl/endpoints/recommend.rs`)
The `JoinType` import was removed since the qualifier join is no longer needed. The endpoint signature remains unchanged, returning `Result<Json<PaginatedResults<PurlSummary>>, AppError>`.

### Test evidence (`tests/api/purl_recommend.rs`)
The `test_recommend_purls_basic` test now asserts the simplified format:
```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```
The assertion confirms the response contains a versioned PURL (`@3.12`) without any qualifier suffix (no `?`).

### Additional test evidence (`tests/api/purl_simplify.rs`)
The new test file further validates simplified responses across multiple PURL types:
- `test_simplified_purl_no_version` confirms PURLs without version are returned correctly
- `test_simplified_purl_mixed_types` confirms npm PURLs are also stripped of qualifiers (no `vcs_url`)

## Verdict: PASS

The service layer explicitly calls `without_qualifiers()` on every PURL before building the response, and multiple tests confirm versioned PURLs are returned without qualifier parameters.
