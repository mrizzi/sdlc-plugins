## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add integration tests for the SBOM comparison endpoint. These tests hit the actual endpoint with a real PostgreSQL test database, validating the full request-response cycle including query parameter parsing, service invocation, and JSON serialization. This ensures the comparison feature works end-to-end on the backend.

## Files to Create
- `tests/api/sbom_compare.rs` — Integration tests for `GET /api/v2/sbom/compare`

## Files to Modify
- `tests/api/mod.rs` — Add `mod sbom_compare;` if a module file exists, or ensure the new test file is discovered by the test harness

## Implementation Notes
Follow the existing integration test pattern in `tests/api/sbom.rs`. Tests should:

1. Set up test data: ingest two SBOMs with known package sets using the ingestion service or test fixtures.
2. Make HTTP requests to `GET /api/v2/sbom/compare?left={id1}&right={id2}`.
3. Assert on response status codes and JSON body structure.

Test cases:
- **Happy path**: Two SBOMs with overlapping but different packages. Assert that the response contains correct entries in each of the six diff categories.
- **Identical SBOMs**: Compare an SBOM with itself (use two different IDs pointing to identical content). Assert all diff lists are empty.
- **Missing query params**: Omit `left` or `right`. Assert 400 status.
- **Same ID**: Pass the same UUID for both `left` and `right`. Assert 400 status.
- **Non-existent SBOM**: Pass a UUID that does not correspond to any SBOM. Assert 404 status.
- **Version change direction**: Set up SBOMs where a package goes from 1.0.0 to 2.0.0 (upgrade) and another goes from 3.0.0 to 1.0.0 (downgrade). Assert direction field is correct.
- **Vulnerability diff**: Set up SBOMs where one has an advisory link and the other does not. Assert correct categorization as new or resolved vulnerability.

Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern per project conventions.

## Reuse Candidates
- `tests/api/sbom.rs` — Reference for test setup, fixtures, and assertion patterns
- `tests/api/advisory.rs` — Reference for advisory-related test data setup

## Acceptance Criteria
- [ ] All integration tests pass against the PostgreSQL test database
- [ ] Happy path test verifies all six diff categories in the response
- [ ] Error cases (missing params, same ID, non-existent SBOM) return correct status codes
- [ ] Tests are discoverable by `cargo test`

## Test Requirements
- [ ] Happy path with overlapping packages returns correct diff
- [ ] Identical SBOMs return empty diff lists
- [ ] Missing query parameters return 400
- [ ] Same left and right ID returns 400
- [ ] Non-existent SBOM ID returns 404
- [ ] Version change direction (upgrade/downgrade) is correct
- [ ] Vulnerability new/resolved categorization is correct

## Dependencies
- Depends on: Task 4 — Backend comparison endpoint
