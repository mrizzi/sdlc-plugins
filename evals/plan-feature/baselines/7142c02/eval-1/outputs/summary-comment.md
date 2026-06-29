# Implementation Plan Summary — TC-9001: Add Advisory Severity Aggregation Endpoint

## Tasks Created

| # | Slug | Title |
|---|---|---|
| 1 | task-1-advisory-summary-model | Define AdvisorySeveritySummary response struct and SeverityThreshold enum |
| 2 | task-2-advisory-summary-service | Implement service-layer severity aggregation query |
| 3 | task-3-advisory-summary-endpoint | Implement GET /api/v2/sbom/{id}/advisory-summary endpoint with caching |
| 4 | task-4-cache-invalidation | Add cache invalidation to advisory ingestion pipeline |
| 5 | task-5-integration-tests | Write comprehensive integration tests for the endpoint |

## Repositories Affected

- **trustify-backend** — all 5 tasks target this repository

## Architecture Summary

The implementation adds a new REST endpoint (`GET /api/v2/sbom/{id}/advisory-summary`) to the existing SBOM module following the project's established `model/ + service/ + endpoints/` pattern. The work is decomposed into five tasks forming a dependency chain:

1. **Model layer** (Task 1): Defines the `AdvisorySeveritySummary` response struct and `SeverityThreshold` enum in the SBOM model directory.
2. **Service layer** (Task 2): Implements the database aggregation query that joins `sbom_advisory` with `advisory`, deduplicates by advisory ID, and groups counts by severity level. Validates SBOM existence (404 if missing) and supports optional threshold filtering.
3. **Endpoint layer** (Task 3): Exposes the service via an Axum HTTP handler with path and query parameter extraction, JSON response serialization, and 5-minute `tower-http` cache configuration.
4. **Cache invalidation** (Task 4): Hooks into the advisory ingestion pipeline to invalidate cached summaries when new SBOM-advisory relationships are created.
5. **Integration tests** (Task 5): Comprehensive test suite covering success cases, 404 handling, threshold filtering, deduplication, and cache headers.

No new database tables or migrations are required — the endpoint queries existing `sbom_advisory` and `advisory` entities.

## Inherited Fields

Inherited fields propagated to tasks: priority=Major, fixVersion=RHTPA 1.5.0
