# Criterion 9 (Test Requirement): Add new test file `tests/api/purl_simplify.rs`

## Criterion Text
Add new test file `tests/api/purl_simplify.rs` with tests for simplified format edge cases.

## Evidence from PR Diff

### New file (`tests/api/purl_simplify.rs`)
The diff shows a new file created with 62 lines containing three test functions:

1. **`test_simplified_purl_no_version`** -- Tests that PURLs without a version are returned correctly (without qualifiers). Verifies edge case where no version component exists.

2. **`test_simplified_purl_mixed_types`** -- Tests that PURLs of different types (npm, pypi) all have qualifiers stripped. Verifies the simplification works across PURL types, not just Maven.

3. **`test_simplified_purl_ordering_preserved`** -- Tests that response ordering and pagination are preserved after qualifier removal and deduplication. Seeds 3 versions, requests with `limit=2`, and verifies correct count and no qualifiers.

All three tests follow the repository's established integration test patterns:
- Use `#[test_context(TestContext)]` and `#[tokio::test]`
- Use the Given/When/Then comment structure
- Assert with `StatusCode::OK` and deserialize as `PaginatedResults<PurlSummary>`
- Include explicit `!contains('?')` or `!contains("vcs_url")` assertions

## Verdict: PASS

The new test file `tests/api/purl_simplify.rs` was created with three well-structured integration tests covering edge cases of the simplified PURL format.
