## Repository
trustify-backend

## Description
Add integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint covering the happy path, 404 for missing SBOM, threshold query parameter filtering, deduplication of advisories, and cache behavior.

## Files to Create
- `tests/api/sbom_advisory_summary.rs` — Integration test module for the advisory-summary endpoint

## Implementation Notes
Follow the integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`. Tests hit a real PostgreSQL test database using the existing test harness. Use the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern from existing tests.

Test cases to implement:

1. **Happy path**: Ingest an SBOM, link several advisories with mixed severities (2 critical, 3 high, 1 medium, 0 low). Call `GET /api/v2/sbom/{id}/advisory-summary`. Assert response is `{ "critical": 2, "high": 3, "medium": 1, "low": 0, "total": 6 }`.

2. **SBOM not found**: Call `GET /api/v2/sbom/{nonexistent-id}/advisory-summary` with a UUID that does not exist. Assert 404 status code.

3. **Empty advisories**: Ingest an SBOM with no linked advisories. Assert response is `{ "critical": 0, "high": 0, "medium": 0, "low": 0, "total": 0 }`.

4. **Deduplication**: Link the same advisory to an SBOM twice (if the data model allows duplicate join rows). Assert the advisory is counted only once.

5. **Threshold filter -- critical**: Call with `?threshold=critical`. Assert only `critical` has a non-zero value and `total` equals `critical`.

6. **Threshold filter -- high**: Call with `?threshold=high`. Assert `critical` and `high` are present, `medium` and `low` are 0.

7. **Invalid threshold**: Call with `?threshold=invalid`. Assert 400 status code.

Register the test module in `tests/api/` following the existing module structure (update `Cargo.toml` if needed or add `mod sbom_advisory_summary;` to the test crate root).

## Reuse Candidates
- `tests/api/sbom.rs` — Test setup patterns for ingesting SBOMs in the test database
- `tests/api/advisory.rs` — Test setup patterns for creating advisories and linking them to SBOMs

## Acceptance Criteria
- [ ] All 7 test cases pass against the test database
- [ ] Tests follow existing test patterns and conventions from `tests/api/sbom.rs`
- [ ] Test module is properly registered and discovered by `cargo test`

## Verification Commands
- `cargo test -p trustify-tests -- sbom_advisory_summary` — All advisory-summary tests pass

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint and register route
- Depends on: Task 4 — Add threshold query parameter filtering
- Depends on: Task 5 — Add caching and cache invalidation on advisory ingestion
