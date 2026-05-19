# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Criterion Text
`GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

## Verdict: PASS

## Reasoning

The PR diff shows changes in two locations that implement this requirement:

### Service layer (`modules/fundamental/src/purl/service/mod.rs`)

The recommendation query was modified to strip qualifiers from PURLs before returning them. The key change is:

```rust
// Before (base branch):
.map(|p| PurlSummary {
    purl: p.to_string(),
})

// After (PR branch):
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

The `without_qualifiers()` method is called on each PURL entity before serializing it to a string, which strips all qualifier key-value pairs from the output. The task's Implementation Notes confirmed that `PackageUrl` builder in `common/src/purl.rs` supports the `without_qualifiers()` method.

### Endpoint layer (`modules/fundamental/src/purl/endpoints/recommend.rs`)

The `JoinType` import for `sea_orm::JoinType` was removed since the qualifier join is no longer needed. The endpoint handler itself continues to call the same `PurlService::recommend()` method, which now returns simplified PURLs.

### Test confirmation

The updated `test_recommend_purls_basic` test in `tests/api/purl_recommend.rs` explicitly asserts the new behavior:

```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This confirms that the endpoint returns a versioned PURL (`@3.12`) without any qualifier string (no `?repository_url=...&type=jar`).

The new test file `tests/api/purl_simplify.rs` also contains `test_simplified_purl_no_version` and `test_simplified_purl_mixed_types` which further confirm that PURLs of various types are returned without qualifiers.

The code changes directly implement the requirement: the service layer strips qualifiers using `without_qualifiers()`, and tests confirm the endpoint returns versioned PURLs without qualifier parameters.
