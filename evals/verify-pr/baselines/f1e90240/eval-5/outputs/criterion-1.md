# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Criterion Text
`GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

## Verdict: PASS

## Reasoning

The PR satisfies this criterion through changes in both the service layer and the test layer.

### Service Layer Changes (`modules/fundamental/src/purl/service/mod.rs`)

The service code now strips qualifiers from PURLs before returning them:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

Previously, the PURL was returned as-is via `p.to_string()`, which included all qualifiers. The new code calls `without_qualifiers()` on the PURL model before converting to string. This ensures the response contains versioned PURLs like `pkg:maven/org.apache/commons-lang3@3.12` rather than `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`.

### Endpoint Changes (`modules/fundamental/src/purl/endpoints/recommend.rs`)

The `JoinType` import for `sea_orm::JoinType` was removed, consistent with the qualifier join being removed from the service layer. The endpoint return type remains `Result<Json<PaginatedResults<PurlSummary>>, AppError>`, confirming versioned PURLs are still wrapped in the expected response structure.

### Test Verification (`tests/api/purl_recommend.rs`)

The updated `test_recommend_purls_basic` test seeds PURLs with qualifiers but asserts the response returns versioned PURLs without them:

```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

The assertion explicitly checks that the returned PURL is versioned (`@3.12`) but lacks qualifiers (no `?` suffix). This directly validates the criterion's requirement.

### Additional Validation (`tests/api/purl_simplify.rs`)

The new test file provides further confirmation across different PURL types:
- `test_simplified_purl_no_version`: confirms PURLs without version are returned correctly
- `test_simplified_purl_mixed_types`: confirms npm PURLs with qualifiers are returned without them (e.g., `pkg:npm/%40angular/core@16.0.0` instead of including `?vcs_url=...`)

All evidence confirms the endpoint returns versioned PURLs without qualifiers.
