## Repository
trustify-backend

## Description
Update the REST API documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. This documentation task covers the endpoint path, HTTP method, path parameters, optional query parameters, response shape, error responses, and caching behavior. API consumers and the frontend dashboard team need this documentation to integrate with the new endpoint correctly.

## Files to Modify
- `README.md` — add the new endpoint to the API endpoints section with path, parameters, and response shape

## Documentation Updates
- `README.md` — add `GET /api/v2/sbom/{id}/advisory-summary` to the API endpoints section, including:
  - Path: `GET /api/v2/sbom/{id}/advisory-summary`
  - Path parameters: `id` (UUID) -- the SBOM identifier
  - Query parameters: `threshold` (optional, one of `critical`, `high`, `medium`, `low`) -- filters counts to severities at or above the specified level
  - Response body: `{ "critical": number, "high": number, "medium": number, "low": number, "total": number }`
  - Error responses: 404 when SBOM ID does not exist, 400 for invalid threshold value
  - Caching: responses are cached for 5 minutes; cache is invalidated when new advisories are linked to the SBOM

## Implementation Notes
- Check whether the project uses an OpenAPI/Swagger specification file (e.g., `openapi.yaml`, `swagger.json`) or utoipa-generated docs. If so, verify that the new endpoint is included in the generated spec through the utoipa annotations added in Task 3.
- If the project maintains a separate API reference document, add the endpoint documentation following the format used for existing endpoints like `GET /api/v2/sbom/{id}` and `GET /api/v2/advisory`.
- Per `docs/constraints.md` section 5 (Code Change Rules): inspect existing documentation before modifying to match format and conventions.

## Acceptance Criteria
- [ ] The new endpoint is documented with path, parameters, response shape, and error responses
- [ ] Documentation is consistent with existing endpoint documentation format in `README.md`
- [ ] Caching behavior (5-minute TTL, invalidation on advisory ingestion) is documented
- [ ] Threshold query parameter is documented with valid values and behavior

## Test Requirements
- [ ] Manual review: verify the documented response shape matches the actual `AdvisorySeveritySummary` struct fields

## Dependencies
- Depends on: Task 3 — Add advisory summary endpoint
- Depends on: Task 5 — Add threshold query parameter support
