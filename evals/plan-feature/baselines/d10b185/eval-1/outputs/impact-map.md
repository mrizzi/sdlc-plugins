# Repository Impact Map — TC-9001

## Feature

**TC-9001**: Add advisory severity aggregation endpoint

## Workflow Mode

**direct-to-main** — All changes are confined to a single repository (trustify-backend). The new endpoint is purely additive and does not break existing functionality. No coordinated schema migrations, no breaking API changes, and no cross-cutting refactors are required. Each task can be merged to `main` independently without leaving the codebase in a broken state.

## Impact

```
trustify-backend:
  changes:
    - Add AdvisorySeveritySummary model struct for severity count response
    - Add advisory severity aggregation query method to SbomService
    - Add GET /api/v2/sbom/{id}/advisory-summary endpoint handler with 5-minute cache
    - Add optional ?threshold query parameter support for severity filtering (non-MVP)
    - Add cache invalidation for advisory summaries in the advisory ingestion pipeline
    - Add integration tests for the advisory-summary endpoint
    - Update API documentation to include the new endpoint
```

## Task Breakdown

| Task | Summary | Dependencies |
|------|---------|--------------|
| 1 | Add AdvisorySeveritySummary model and SbomService aggregation method | None |
| 2 | Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching | Task 1 |
| 3 | Add cache invalidation for advisory summaries in advisory ingestion | Task 2 |
| 4 | Add integration tests for advisory-summary endpoint | Task 2 |
| 5 | Add API documentation for the advisory-summary endpoint | Task 2 |
