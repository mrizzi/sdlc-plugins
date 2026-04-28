# Task 6 — Update API documentation for advisory summary endpoint

## Repository
trustify-backend

## Description
Update the REST API documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Document the endpoint path, HTTP method, path parameters, optional query parameters, response shape, error responses, and caching behavior. This enables API consumers and the frontend dashboard team to integrate with the new endpoint.

## Files to Modify
- `README.md` — add the new endpoint to the API reference section if endpoints are documented there

## Implementation Notes
- Locate the existing API documentation by checking `README.md` and any files under a `docs/` directory. The endpoint should be documented alongside the existing SBOM endpoints (`GET /api/v2/sbom`, `GET /api/v2/sbom/{id}`).
- Document the following:
  - **Path**: `GET /api/v2/sbom/{id}/advisory-summary`
  - **Path parameters**: `id` (string) — the SBOM identifier
  - **Query parameters**: `threshold` (optional, string, one of: `critical`, `high`, `medium`, `low`) — filter counts to only include severities at or above the specified level
  - **Success response** (200 OK): `{ "critical": number, "high": number, "medium": number, "low": number, "total": number }`
  - **Error responses**: 404 Not Found when SBOM ID does not exist
  - **Caching**: responses are cached for 5 minutes; cache is invalidated when new advisories are linked to the SBOM
- Follow the documentation format and style established by existing endpoint documentation in the repository.
- Per constraints doc section 4.9: tasks that change public APIs should include documentation updates.

## Reuse Candidates
- `README.md` — existing API documentation format and style to follow

## Acceptance Criteria
- [ ] New endpoint is documented with path, parameters, response shape, and error responses
- [ ] Documentation follows the same format as existing endpoint documentation
- [ ] Caching behavior is documented
- [ ] Threshold query parameter is documented with allowed values

## Test Requirements
- [ ] Manual review: documentation is accurate and consistent with the implemented endpoint behavior

## Dependencies
- Depends on: Task 3 — Add advisory summary endpoint
