# Implementation Plan: TC-9201

## Summary

Add an advisory severity aggregation service method and REST endpoint that returns severity counts (Critical, High, Medium, Low, total) for a given SBOM. This enables dashboard widgets to render severity breakdowns without client-side counting.

## Sibling Analysis Performed

Before planning changes, the following sibling files were inspected to discover conventions:

- `modules/fundamental/src/advisory/endpoints/get.rs` -- endpoint handler pattern (Path extraction, service call, JSON return)
- `modules/fundamental/src/advisory/service/advisory.rs` -- service method signatures (self, id, tx)
- `modules/fundamental/src/advisory/model/summary.rs` -- struct definition pattern (Serialize/Deserialize derives, severity field)
- `modules/fundamental/src/advisory/model/mod.rs` -- module registration pattern
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- route registration pattern
- `modules/fundamental/src/sbom/endpoints/get.rs` -- cross-module endpoint pattern reference
- `entity/src/sbom_advisory.rs` -- join table structure for SBOM-Advisory relationship
- `common/src/error.rs` -- AppError pattern
- `tests/api/advisory.rs` -- integration test pattern

## Files to Create

| # | File | Purpose |
|---|------|---------|
| 1 | `modules/fundamental/src/advisory/model/severity_summary.rs` | SeveritySummary response struct |
| 2 | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | GET handler for `/api/v2/sbom/{id}/advisory-summary` |
| 3 | `tests/api/advisory_summary.rs` | Integration tests for the new endpoint |

## Files to Modify

| # | File | Change |
|---|------|--------|
| 4 | `modules/fundamental/src/advisory/service/advisory.rs` | Add `severity_summary` method to `AdvisoryService` |
| 5 | `modules/fundamental/src/advisory/endpoints/mod.rs` | Register the new route |
| 6 | `modules/fundamental/src/advisory/model/mod.rs` | Add `pub mod severity_summary;` declaration |

## Files NOT Modified

- `server/src/main.rs` -- no changes needed; routes auto-mount via module registration as confirmed in the task description.

## Detailed Change Descriptions

See individual `file-N-description.md` files for detailed changes to each file.

## Change Order

1. Create the model struct first (`file-1`) since other files depend on it.
2. Add the service method (`file-4`) that queries the database and returns the new struct.
3. Register the model module (`file-6`) so the struct is accessible.
4. Create the endpoint handler (`file-2`) that calls the service method.
5. Register the route (`file-5`) to wire the handler into the router.
6. Create integration tests (`file-3`) to validate the endpoint.

## Commit Message

```
feat(advisory): add severity aggregation endpoint

Add SeveritySummary model, AdvisoryService.severity_summary() method,
and GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
advisory severity counts (critical, high, medium, low, total) for a
given SBOM.

TC-9201
```
