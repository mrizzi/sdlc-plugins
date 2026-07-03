## Repository
trustify-backend

## Target Branch
main

## Description
Write integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint covering the primary scenarios: valid SBOM with advisories at mixed severity levels, non-existent SBOM returning 404, threshold filtering, deduplication of advisory IDs, empty SBOM, and cache header validation. These tests follow the existing integration test patterns in `tests/api/` and run against a real PostgreSQL test database.

additional_fields: { "labels": ["ai-generated-jira"], "priority": "Major", "fixVersions": "RHTPA 1.5.0" }

## Files to Create
- `tests/api/sbom_advisory_summary.rs` -- integration tests for the advisory-summary endpoint

## Files to Modify
- `tests/Cargo.toml` -- add any necessary test dependencies if not already present

## Implementation Notes
Follow the integration test patterns established in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern.

Each test should:
1. Set up test data: create an SBOM via ingestion, create advisories with known severity levels, link them via the `sbom_advisory` join table
2. Call `GET /api/v2/sbom/{id}/advisory-summary` via the test HTTP client
3. Assert response status and body

Test cases to implement:
- `test_advisory_summary_returns_counts`: Create an SBOM with 2 critical, 3 high, 1 medium, 0 low advisories. Assert response is `{ "critical": 2, "high": 3, "medium": 1, "low": 0, "total": 6 }`.
- `test_advisory_summary_not_found`: Request advisory-summary for a non-existent SBOM UUID. Assert 404 response.
- `test_advisory_summary_threshold_filter`: Create an SBOM with mixed severities, request with `?threshold=high`. Assert only critical and high counts are returned.
- `test_advisory_summary_deduplication`: Link the same advisory to an SBOM twice (if possible via different paths). Assert it is counted only once.
- `test_advisory_summary_empty`: Create an SBOM with no linked advisories. Assert all counts are zero and total is zero.
- `test_advisory_summary_cache_header`: Assert the response includes `Cache-Control: max-age=300`.

Use the existing test utilities and setup patterns from `tests/api/sbom.rs` for SBOM creation and from `tests/api/advisory.rs` for advisory creation.

Per CONVENTIONS.md: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task creates `tests/api/sbom_advisory_summary.rs` matching the convention's `.rs` test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` -- SBOM test setup patterns (creating test SBOMs, making HTTP requests)
- `tests/api/advisory.rs` -- advisory test setup patterns (creating test advisories with severity levels)

## Acceptance Criteria
- [ ] All six integration test cases pass against the PostgreSQL test database
- [ ] Tests cover: valid counts, 404, threshold filter, deduplication, empty SBOM, cache header
- [ ] Tests follow existing patterns in `tests/api/` and do not introduce new test infrastructure

## Test Requirements
- [ ] `test_advisory_summary_returns_counts` -- validates correct severity counts for a known dataset
- [ ] `test_advisory_summary_not_found` -- validates 404 for non-existent SBOM
- [ ] `test_advisory_summary_threshold_filter` -- validates threshold query param filtering
- [ ] `test_advisory_summary_deduplication` -- validates advisory deduplication
- [ ] `test_advisory_summary_empty` -- validates zero counts for SBOM with no advisories
- [ ] `test_advisory_summary_cache_header` -- validates Cache-Control header

## Verification Commands
- `cargo test -p trustify-tests sbom_advisory_summary` -- all tests pass

## Dependencies
- Depends on: Task 2 -- Implement advisory-summary REST endpoint with caching
- Depends on: Task 3 -- Add cache invalidation to advisory ingestion pipeline
