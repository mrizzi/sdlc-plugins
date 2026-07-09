## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API reference documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint added by feature TC-9001. The feature's Documentation Considerations section specifies doc impact type "Updates" — the endpoint must be added to the existing REST API reference so that API consumers know the endpoint path, parameters, and response shape.

Doc impact type: Updates to existing content.
User purpose: API consumers need to know the endpoint path, parameters, and response shape.
Reference material: Existing SBOM advisory endpoints documentation.

## Acceptance Criteria
- [ ] REST API reference includes the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- [ ] Documentation covers the endpoint path, HTTP method, and path parameters (`id` — SBOM UUID)
- [ ] Documentation covers the optional `?threshold` query parameter with valid values (`critical`, `high`, `medium`, `low`)
- [ ] Documentation includes the response shape: `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Documentation describes the 404 response for non-existent SBOM IDs
- [ ] Documentation describes the 400 response for invalid threshold values
- [ ] Documentation mentions the 5-minute cache behavior
- [ ] Documentation is consistent with the implemented feature behavior

## Test Requirements
- [ ] Verify the documented endpoint path matches the implemented route (`/api/v2/sbom/{id}/advisory-summary`)
- [ ] Verify the documented response shape matches the `SeveritySummary` struct fields
- [ ] Verify the documented query parameters match the implemented threshold filtering behavior

## Dependencies
- Depends on: Task 1 — Add advisory severity summary response model
- Depends on: Task 2 — Add advisory severity aggregation service method
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint
- Depends on: Task 4 — Add cache invalidation for advisory summary
- Depends on: Task 5 — Add threshold query parameter to advisory summary endpoint
- Depends on: Task 6 — Add integration tests for advisory summary endpoint
