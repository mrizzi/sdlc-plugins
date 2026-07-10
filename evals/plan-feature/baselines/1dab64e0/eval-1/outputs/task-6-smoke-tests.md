## Repository
trustify-backend

## Target Branch
main

## Description
Perform smoke test validation for the advisory severity aggregation feature (TC-9001). Verify that all new API endpoints return successful responses with valid inputs, that all modified API endpoints maintain backward compatibility, and that the end-to-end workflow completes without errors.

Specifically, validate:
- The new `GET /api/v2/sbom/{id}/advisory-summary` endpoint responds with valid severity counts
- Existing SBOM and advisory endpoints continue to function correctly after the changes
- The full workflow (ingest SBOM, ingest advisories, fetch severity summary) completes end-to-end

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors

## Test Requirements
- [ ] Smoke test: `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with valid severity counts for a valid SBOM
- [ ] Smoke test: `GET /api/v2/sbom/{id}/advisory-summary` returns 404 for non-existent SBOM
- [ ] Smoke test: existing `GET /api/v2/sbom/{id}` endpoint still works correctly
- [ ] Smoke test: existing `GET /api/v2/advisory` endpoint still works correctly
- [ ] Smoke test: end-to-end flow (ingest SBOM -> ingest advisories -> fetch summary) completes without errors

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and aggregation service method
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching and threshold filter
- Depends on: Task 3 — Add cache invalidation for advisory-summary during advisory ingestion
- Depends on: Task 4 — Add integration tests for advisory-summary endpoint
