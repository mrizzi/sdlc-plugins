## Repository
trustify-backend

## Target Branch
main

## Description
Execute performance benchmarks for the advisory severity aggregation feature (TC-9001). Validate that API response time is within acceptable thresholds under load, no memory leaks are detected during sustained usage, and database query performance does not degrade with increased data volume. The non-functional requirement specifies p95 < 200ms for SBOMs with up to 500 advisories.

## Acceptance Criteria
- [ ] API response time is within acceptable thresholds under load
- [ ] No memory leaks detected during sustained usage
- [ ] Database query performance does not degrade with increased data volume

## Test Requirements
- [ ] Performance test: `GET /api/v2/sbom/{id}/advisory-summary` p95 response time < 200ms with SBOM containing 500 linked advisories
- [ ] Performance test: sustained load (100 concurrent requests over 5 minutes) shows no unbounded memory growth
- [ ] Performance test: response time with 100 advisories vs 500 advisories shows linear or sub-linear scaling, not exponential
- [ ] Performance test: cached responses (within 5-minute TTL) return within 10ms p95
- [ ] Performance test: alert threshold — p95 does not exceed 500ms under any tested load profile

## Dependencies
- Depends on: Task 1 — Add advisory severity summary response model
- Depends on: Task 2 — Add advisory severity aggregation service method
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint
- Depends on: Task 4 — Add cache invalidation for advisory summary
- Depends on: Task 5 — Add threshold query parameter to advisory summary endpoint
- Depends on: Task 6 — Add integration tests for advisory summary endpoint
