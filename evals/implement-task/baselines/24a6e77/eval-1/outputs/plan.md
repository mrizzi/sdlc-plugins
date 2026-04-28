# Implementation Plan: TC-9201 — Add advisory severity aggregation service and endpoint

## Pre-implementation Analysis

Before making any changes, inspect the following existing files to understand conventions and patterns:

1. **`modules/fundamental/src/advisory/endpoints/get.rs`** — Study the existing GET handler pattern: how path parameters are extracted via `Path<Id>`, how the service is called, how errors are mapped, and how the JSON response is returned. This is the primary template for the new endpoint handler.

2. **`modules/fundamental/src/advisory/service/advisory.rs`** — Study the `AdvisoryService` struct and its existing `fetch` and `list` methods. Understand the method signature pattern (`&self, id: Id, tx: &Transactional<'_>`) and how results are returned as `Result<T, AppError>`. This is the template for the new `severity_summary` method.

3. **`modules/fundamental/src/advisory/model/summary.rs`** — Examine the `AdvisorySummary` struct to understand the `severity` field that will be used for counting. Also observe the derive macros and serde attributes used on model structs.

4. **`common/src/error.rs`** — Understand the `AppError` enum and how `.context()` wrapping is used for error propagation. All new code must follow this error handling convention.

5. **`modules/fundamental/src/advisory/endpoints/mod.rs`** — See how routes are registered using `Router::new().route("/path", get(handler))` to follow the same pattern for the new route.

6. **`modules/fundamental/src/advisory/model/mod.rs`** — See how model submodules are declared with `pub mod` to follow the same pattern.

## Branch

Create branch `TC-9201` from main before starting implementation.

## Files to Create

| # | File | Purpose |
|---|------|---------|
| 1 | `modules/fundamental/src/advisory/model/severity_summary.rs` | `SeveritySummary` response struct with fields: `critical`, `high`, `medium`, `low`, `total` (all `u64`), deriving `Serialize`, `Deserialize`, `Clone`, `Debug`, `Default`, `utoipa::ToSchema` |
| 2 | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | GET handler for `/api/v2/sbom/{id}/advisory-summary`. Extracts `Path<Id>`, calls `AdvisoryService::severity_summary`, returns `Json<SeveritySummary>` |
| 3 | `tests/api/advisory_summary.rs` | Integration tests: valid SBOM with known advisories, non-existent SBOM returns 404, SBOM with no advisories returns all zeros, duplicate advisories are deduplicated |

## Files to Modify

| # | File | Change |
|---|------|--------|
| 4 | `modules/fundamental/src/advisory/model/mod.rs` | Add `pub mod severity_summary;` to register the new model module |
| 5 | `modules/fundamental/src/advisory/endpoints/mod.rs` | Import the new handler and register the route `.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::handler))` |
| 6 | `modules/fundamental/src/advisory/service/advisory.rs` | Add `severity_summary(&self, sbom_id: Id, tx: &Transactional<'_>) -> Result<SeveritySummary, AppError>` method to `AdvisoryService` |

## Commit

```
git checkout -b TC-9201
# ... make changes ...
git add modules/fundamental/src/advisory/model/severity_summary.rs \
       modules/fundamental/src/advisory/endpoints/severity_summary.rs \
       tests/api/advisory_summary.rs \
       modules/fundamental/src/advisory/model/mod.rs \
       modules/fundamental/src/advisory/endpoints/mod.rs \
       modules/fundamental/src/advisory/service/advisory.rs
git commit -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary model, service method,
endpoint handler, and integration tests.

TC-9201" --trailer='Assisted-by: Claude Code'
```
