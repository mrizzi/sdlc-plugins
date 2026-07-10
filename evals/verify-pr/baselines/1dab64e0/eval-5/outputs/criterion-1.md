# Criterion 1: `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

## Verdict: PASS

## Analysis

### What the criterion requires

The endpoint must return PURLs that include the version component but exclude qualifiers. For example, the response should contain `pkg:maven/org.apache/commons-lang3@3.12` rather than `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`.

### Evidence from the PR diff

#### Service layer change (`modules/fundamental/src/purl/service/mod.rs`)

The service layer now calls `without_qualifiers()` on each PURL before constructing the response summary:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

Previously, the code used `p.to_string()` directly, which included qualifiers. The new code explicitly strips qualifiers before serialization, producing versioned-only PURLs.

#### Endpoint layer change (`modules/fundamental/src/purl/endpoints/recommend.rs`)

The `JoinType` import was removed, indicating that the qualifier join is no longer needed at the endpoint level. The endpoint still returns `Result<Json<PaginatedResults<PurlSummary>>, AppError>`, confirming the response type is unchanged.

#### Test validation (`tests/api/purl_recommend.rs`)

The `test_recommend_purls_basic` test now asserts:

```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This confirms the response contains versioned PURLs without qualifiers. The test seeds data with full qualifiers (`?repository_url=...&type=jar`) and verifies the response strips them.

#### Additional test validation (`tests/api/purl_simplify.rs`)

The new `test_simplified_purl_no_version` test confirms that PURLs without a version component are also returned without qualifiers. The `test_simplified_purl_mixed_types` test confirms qualifier stripping works across different PURL types (npm, pypi), asserting:

```rust
assert_eq!(body.items[0].purl, "pkg:npm/%40angular/core@16.0.0");
assert!(!body.items[0].purl.contains("vcs_url"));
```

### Conclusion

The service layer strips qualifiers using `without_qualifiers()`, the endpoint returns the simplified PURLs, and multiple tests validate the expected output format. The criterion is satisfied.
