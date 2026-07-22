# Task 8: Performance benchmarks for advisory severity aggregation feature

**Jira Parent**: TC-9001
**Priority**: Major
**Fix Versions**: RHTPA 1.5.0

## Repository

trustify-backend

## Target Branch

main

## Description

Execute performance benchmarks to validate that the advisory severity aggregation endpoint meets the non-functional requirements specified in the feature. Verify that API response time is within acceptable thresholds under load (p95 < 200ms for SBOMs with up to 500 advisories), that no memory leaks are detected during sustained usage, and that the aggregation query performance does not degrade with increased data volume.

## Acceptance Criteria

- [ ] API response time is within acceptable thresholds under load
  - [ ] p95 response time for `GET /api/v2/sbom/{id}/advisory-summary` is < 200ms with an SBOM linked to 500 advisories
  - [ ] p95 response time remains < 200ms under concurrent load (at least 50 concurrent requests)
- [ ] No memory leaks detected during sustained usage
  - [ ] Memory usage remains stable after 1000 consecutive requests to the advisory-summary endpoint
  - [ ] No unbounded growth in cached entries when cache invalidation is functioning
- [ ] Database query performance does not degrade with increased data volume
  - [ ] Aggregation query execution time is measured with 100, 500, and 1000 advisories per SBOM
  - [ ] Query plan uses index scans on the `sbom_advisory` join table, not sequential scans

## Test Requirements

- [ ] Benchmarks are run against a PostgreSQL database with representative data volumes
- [ ] Load testing tool (e.g., `wrk`, `hey`, or `criterion` for Rust microbenchmarks) is used for throughput measurement
- [ ] Results are documented with specific latency percentiles (p50, p95, p99)

## Dependencies

- Task 1 (advisory severity summary model)
- Task 2 (advisory severity aggregation service)
- Task 3 (advisory-summary endpoint)
- Task 4 (cache invalidation on advisory ingestion)
- Task 5 (advisory-summary integration tests)
