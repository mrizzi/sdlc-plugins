## Repository
trustify-backend

## Description
Add the `GET /api/v2/sbom/compare?left={id1}&right={id2}` HTTP endpoint that returns a structured comparison between two SBOMs. The endpoint calls `SbomService::compare` and returns `SbomComparisonResult` as JSON.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — handler function for `GET /api/v2/sbom/compare`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new comparison route

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: returns structured diff with added/removed packages, version changes, new/resolved vulnerabilities, and license changes. Returns 404 if either SBOM does not exist.

## Implementation Notes
- Follow the endpoint handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for service injection and error handling.
- Extract `left` and `right` query parameters using Axum's `Query<T>` extractor with a `CompareQuery` struct.
- Register in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing route registration pattern.
- P95 response time target: < 1s for SBOMs with up to 2000 packages each.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — handler pattern reference
- `modules/fundamental/src/sbom/endpoints/list.rs` — query parameter extraction pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with correct JSON shape
- [ ] Returns 404 if either SBOM ID does not exist
- [ ] Route is registered alongside existing SBOM endpoints

## Test Requirements
- [ ] Integration test: comparison of two SBOMs returns correct diff
- [ ] Integration test: 404 for non-existent SBOM ID
- [ ] Integration test: comparison of identical SBOMs returns empty diff categories

## Dependencies
- Depends on: Task 2 — SBOM comparison service
