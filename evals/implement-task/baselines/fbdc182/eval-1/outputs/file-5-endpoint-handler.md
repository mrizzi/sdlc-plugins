# File 5 — Create: `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

## Purpose

Axum handler for `GET /api/v2/sbom/{id}/advisory-summary`. Extracts the SBOM ID from the path, calls `AdvisoryService::severity_summary`, and returns the result as JSON.

## Inspection Step

Before writing, read `modules/fundamental/src/advisory/endpoints/get.rs` in full to confirm:
- How `State` and `Path` extractors are imported and used
- The exact type for `Id` (may be `uuid::Uuid`, `i64`, or a newtype wrapper)
- How `Transactional` is obtained (likely from `State` alongside the service, or as a separate extractor)
- How `Json` is returned
- Whether `#[utoipa::path(...)]` annotations are used on handlers

Also read `modules/fundamental/src/sbom/endpoints/get.rs` as a second sibling to confirm the `Transactional` extractor pattern — this is especially important because the new endpoint crosses the SBOM/advisory boundary.

## Full File Content

```rust
use axum::{
    extract::{Path, State},
    Json,
};
use std::sync::Arc;

use common::db::Transactional;
use common::error::AppError;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::advisory::AdvisoryService;

/// GET /api/v2/sbom/{id}/advisory-summary
///
/// Returns aggregated advisory severity counts for the specified SBOM.
/// Responds with 404 if the SBOM does not exist.
#[utoipa::path(
    get,
    path = "/api/v2/sbom/{id}/advisory-summary",
    params(
        ("id" = Id, Path, description = "SBOM identifier")
    ),
    responses(
        (status = 200, description = "Severity summary returned", body = SeveritySummary),
        (status = 404, description = "SBOM not found"),
    ),
    tag = "advisory"
)]
pub async fn severity_summary(
    State(service): State<Arc<AdvisoryService>>,
    Path(id): Path<Id>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await?;
    Ok(Json(summary))
}
```

## Notes on `Id` type

The exact type for `Id` must be confirmed by reading `modules/fundamental/src/advisory/endpoints/get.rs`. Common patterns:
- `uuid::Uuid` — if advisories are UUID-keyed
- A newtype like `SbomId(uuid::Uuid)` — if the codebase uses typed IDs

Use whatever type `get.rs` uses for `Path<Id>`.

## Notes on `Transactional` extractor

The `Transactional<'_>` pattern must be confirmed. In Axum, a database transaction is usually obtained via:
- A custom extractor that begins a transaction from the connection pool in `State`
- A `DatabaseConnection` from `State` with explicit `.begin()` called in the handler body

Read `get.rs` to see the exact pattern and replicate it. If transactions are not used for read-only handlers, use `&DatabaseConnection` directly from `State`.

## Notes on `#[utoipa::path(...)]` annotation

If `get.rs` does not use utoipa annotations, omit the `#[utoipa::path(...)]` block entirely. Only include it if sibling handlers use it.

## Convention compliance

- Handler function name matches the file name: `severity_summary`
- `///` doc comment before the handler
- Returns `Result<Json<SeveritySummary>, AppError>` — matches the `Result<T, AppError>` convention
- `?` propagation used (no manual error mapping in handler body)
- State and Path extractor order matches sibling handlers
- No business logic in the handler — all logic delegated to `AdvisoryService`
