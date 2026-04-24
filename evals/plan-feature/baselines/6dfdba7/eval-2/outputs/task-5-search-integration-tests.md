## Repository
trustify-backend

## Description
Add comprehensive integration tests for the improved search functionality, covering full-text search relevance, filter parameters, and performance characteristics. The existing search tests in `tests/api/search.rs` need to be extended to validate the new behavior introduced by the search improvements. These tests serve as the primary verification that the feature requirements are met.

**Assumption (pending clarification):** Without a concrete performance target from the feature description, performance tests will assert that search queries complete within a reasonable time bound (e.g., < 500ms for typical queries against the test dataset). This threshold is a placeholder and should be replaced with the actual SLA once defined.

## Files to Modify
- `tests/api/search.rs` — Add integration tests for full-text search relevance scoring, filter parameter handling, backward compatibility, edge cases, and basic performance assertions

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/search.rs`, `tests/api/sbom.rs`, and `tests/api/advisory.rs` — tests run against a real PostgreSQL test database
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern established in the test conventions
- Test setup should:
  1. Insert test data with known searchable content (e.g., SBOMs with specific names, advisories with known severity levels) so that relevance and filtering can be deterministically verified
  2. Run migrations including the new m0002 migration from Task 1 to ensure tsvector columns and indexes exist
- Test categories to cover:
  - **Relevance**: Insert items with varying degrees of match to a search term; assert that exact matches rank higher than partial matches
  - **Filters**: Test each supported filter type (entity_type, severity, date_range) individually and in combination
  - **Backward compatibility**: Existing search queries without filters should still return valid results
  - **Edge cases**: Empty query string, special characters in search terms, very long queries, no matching results
  - **Performance**: Use `std::time::Instant` to measure query duration and assert it stays under a threshold
- Reference `tests/Cargo.toml` for test dependencies (HTTP client, test database setup utilities)

## Reuse Candidates
- `tests/api/sbom.rs` — Pattern for integration test structure, test data setup, and HTTP assertions
- `tests/api/advisory.rs` — Pattern for integration tests with entity-specific assertions
- `tests/api/search.rs` — Existing search tests to extend (do not break existing tests)

## Acceptance Criteria
- [ ] At least 3 relevance scoring tests verify that more-relevant results rank higher
- [ ] At least 3 filter tests verify correct filtering by entity type, severity, and date range
- [ ] At least 1 backward compatibility test verifies existing search behavior is preserved
- [ ] At least 2 edge case tests cover empty queries and special characters
- [ ] At least 1 performance test asserts search completes within the target time threshold
- [ ] All existing search tests continue to pass
- [ ] All new tests pass in CI against a PostgreSQL test database

## Test Requirements
- [ ] Relevance test: "exact name match" ranks higher than "partial description match"
- [ ] Relevance test: multi-word query matches items containing all words higher than items with only some words
- [ ] Filter test: filtering by entity_type=sbom returns only SBOM results
- [ ] Filter test: filtering by severity=critical returns only critical-severity advisories
- [ ] Filter test: combining entity_type and date_from filters returns correct intersection
- [ ] Edge case test: empty query with filters returns filtered but unranked results
- [ ] Edge case test: search with SQL injection characters does not cause errors
- [ ] Performance test: search query completes within 500ms for test dataset (placeholder threshold)
- [ ] Backward compatibility test: search request without filter parameters returns valid paginated results

## Verification Commands
- `cargo test --test search` — All search integration tests pass
- `cargo test --test search -- --nocapture` — Run with output to inspect performance timing

## Dependencies
- Depends on: Task 4 — Update search endpoint to expose filters and relevance
