## Repository
trustify-backend

## Target Branch
main

## Description
Execute smoke tests for the advisory severity aggregation feature (TC-9001). Validate that all new API endpoints return successful responses with valid inputs, all modified API endpoints maintain backward compatibility, and the end-to-end workflow (SBOM ingestion, advisory correlation, severity summary retrieval) completes without errors.

## Acceptance Criteria
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors

## Test Requirements
- [ ] Smoke test: `GET /api/v2/sbom/{valid-id}/advisory-summary` returns 200 with valid severity counts
- [ ] Smoke test: `GET /api/v2/sbom/{valid-id}/advisory-summary?threshold=critical` returns 200 with filtered counts
- [ ] Smoke test: existing `GET /api/v2/sbom/{id}` endpoint still returns expected results (backward compatibility)
- [ ] Smoke test: existing `GET /api/v2/sbom` list endpoint still returns expected results (backward compatibility)
- [ ] Smoke test: existing `GET /api/v2/advisory` endpoint still returns expected results (backward compatibility)
- [ ] Smoke test: end-to-end flow — ingest SBOM, correlate advisories, call `GET /api/v2/sbom/{id}/advisory-summary`, verify severity counts reflect the correlated advisories

## Dependencies
- Depends on: Task 1 — Add advisory severity summary response model
- Depends on: Task 2 — Add advisory severity aggregation service method
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint
- Depends on: Task 4 — Add cache invalidation for advisory summary
- Depends on: Task 5 — Add threshold query parameter to advisory summary endpoint
- Depends on: Task 6 — Add integration tests for advisory summary endpoint
