# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Acceptance Criterion
`GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers.

## Evidence

### Production Code Changes

In `modules/fundamental/src/purl/service/mod.rs`, the PR removes the qualifier join:
- Removed: `.join(JoinType::LeftJoin, purl::Relation::PurlQualifier.def())`
- Added: `let simplified = p.without_qualifiers();` followed by `PurlSummary { purl: simplified.to_string() }`

This ensures that the service layer strips qualifiers from every PURL before including it in the response.

In `modules/fundamental/src/purl/endpoints/recommend.rs`, the unused `use sea_orm::JoinType;` import was removed, consistent with the qualifier join removal.

### Test Evidence

In `tests/api/purl_recommend.rs`, the `test_recommend_purls_basic` test was updated:
- Seeds PURLs with qualifiers: `"pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar"`
- Asserts the response contains the versioned PURL without qualifiers: `assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12")`

In the new file `tests/api/purl_simplify.rs`:
- `test_simplified_purl_no_version` seeds a versionless PURL and verifies it is returned without qualifiers
- `test_simplified_purl_mixed_types` seeds npm and pypi PURLs with qualifiers and verifies qualifiers are stripped
- `test_simplified_purl_ordering_preserved` seeds 3 versioned PURLs with qualifiers and verifies response ordering without qualifiers

All CI checks pass.

## Verdict: PASS

The production code strips qualifiers using `without_qualifiers()`, and multiple tests confirm the endpoint returns versioned PURLs without qualifiers.
