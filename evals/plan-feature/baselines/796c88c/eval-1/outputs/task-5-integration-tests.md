## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests should cover the happy path (SBOM with advisories at various severity levels), the 404 case (nonexistent SBOM), an SBOM with no advisories (all counts zero), and deduplication (same advisory linked multiple times should count once). These tests validate the full request-response cycle against a real PostgreSQL test database.

## Files to Create
- `tests/api/sbom_advisory_summary.rs` — Integration test module with test functions covering all scenarios

## Files to Modify
- `tests/api/mod.rs` or test harness entry point — Register the new test module if tests use a `mod.rs` structure (check existing `tests/api/sbom.rs` and `tests/api/advisory.rs` for the pattern)

## Implementation Notes
- Follow the test pattern in `tests/api/sbom.rs` for: test database setup, SBOM ingestion fixtures, making HTTP requests to the test server, and asserting response status and JSON body.
- Use `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` as per the project's testing convention.
- Deserialize the response body into `AdvisorySeveritySummary` and assert individual field values.
- Test scenarios:
  1. **Happy path**: Ingest an SBOM, link 2 critical + 1 high + 3 medium advisories, assert `{ critical: 2, high: 1, medium: 3, low: 0, total: 6 }`.
  2. **SBOM not found**: Request with a random UUID, expect 404.
  3. **No advisories**: Ingest an SBOM with no linked advisories, expect `{ critical: 0, high: 0, medium: 0, low: 0, total: 0 }`.
  4. **Deduplication**: Link the same advisory to the SBOM twice, assert it is counted only once.
  5. **Cache header**: Assert response includes `Cache-Control` header with `max-age=300`.

## Reuse Candidates
- `tests/api/sbom.rs` — Existing SBOM integration tests showing test setup, fixture ingestion, request construction, and assertion patterns
- `tests/api/advisory.rs` — Advisory test patterns for ingesting advisory fixtures and linking them to SBOMs

## Acceptance Criteria
- [ ] Happy path test passes: correct severity counts returned for an SBOM with mixed advisories
- [ ] 404 test passes: nonexistent SBOM returns 404 status
- [ ] Empty advisories test passes: SBOM with no advisories returns all-zero counts
- [ ] Deduplication test passes: duplicate advisory links do not inflate counts
- [ ] Cache header test passes: response contains `Cache-Control: public, max-age=300`

## Test Requirements
- [ ] All 5 test scenarios described above are implemented and pass

## Verification Commands
- `cargo test --test api sbom_advisory_summary` — all integration tests pass

## Dependencies
- Depends on: Task 3 — Advisory summary endpoint

## Applicable Conventions
- **Testing**: Applies: task creates `tests/api/sbom_advisory_summary.rs` matching the convention's integration tests in `tests/api/` scope.

[sdlc-workflow] Description digest: sha256-md:0903a5be25f068c14f8bdeea51570e97e0298d5b8aebf06218e38d9d0f80da62
