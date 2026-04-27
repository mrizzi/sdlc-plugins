## Repository
trustify-backend

## Description
Add the `GET /api/v2/sbom/{id}/license-report` HTTP endpoint that returns a license compliance report for the specified SBOM. Calls `SbomService::generate_license_report` and returns `LicenseReport` as JSON.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — handler function for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new route

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns `{ "groups": [{ "license": "MIT", "packages": [...], "compliant": true }] }`; 404 if SBOM not found

## Implementation Notes
- Follow the endpoint handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs`: extract path parameters using Axum `Path<Uuid>`, inject `SbomService` via state, return `Result<Json<LicenseReport>, AppError>`.
- Register in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing route registration pattern.
- P95 response time target: < 500ms for SBOMs with up to 1000 packages.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — handler pattern reference
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with correct JSON shape
- [ ] Returns 404 for non-existent SBOM ID
- [ ] Route is registered alongside existing SBOM endpoints

## Test Requirements
- [ ] Integration test: license report returns correct grouped data
- [ ] Integration test: 404 for non-existent SBOM ID
- [ ] Integration test: non-compliant licenses are correctly flagged

## Dependencies
- Depends on: Task 2 — License report model and service
