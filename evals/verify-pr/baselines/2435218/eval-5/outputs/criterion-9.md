# Criterion 9: Add new test file `tests/api/purl_simplify.rs` with edge case tests

## Criterion Text
Add new test file `tests/api/purl_simplify.rs` with tests for simplified format edge cases.

## Evidence from PR Diff

### New file `tests/api/purl_simplify.rs`
The PR creates a new test file with 62 lines containing three integration test functions:

**1. `test_simplified_purl_no_version`**
- Tests a PURL without a version component (`pkg:maven/org.apache/commons-io`)
- Seeds the versionless PURL and asserts it is returned without qualifiers
- Validates: `assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-io")`
- Edge case covered: PURLs that have no version qualifier should still work correctly

**2. `test_simplified_purl_mixed_types`**
- Tests non-Maven PURL types: npm (`pkg:npm/%40angular/core@16.0.0?vcs_url=...`) and pypi (`pkg:pypi/requests@2.31.0?repository_url=...`)
- Queries for the npm PURL and asserts qualifiers are stripped
- Validates: `assert_eq!(body.items[0].purl, "pkg:npm/%40angular/core@16.0.0")` and `assert!(!body.items[0].purl.contains("vcs_url"))`
- Edge case covered: qualifier stripping works across different PURL type ecosystems

**3. `test_simplified_purl_ordering_preserved`**
- Seeds 3 versions of a package with qualifiers (`@3.10`, `@3.11`, `@3.12`)
- Requests with `limit=2` and asserts correct pagination
- Validates: `assert_eq!(body.items.len(), 2)`, `assert_eq!(body.total, 3)`, and no `?` in results
- Edge case covered: ordering and pagination remain correct after qualifier removal and dedup

### Structure
The file follows the same test patterns as the existing `tests/api/purl_recommend.rs`:
- Uses `TestContext` from `crate::common`
- Uses `#[test_context(TestContext)]` and `#[tokio::test]` attributes
- Deserializes responses as `PaginatedResults<PurlSummary>`
- Uses `assert_eq!` for status codes and response values

## Verdict: PASS

The new `tests/api/purl_simplify.rs` file was created with three integration tests covering edge cases: versionless PURLs, mixed PURL type ecosystems, and ordering/pagination after simplification. All tests follow the established project test conventions.
