## Repository
trustify-backend

## Target Branch
main

## Description
Execute performance benchmarks for the advisory severity aggregation feature to validate that the new endpoint meets p95 latency targets, does not introduce memory leaks, and that database query performance does not degrade with increased data volume. The feature requires p95 < 200ms for SBOMs with up to 500 advisories.

additional_fields: { "labels": ["ai-generated-jira"], "priority": "Major", "fixVersions": "RHTPA 1.5.0" }

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` p95 response time is under 200ms for an SBOM with 500 linked advisories
- [ ] No memory leaks detected during sustained usage (1000+ sequential requests)
- [ ] Database query performance for the aggregation query does not degrade when the SBOM has 100, 250, and 500 advisories
- [ ] Cached responses return within single-digit milliseconds (validating cache effectiveness)
- [ ] Cache invalidation does not introduce noticeable latency to the advisory ingestion pipeline

## Test Requirements
- [ ] API response time is within acceptable thresholds under load
- [ ] No memory leaks detected during sustained usage
- [ ] Database query performance does not degrade with increased data volume

## Dependencies
- Depends on: Task 1 — Create advisory severity summary model and aggregation service
- Depends on: Task 2 — Implement advisory-summary REST endpoint with caching
- Depends on: Task 3 — Add cache invalidation to advisory ingestion pipeline
- Depends on: Task 4 — Write integration tests for advisory-summary endpoint
