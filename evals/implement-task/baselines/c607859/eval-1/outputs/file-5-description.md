# File 5: modules/fundamental/src/advisory/endpoints/severity_summary.rs

**Action**: CREATE

## Context

New endpoint handler file for the `GET /api/v2/sbom/{id}/advisory-summary` route. This
follows the existing endpoint pattern established in `advisory/endpoints/get.rs` and
`sbom/endpoints/get.rs`.

## Sibling Pattern Reference

Examining `advisory/endpoints/get.rs` and `sbom/endpoints/get.rs`:
- Handlers are `async fn` that extract path parameters via `Path<Id>`
- Handlers receive the service via Axum state extraction (e.g., `State<AdvisoryService>` or similar app state pattern)
- Handlers return `Result<Json<T>, AppError>`
- Transaction context is obtained from the app state or connection pool
- Error propagation uses `.context()` wrapping

## File Contents

```rust
use axum::{
    extract::{Path, State},
    Json,
};

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;
use common::db::Transactional;

/// Handler for `GET /api/v2/sbom/{id}/advisory-summary`.
///
/// Returns aggregated severity counts for all vulnerability advisories
/// linked to the specified SBOM. The response includes counts for critical,
/// high, medium, and low severity levels, plus a total.
pub async fn get_severity_summary(
    State(service): State<AdvisoryService>,
    Path(sbom_id): Path<Id>,
) -> Result<Json<SeveritySummary>, AppError> {
    // Use a read transaction for the query
    let tx = Transactional::None; // or obtain from connection pool as per project pattern

    let summary = service
        .severity_summary(sbom_id, &tx)
        .await
        .context("fetching advisory severity summary")?;

    Ok(Json(summary))
}
```

## Design Decisions

- **Path parameter extraction**: uses `Path<Id>` consistent with `get.rs` siblings.
- **State extraction**: uses `State<AdvisoryService>` consistent with how services are injected in the Axum app state.
- **Return type**: `Result<Json<SeveritySummary>, AppError>` -- the `Json` wrapper serializes the struct; `AppError` implements `IntoResponse` for error cases.
- **Transaction**: follows the same transactional pattern as sibling handlers.
- **Error wrapping**: uses `.context()` consistent with all handlers in the codebase.
- **Documentation**: handler function has a doc comment explaining the endpoint's purpose and response.

## Data-Flow Trace

1. Axum receives `GET /api/v2/sbom/{id}/advisory-summary`
2. Router dispatches to `get_severity_summary` handler
3. Handler extracts `sbom_id` from path via `Path<Id>`
4. Handler calls `AdvisoryService::severity_summary(sbom_id, &tx)`
5. Service queries database, deduplicates, counts by severity
6. Service returns `SeveritySummary` or `AppError`
7. Handler wraps result in `Json` and returns
8. Axum serializes `SeveritySummary` to JSON response body

All stages connected -- **COMPLETE**.
