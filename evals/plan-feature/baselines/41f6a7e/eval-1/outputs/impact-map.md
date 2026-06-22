# Repository Impact Map — TC-9001

## Feature: Add advisory severity aggregation endpoint

```
trustify-backend:
  changes:
    - Add AdvisorySeveritySummary model struct to represent severity counts (critical, high, medium, low, total)
    - Add service method to SbomService that queries the sbom_advisory join table, joins to advisory for severity, deduplicates by advisory ID, and aggregates counts by severity level
    - Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute cache configuration
    - Add optional ?threshold query parameter to filter severity counts above a given level
    - Return 404 when SBOM ID does not exist (consistent with existing SBOM endpoints)
    - Add cache invalidation hook in advisory ingestion pipeline when new advisories are linked to an SBOM
    - Add integration tests for the new endpoint covering: success with counts, 404 for missing SBOM, threshold filtering, deduplication of advisories, cache behavior
    - Update API documentation to include the new endpoint
```

## Workflow Mode Decision

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present:
- No coordinated schema migrations — the feature uses existing tables (sbom_advisory, advisory) with no schema changes
- No breaking API changes — this is a net-new endpoint that does not modify existing API contracts
- No cross-cutting refactors — changes are contained within the SBOM module
- No tightly coupled components — this is a backend-only change; the frontend is a separate concern and the endpoint functions independently

All tasks can be merged to main independently without leaving the codebase in a broken state.
