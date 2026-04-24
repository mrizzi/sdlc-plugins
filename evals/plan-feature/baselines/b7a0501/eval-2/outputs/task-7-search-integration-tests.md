# Task 7 — Add Comprehensive Integration Tests for Search Improvements

## Repository
trustify-backend

## Description
Add comprehensive integration tests covering the full search improvement feature: full-text search relevance ranking, filter parameters, combined filters, edge cases, and performance characteristics. This ensures all the changes from Tasks 1-6 work together correctly end-to-end against a real PostgreSQL test database.

## Files to Modify
- `tests/api/search.rs` — Add new integration test cases for full-text search, relevance ranking, filtering, combined filters, and edge cases

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/search.rs` — inspect the file to understand the test setup, database seeding, and assertion patterns before adding tests
- Also inspect `tests/api/sbom.rs` and `tests/api/advisory.rs` for additional test pattern references (e.g., how test data is seeded, how responses are parsed)
- Tests should use the `assert_eq!(resp.status(), StatusCode::OK)` pattern as documented in the repository conventions
- Seed test data that includes:
  - Multiple SBOMs with different names/descriptions for testing relevance ranking
  - Multiple advisories with different severity levels for testing severity filter
  - Multiple packages with different licenses for testing license filter
  - Items with different timestamps for testing date range filter
- Test categories:
  1. **Relevance ranking**: search for a term that appears in multiple items with different relevance, verify ordering
  2. **Entity type filter**: verify each entity type filter returns only the correct type
  3. **Severity filter**: verify severity filter on advisories
  4. **Date range filter**: verify date range filtering
  5. **License filter**: verify license filtering on packages
  6. **Combined filters**: verify multiple filters work together
  7. **Edge cases**: empty query, no results, special characters in search query, very long search query
  8. **Backward compatibility**: existing search behavior without filters still works
- Per constraints doc section 5.9: prefer parameterized tests when multiple test cases exercise the same behavior with different inputs
- Per constraints doc section 5.11: add a doc comment to every test function
- Per constraints doc section 5.12: add given-when-then inline comments to non-trivial test functions

## Reuse Candidates
- `tests/api/search.rs` — Existing search integration tests for pattern reference
- `tests/api/sbom.rs` — SBOM endpoint integration tests for setup and assertion patterns
- `tests/api/advisory.rs` — Advisory endpoint integration tests for setup patterns

## Acceptance Criteria
- [ ] Integration tests cover full-text search relevance ranking
- [ ] Integration tests cover each individual filter (entity_type, severity, date_range, license)
- [ ] Integration tests cover combined filter scenarios
- [ ] Integration tests cover edge cases (empty query, no results, special characters)
- [ ] Integration tests verify backward compatibility (search without filters)
- [ ] All new tests pass against a real PostgreSQL test database
- [ ] Test functions have doc comments
- [ ] Non-trivial tests have given-when-then inline comments

## Test Requirements
- [ ] All test cases listed in the test categories above are implemented and pass
- [ ] Tests are parameterized where appropriate (e.g., testing each entity type filter could use parameterized inputs)

## Verification Commands
- `cargo test --test api -- search` — all search integration tests pass

## Dependencies
- Depends on: Task 5 — Add Filter Parameters to Search Endpoint
- Depends on: Task 6 — Add Caching for Search Results
