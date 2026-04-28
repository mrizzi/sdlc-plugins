## Repository
trustify-backend

## Description
Update the API documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Document the endpoint path, HTTP method, path parameters, optional query parameters, response shape, error responses, and caching behavior. This ensures API consumers and the frontend dashboard team can discover and integrate with the new endpoint.

## Files to Modify
- `README.md` — add the new endpoint to the API endpoints section if one exists

## Documentation Updates
- `README.md` — add entry for `GET /api/v2/sbom/{id}/advisory-summary` with: path parameter (`id`: SBOM identifier), optional query parameter (`threshold`: severity level filter, values: critical/high/medium/low), response shape (`{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`), 404 behavior for missing SBOMs, and 5-minute cache TTL note

## Implementation Notes
- Review `README.md` for an existing API reference section. If the README documents existing endpoints like `GET /api/v2/sbom/{id}` or `GET /api/v2/advisory`, follow the same documentation format and style for the new endpoint.
- Include the following details in the documentation:
  - Endpoint: `GET /api/v2/sbom/{id}/advisory-summary`
  - Path parameter: `id` (SBOM identifier, required)
  - Query parameter: `threshold` (optional, values: `critical`, `high`, `medium`, `low`) — filters counts to only include severity levels at or above the specified threshold
  - Success response (200): `{ "critical": 2, "high": 5, "medium": 3, "low": 1, "total": 11 }`
  - Error response (404): returned when the SBOM ID does not exist
  - Caching: responses are cached for 5 minutes; cache is invalidated when new advisories are linked to the SBOM
- Per constraints doc section 4: this task updates public API documentation, so the Documentation Updates section is required.

## Acceptance Criteria
- [ ] The new endpoint is documented in the project's API reference
- [ ] Documentation includes endpoint path, HTTP method, path parameter, query parameter, response shape, error responses, and caching behavior
- [ ] Documentation style matches existing endpoint documentation in the same file

## Test Requirements
- [ ] Manual review: verify the documentation accurately describes the endpoint's behavior as implemented in Tasks 1-5

## Dependencies
- Depends on: Task 3 — Advisory summary REST endpoint
