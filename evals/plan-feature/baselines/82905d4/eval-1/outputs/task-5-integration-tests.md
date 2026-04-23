## Repository
trustify-backend

## Description
Add comprehensive integration tests for the advisory-summary endpoint that exercise the full request-response cycle against a real PostgreSQL test database. These tests verify the complete behavior of the feature including correct severity aggregation, deduplication, 404 handling, caching headers, and interaction with the ingestion pipeline.

## Files to Create
- `tests/api/sbom_advisory_summary.rs` — Integration test module containing tests for GET /api/v2/sbom/{id}/advisory-summary covering all acceptance scenarios

## Files to Modify
- `tests/Cargo.toml` — Add the new test file to the test suite if explicit test target registration is required

## Implementation Notes
- Follow the integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These tests:
  1. Set up a test database with known fixture data (SBOMs, advisories, sbom_advisory links)
  2. Start the Axum test server
  3. Make HTTP requests via a test client
  4. Assert on response status codes, headers, and JSON body content using `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Use the existing test infrastructure for database setup and teardown. Reference `tests/api/sbom.rs` for how test SBOMs are created and `tests/api/advisory.rs` for how test advisories are ingested.
- For the deduplication test, create a scenario where one advisory is linked to the same SBOM via two different packages (two rows in sbom_advisory referencing the same advisory ID but different package contexts). Verify the advisory is counted once.
- For the cache header test, inspect the response headers for `Cache-Control` containing `max-age=300`.
- For the end-to-end ingestion test, use the IngestorService to ingest an advisory after the initial summary query, then query again to verify counts changed.

## Reuse Candidates
- `tests/api/sbom.rs` — Test setup patterns for creating SBOMs in the test database
- `tests/api/advisory.rs` — Test setup patterns for ingesting advisories and asserting endpoint responses

## Acceptance Criteria
- [ ] Integration test file exists at `tests/api/sbom_advisory_summary.rs`
- [ ] All tests pass against a PostgreSQL test database
- [ ] Tests cover: happy path, missing SBOM 404, zero advisories, multiple severity levels, deduplication, cache headers
- [ ] Tests follow existing project conventions (StatusCode assertions, JSON deserialization)
- [ ] `cargo test --test api` passes with all new tests included

## Test Requirements
- [ ] Test: GET /api/v2/sbom/{id}/advisory-summary returns 200 with correct severity counts for an SBOM with advisories at each severity level (critical=2, high=3, medium=1, low=4, total=10)
- [ ] Test: GET /api/v2/sbom/{id}/advisory-summary returns 404 for a non-existent SBOM ID
- [ ] Test: GET /api/v2/sbom/{id}/advisory-summary returns all-zero counts for an SBOM with no linked advisories
- [ ] Test: Deduplication — an advisory linked to the same SBOM via multiple packages is counted only once
- [ ] Test: Response includes Cache-Control header with max-age=300
- [ ] Test: Response JSON deserializes into AdvisorySeveritySummary struct with correct field values
- [ ] Test: After ingesting a new advisory linked to an SBOM, a subsequent GET returns updated counts

## Verification Commands
- `cargo test --test api sbom_advisory_summary` — all integration tests pass
- `cargo test --test api` — full API test suite passes (no regressions)

## Dependencies
- Depends on: Task 4 — Cache invalidation (all feature components must be in place for end-to-end tests)
