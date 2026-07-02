## Repository
trustify-backend

## Target Branch
main

## Description
Execute smoke tests for the advisory severity aggregation feature to validate that all new and modified API endpoints return successful responses with valid inputs, maintain backward compatibility for existing endpoints, and that the end-to-end workflow (SBOM ingestion, advisory correlation, and severity summary retrieval) completes without errors.

additional_fields: { "labels": ["ai-generated-jira"], "priority": "Major", "fixVersions": "RHTPA 1.5.0" }

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with valid JSON for a valid SBOM ID
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns 200 with filtered results
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 404 for non-existent SBOM ID
- [ ] All existing SBOM endpoints (`GET /api/v2/sbom`, `GET /api/v2/sbom/{id}`) continue to return expected responses (backward compatibility)
- [ ] All existing advisory endpoints (`GET /api/v2/advisory`, `GET /api/v2/advisory/{id}`) continue to return expected responses (backward compatibility)
- [ ] End-to-end workflow completes: ingest SBOM, ingest advisories, correlate, call advisory-summary, verify counts match

## Test Requirements
- [ ] All new API endpoints return successful responses with valid inputs
- [ ] All modified API endpoints maintain backward compatibility
- [ ] End-to-end workflow completes without errors

## Dependencies
- Depends on: Task 1 — Create advisory severity summary model and aggregation service
- Depends on: Task 2 — Implement advisory-summary REST endpoint with caching
- Depends on: Task 3 — Add cache invalidation to advisory ingestion pipeline
- Depends on: Task 4 — Write integration tests for advisory-summary endpoint
