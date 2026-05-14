# Task 3: Add integration tests for SBOM comparison endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the `GET /api/v2/sbom/compare` endpoint that exercise the full request lifecycle against a real PostgreSQL test database. These tests verify the endpoint correctly computes diffs, handles error cases, and returns proper HTTP status codes and response shapes.

## Files to Create
- `tests/api/sbom_compare.rs` — Integration tests for the comparison endpoint

## Files to Modify
- `tests/Cargo.toml` — Ensure the test crate includes any new dependencies if needed (e.g., `serde_json` for response assertion)

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` — tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` style assertions.
- **Test setup**: Ingest two SBOMs with known, controlled package/advisory data so that the diff results are deterministic. Use the ingestion facilities from `modules/ingestor/src/service/mod.rs` or the existing test helpers.
- **Test cases to implement**:
  1. **Happy path — all diff categories populated**: Ingest two SBOMs where:
     - Left has packages A, B, C; Right has packages B, C, D (A removed, D added)
     - Package B has a version change between left and right
     - Right has a new advisory not present in left
     - Left has an advisory not present in right (resolved)
     - Package C has a different license in left vs right
     - Assert all six arrays in the response contain the expected entries
  2. **Identical SBOMs**: Compare an SBOM with itself (should return 400) or two SBOMs with identical content (all diff arrays empty)
  3. **Missing SBOM ID**: Provide a non-existent UUID for `left` or `right` — expect 404
  4. **Same ID for both**: Set `left` == `right` — expect 400
  5. **Missing query params**: Omit `left` or `right` — expect 400
  6. **Large SBOM diff**: Ingest SBOMs with a larger number of packages (e.g., 100+) and verify the response completes without error
- Deserialize the response body into `SbomComparison` from `modules/fundamental/src/sbom/model/compare.rs` and assert field values.
- Use `serde_json::from_slice` or `resp.json::<SbomComparison>()` for deserialization.

## Acceptance Criteria
- [ ] At least 5 integration test cases covering happy path, error cases, and edge cases
- [ ] Tests pass against the PostgreSQL test database (`cargo test --test api`)
- [ ] Response structure matches the `SbomComparison` model (deserializes without error)
- [ ] HTTP status codes are correct for all error scenarios (400, 404)
- [ ] Tests are deterministic (controlled test data, no reliance on external state)

## Test Requirements
- [ ] Happy path test with all six diff categories populated and verified
- [ ] Test for identical SBOM comparison returning empty diff arrays
- [ ] Test for non-existent SBOM IDs returning 404
- [ ] Test for same left/right ID returning 400
- [ ] Test for missing query parameters returning 400
- [ ] Test for larger SBOM datasets completing successfully

## Dependencies
- Depends on: Task 2 — Implement SBOM comparison service and endpoint
