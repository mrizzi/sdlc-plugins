## Repository
trustify-backend

## Target Branch
main

## Description
Perform performance benchmark validation for the advisory severity aggregation feature (TC-9001). Verify that the API response time is within acceptable thresholds under load, that no memory leaks are detected during sustained usage, and that database query performance does not degrade with increased data volume.

Specifically, validate against the feature's non-functional requirements:
- `GET /api/v2/sbom/{id}/advisory-summary` p95 response time < 200ms for SBOMs with up to 500 advisories
- No memory leaks during sustained advisory-summary requests
- Aggregation query performance does not degrade as advisory count increases

## Acceptance Criteria
- [ ] API response time is within acceptable thresholds under load
- [ ] No memory leaks detected during sustained usage
- [ ] Database query performance does not degrade with increased data volume

## Test Requirements
- [ ] Benchmark: measure p95 response time for `GET /api/v2/sbom/{id}/advisory-summary` with SBOMs having 10, 100, and 500 linked advisories
- [ ] Benchmark: verify p95 < 200ms for SBOMs with up to 500 advisories
- [ ] Benchmark: run sustained load test and monitor memory usage for leaks
- [ ] Benchmark: measure query performance with increasing advisory counts to verify no degradation

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and aggregation service method
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching and threshold filter
- Depends on: Task 3 — Add cache invalidation for advisory-summary during advisory ingestion
- Depends on: Task 4 — Add integration tests for advisory-summary endpoint
