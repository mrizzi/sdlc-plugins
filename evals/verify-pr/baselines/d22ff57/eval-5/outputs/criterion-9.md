# Criterion 9 (Test Requirement 4): Add tests/api/purl_simplify.rs

## Criterion Text
Add new test file `tests/api/purl_simplify.rs` with tests for simplified format edge cases.

## Evidence from PR Diff

### New file `tests/api/purl_simplify.rs`
The file is created as a new file (`new file mode 100644`) with 62 lines containing 3 integration tests:

1. **`test_simplified_purl_no_version`** -- tests the edge case of a PURL without a version qualifier (`pkg:maven/org.apache/commons-io`). Verifies the response returns the PURL as-is without qualifiers.

2. **`test_simplified_purl_mixed_types`** -- tests the edge case of non-Maven PURL types (npm with `@angular/core` and pypi with `requests`). Seeds PURLs with `vcs_url` and `repository_url` qualifiers and verifies they are stripped from the response.

3. **`test_simplified_purl_ordering_preserved`** -- tests that response ordering and pagination are preserved after qualifier removal and deduplication. Seeds 3 versions with `type=jar` qualifiers, requests with `limit=2`, and asserts correct item count, absence of qualifiers, and correct total.

All three test functions include:
- Doc comments (`///`)
- Given-when-then inline comments
- Standard test decorators (`#[test_context(TestContext)]`, `#[tokio::test]`)
- `StatusCode::OK` status assertion
- `PaginatedResults<PurlSummary>` deserialization
- Explicit qualifier-absence assertions

## Verdict: PASS

The new test file `tests/api/purl_simplify.rs` was created with 3 integration tests covering edge cases for the simplified format: no-version PURLs, mixed PURL types, and ordering/pagination preservation.
