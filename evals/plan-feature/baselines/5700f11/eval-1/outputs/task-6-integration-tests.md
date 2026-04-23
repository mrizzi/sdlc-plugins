## Repository
trustify-backend

## Description
Add comprehensive integration tests for the advisory-summary endpoint covering the full request lifecycle against a real PostgreSQL test database. These tests validate the end-to-end behavior of the endpoint including correct severity counting, 404 handling, threshold filtering, and cache headers.

## Files to Create
- `tests/api/advisory_summary.rs` — Integration test module for the advisory-summary endpoint

## Files to Modify
- `tests/Cargo.toml` — Add the new test file to the test configuration if required by the project's test setup

## Implementation Notes
- Create `tests/api/advisory_summary.rs` following the test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`: set up test fixtures by inserting SBOM and advisory records into the test database, then make HTTP requests and assert on response status, headers, and body.
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern established in the existing integration tests.
- Test fixture setup should:
  1. Insert an SBOM record via the SBOM entity (`entity/src/sbom.rs`)
  2. Insert advisory records at various severity levels via the advisory entity (`entity/src/advisory.rs`)
  3. Link them via the `sbom_advisory` join table entity (`entity/src/sbom_advisory.rs`)
- Test cases to implement:
  - **Happy path**: SBOM with 2 critical, 3 high, 1 medium, 0 low advisories returns correct counts and total=6
  - **Empty advisories**: SBOM with no linked advisories returns all zeros and total=0
  - **404**: Request with non-existent SBOM UUID returns 404
  - **Deduplication**: Insert duplicate advisory links and verify counts reflect unique advisories only
  - **Threshold=critical**: Returns only critical count, others zeroed
  - **Threshold=high**: Returns critical + high counts
  - **Invalid threshold**: Returns 400 Bad Request
  - **Cache header**: Response includes `Cache-Control: max-age=300`
- Parse response body as `AdvisorySeveritySummary` and assert individual field values.

## Reuse Candidates
- `tests/api/sbom.rs` — Test setup patterns, HTTP client configuration, database fixture insertion
- `tests/api/advisory.rs` — Advisory-specific test fixture patterns
- `entity/src/sbom.rs` — SBOM entity for fixture insertion
- `entity/src/advisory.rs` — Advisory entity for fixture insertion
- `entity/src/sbom_advisory.rs` — Join table entity for linking fixtures

## Acceptance Criteria
- [ ] All integration tests pass against the PostgreSQL test database
- [ ] Tests cover happy path, empty state, 404, deduplication, threshold filtering, invalid input, and cache headers
- [ ] Test module follows existing conventions in `tests/api/`

## Test Requirements
- [ ] Happy path test with known severity counts
- [ ] Empty advisories test returns all-zero counts
- [ ] Non-existent SBOM ID returns 404
- [ ] Duplicate advisory links produce deduplicated counts
- [ ] Threshold=critical returns only critical count
- [ ] Threshold=high returns critical and high counts
- [ ] Invalid threshold returns 400
- [ ] Cache-Control header is present with max-age=300

## Verification Commands
- `cargo test --test api -- advisory_summary` — All advisory-summary integration tests pass

## Dependencies
- Depends on: Task 4 — Threshold filter (tests cover threshold functionality)
