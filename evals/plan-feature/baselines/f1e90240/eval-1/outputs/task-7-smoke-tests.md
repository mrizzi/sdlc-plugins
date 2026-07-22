# Task 7: Smoke tests for advisory severity aggregation feature

**Jira Parent**: TC-9001
**Priority**: Major
**Fix Versions**: RHTPA 1.5.0

## Repository

trustify-backend

## Target Branch

main

## Description

Execute smoke tests to validate that the advisory severity aggregation feature works end-to-end in a deployed or locally running instance. Verify that all new API endpoints return successful responses with valid inputs, that existing advisory and SBOM endpoints maintain backward compatibility, and that the full workflow (ingest SBOM, ingest advisories, query summary) completes without errors.

## Acceptance Criteria

- [ ] All new API endpoints return successful responses with valid inputs
  - [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with correct JSON shape for a valid SBOM
  - [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns 200 with filtered counts
  - [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 404 for nonexistent SBOM
- [ ] All modified API endpoints maintain backward compatibility
  - [ ] `GET /api/v2/sbom/{id}` still returns expected SBOM details
  - [ ] `GET /api/v2/sbom` list endpoint is unaffected
  - [ ] `GET /api/v2/advisory` and `GET /api/v2/advisory/{id}` are unaffected
- [ ] End-to-end workflow completes without errors
  - [ ] Ingest an SBOM, ingest advisories that correlate to it, then call the advisory-summary endpoint and verify counts match the ingested data

## Test Requirements

- [ ] Smoke tests are run against a running instance (local or staging) with a real PostgreSQL database
- [ ] Test data includes at least one SBOM with advisories at multiple severity levels
- [ ] Results are documented with pass/fail status for each acceptance criterion

## Dependencies

- Task 1 (advisory severity summary model)
- Task 2 (advisory severity aggregation service)
- Task 3 (advisory-summary endpoint)
- Task 4 (cache invalidation on advisory ingestion)
- Task 5 (advisory-summary integration tests)
