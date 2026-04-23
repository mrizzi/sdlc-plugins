## Repository
trustify-backend

## Description
Add comprehensive integration tests for the SBOM comparison endpoint, covering happy-path scenarios with realistic SBOM data, edge cases (empty SBOMs, identical SBOMs, SBOMs with large package counts), and error cases. These tests validate the full request-response cycle against a real PostgreSQL test database, following the project's existing integration test patterns.

## Files to Modify
- `tests/api/sbom.rs` — Optionally add a cross-reference or import if the test module structure requires it (depending on how the test binary discovers modules)

## Files to Create
- `tests/api/sbom_compare.rs` — Integration tests for `GET /api/v2/sbom/compare`

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` — tests hit a real PostgreSQL test database, use `assert_eq!(resp.status(), StatusCode::OK)` for status assertions, and deserialize response bodies for content assertions.
- Set up test data by ingesting two SBOMs with known package and advisory differences using the `IngestorService` from `modules/ingestor/src/service/mod.rs`. The SBOM ingestion logic in `modules/ingestor/src/graph/sbom/mod.rs` handles parsing and storing SBOMs with linked packages.
- Test scenarios should cover:
  - Two SBOMs with distinct packages to verify added/removed detection
  - Two SBOMs sharing packages at different versions to verify version change detection with upgrade/downgrade direction
  - Two SBOMs with different advisory associations to verify new/resolved vulnerability detection
  - Two SBOMs where packages have different licenses to verify license change detection
  - Edge case: comparing an SBOM to itself (expect empty diff)
  - Edge case: comparing SBOMs where one has no packages
- Deserialize the response body into the `SbomComparison` struct from `modules/fundamental/src/sbom/model/comparison.rs` and assert on the counts and contents of each diff section.
- Use the existing `tests/Cargo.toml` for test dependencies and configuration.

## Reuse Candidates
- `tests/api/sbom.rs` — Existing SBOM integration test patterns for test setup, assertion style, and server bootstrapping
- `tests/api/advisory.rs` — Advisory integration tests showing how to set up advisory test data
- `modules/ingestor/src/service/mod.rs::IngestorService` — For ingesting test SBOM data
- `modules/fundamental/src/sbom/model/comparison.rs::SbomComparison` — Response struct to deserialize and assert on

## Acceptance Criteria
- [ ] All integration tests pass against the PostgreSQL test database
- [ ] Tests cover all six diff sections: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, license changes
- [ ] Tests verify correct HTTP status codes for success (200), missing parameters (400), and not-found (404)
- [ ] Tests verify the response body content matches expected diff results for known test data
- [ ] Edge case test confirms comparing an SBOM to itself returns empty diff sections

## Test Requirements
- [ ] Integration test: two SBOMs with non-overlapping packages produce correct added/removed lists
- [ ] Integration test: two SBOMs with shared packages at different versions produce correct version changes with direction
- [ ] Integration test: two SBOMs with different advisories produce correct new/resolved vulnerabilities
- [ ] Integration test: two SBOMs with license differences produce correct license changes
- [ ] Integration test: comparing an SBOM to itself returns all empty sections
- [ ] Integration test: comparing with a non-existent SBOM ID returns 404
- [ ] Integration test: missing query parameters return 400

## Verification Commands
- `cargo test --test api sbom_compare` — All comparison integration tests pass

## Dependencies
- Depends on: Task 2 — Backend comparison endpoint
