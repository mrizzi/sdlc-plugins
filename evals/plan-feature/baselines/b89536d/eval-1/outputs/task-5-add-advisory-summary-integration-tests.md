# Task 5 -- Add integration tests for advisory summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint covering the full range of scenarios: successful aggregation with multiple severities, deduplication of advisories, 404 for nonexistent SBOMs, threshold filtering, empty advisory sets, and cache header verification. These tests exercise the complete request-response cycle against a real PostgreSQL test database, following the existing integration test patterns.

## Files to Create
- `tests/api/advisory_summary.rs` -- integration test file for the advisory summary endpoint with test cases covering all acceptance criteria

## Files to Modify
- `tests/Cargo.toml` -- add the new test file to the test configuration if needed (check if the test harness auto-discovers files)

## Implementation Notes
- Follow the integration test pattern established in `tests/api/sbom.rs` and `tests/api/advisory.rs` for test setup, HTTP client usage, and assertion style
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code assertions, consistent with existing tests
- Tests run against a real PostgreSQL test database -- set up test data by creating SBOMs and advisories with known severities via the ingestion pipeline or direct entity insertion
- Test cases to implement:
  1. **Happy path**: SBOM with advisories at each severity level (critical, high, medium, low) -- verify correct counts and total
  2. **Deduplication**: Same advisory linked to an SBOM through multiple paths -- verify it is counted only once
  3. **Not found**: Request advisory summary for a nonexistent SBOM ID -- verify 404 response
  4. **Empty advisories**: SBOM with no linked advisories -- verify all-zero counts with 200 status
  5. **Threshold filter**: Use `?threshold=high` and verify only critical and high counts are returned
  6. **Cache headers**: Verify response includes `Cache-Control: max-age=300`
- Deserialize response body as `AdvisorySeveritySummary` and assert field values individually for clear test failure messages

## Reuse Candidates
- `tests/api/sbom.rs` -- existing SBOM integration tests to follow for test setup patterns, fixture data creation, and assertion style
- `tests/api/advisory.rs` -- existing advisory integration tests for reference on advisory entity creation in test context
- `common/src/model/paginated.rs::PaginatedResults` -- not directly needed here but shows the response wrapper pattern used by other endpoints

## Acceptance Criteria
- [ ] All integration tests pass against the PostgreSQL test database
- [ ] Tests cover: happy path, deduplication, 404, empty advisories, threshold filter, cache headers
- [ ] Tests follow existing patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`
- [ ] Test failure messages clearly indicate which assertion failed and with what values

## Test Requirements
- [ ] Integration test: SBOM with mixed-severity advisories returns correct per-severity counts and total
- [ ] Integration test: duplicate advisory-SBOM links result in deduplicated counts
- [ ] Integration test: nonexistent SBOM ID returns 404
- [ ] Integration test: SBOM with no advisories returns `{ critical: 0, high: 0, medium: 0, low: 0, total: 0 }`
- [ ] Integration test: threshold=high returns only critical and high counts (medium and low are zero or absent)
- [ ] Integration test: response contains Cache-Control header with max-age=300

## Verification Commands
- `cargo test --test api -- advisory_summary` -- runs all advisory summary integration tests, expects all to pass

## Dependencies
- Depends on: Task 3 -- Add GET /api/v2/sbom/{id}/advisory-summary endpoint
- Depends on: Task 4 -- Add cache invalidation for advisory summary on advisory ingestion
