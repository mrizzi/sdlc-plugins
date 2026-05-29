# Repository Impact Map — TC-9001: Add advisory severity aggregation endpoint

## Impact Map

```
trustify-backend:
  changes:
    - Add AdvisorySeveritySummary model struct for severity count response
    - Add service method to SbomService to aggregate advisory severity counts by SBOM ID with deduplication
    - Add GET /api/v2/sbom/{id}/advisory-summary endpoint handler
    - Register the new route in SBOM endpoint module
    - Add 5-minute cache configuration for the advisory-summary endpoint
    - Add cache invalidation in advisory ingestion pipeline when new advisories are linked to an SBOM
    - Add optional ?threshold query parameter to filter severity counts above a threshold (non-MVP)
    - Add integration tests for the advisory-summary endpoint
    - Update API documentation to include the new endpoint
```

## Workflow Mode Decision

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators were identified:

1. **Coordinated schema migrations** -- No new database tables or schema changes are required. The feature uses existing advisory-SBOM relationship tables (`sbom_advisory` join table).
2. **Breaking API changes** -- The feature adds a new endpoint (`GET /api/v2/sbom/{id}/advisory-summary`) without modifying any existing endpoints or API contracts.
3. **Cross-cutting refactors** -- No structural changes, renames, or module reorganizations are needed. The new code follows the existing module pattern (model + service + endpoints).
4. **Tightly coupled feature components** -- All changes are within a single repository (trustify-backend) and each task can be merged independently without leaving `main` in a broken state. The service layer can exist before the endpoint, and tests can be added incrementally.

Since no atomicity constraints exist, each task PR can be merged to `main` independently in sequence.
