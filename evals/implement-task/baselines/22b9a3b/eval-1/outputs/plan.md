# Implementation Plan: TC-9201

## Task Summary

Add an advisory severity aggregation service method and REST endpoint that returns severity counts (Critical, High, Medium, Low, total) for a given SBOM, enabling dashboard widgets to render severity breakdowns without client-side counting.

## Files to Create

| # | File Path | Purpose |
|---|---|---|
| 1 | `modules/fundamental/src/advisory/model/severity_summary.rs` | New `SeveritySummary` response struct |
| 2 | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | GET handler for `/api/v2/sbom/{id}/advisory-summary` |
| 3 | `tests/api/advisory_summary.rs` | Integration tests for the new endpoint |

## Files to Modify

| # | File Path | Purpose |
|---|---|---|
| 4 | `modules/fundamental/src/advisory/endpoints/mod.rs` | Register the new severity summary route |
| 5 | `modules/fundamental/src/advisory/model/mod.rs` | Add `pub mod severity_summary;` to register the new model module |
| 6 | `modules/fundamental/src/advisory/service/advisory.rs` | Add `severity_summary` method to `AdvisoryService` |

## Files NOT Modified

- `server/src/main.rs` -- No changes needed; routes auto-mount via module registration as stated in the task description.

## Implementation Order

1. **Model first** (file 1, file 5): Create the `SeveritySummary` struct and register it in `model/mod.rs`. This has no dependencies and is needed by both the service and endpoint.
2. **Service method** (file 6): Add `severity_summary` method to `AdvisoryService`. This depends on the model struct and the `sbom_advisory` entity.
3. **Endpoint handler** (file 2, file 4): Create the GET handler and register the route. This depends on the service method and model.
4. **Tests** (file 3): Write integration tests. These depend on all the above being in place.

## API Surface

```
GET /api/v2/sbom/{id}/advisory-summary

Response 200:
{
  "critical": 5,
  "high": 12,
  "medium": 8,
  "low": 3,
  "total": 28
}

Response 404:
{
  "error": "SBOM not found"
}
```

## Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary that returns counts of
advisory severities (critical, high, medium, low, total) for a given
SBOM. Includes SeveritySummary response model, AdvisoryService method,
endpoint handler, and integration tests.

Resolves: TC-9201
```

## Key Design Decisions

1. **Deduplication**: The service method deduplicates advisories by advisory ID before counting, ensuring each advisory is counted only once even if linked multiple times through the `sbom_advisory` join table.
2. **Default zeros**: All severity levels default to 0 when no advisories exist, so the response always has a consistent shape.
3. **404 handling**: If the SBOM ID does not exist, a 404 `AppError` is returned, consistent with existing SBOM endpoints.
4. **Route placement**: The route is nested under the SBOM path (`/api/v2/sbom/{id}/advisory-summary`) since it returns advisory data scoped to a specific SBOM.
5. **No pagination**: This is a summary/aggregation endpoint returning fixed-shape data, so `PaginatedResults<T>` is not used.
