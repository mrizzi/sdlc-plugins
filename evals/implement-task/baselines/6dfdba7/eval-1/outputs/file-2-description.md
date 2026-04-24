# File 2: modules/fundamental/src/advisory/endpoints/severity_summary.rs

## Action: CREATE

## Purpose

Define the GET handler for `/api/v2/sbom/{id}/advisory-summary` that calls `AdvisoryService::severity_summary()` and returns the `SeveritySummary` as JSON.

## Conventions Applied

- Follows the handler pattern from sibling `get.rs` in `advisory/endpoints/`.
- Extracts path parameters via `axum::extract::Path<Id>`.
- Accepts service state via `axum::extract::State` or `Extension` (whichever pattern the existing handlers use).
- Returns `Result<Json<SeveritySummary>, AppError>`.
- Uses `.context()` wrapping for error propagation matching `common/src/error.rs`.

## Detailed Changes

```rust
use axum::{
    extract::{Path, State},
    Json,
};
use trustify_common::error::AppError;
use trustify_common::db::Transactional;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;

/// GET /api/v2/sbom/{id}/advisory-summary
///
/// Returns aggregated advisory severity counts for the given SBOM.
#[utoipa::path(
    get,
    path = "/api/v2/sbom/{id}/advisory-summary",
    params(
        ("id" = Id, Path, description = "SBOM identifier"),
    ),
    responses(
        (status = 200, description = "Advisory severity summary", body = SeveritySummary),
        (status = 404, description = "SBOM not found"),
    ),
)]
pub async fn severity_summary(
    State(service): State<AdvisoryService>,
    Path(id): Path<Id>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to fetch advisory severity summary")?;

    Ok(Json(summary))
}
```

## Notes

- The `Id` type is whatever the existing handlers use for SBOM identifiers (likely a UUID wrapper or string type).
- The `Transactional` extractor is passed through to the service layer, following the existing pattern where database transactions are managed at the handler level.
- The `#[utoipa::path]` annotation is included if the project generates OpenAPI specs (consistent with sibling endpoints).
- 404 handling is delegated to the service layer: if `severity_summary()` cannot find the SBOM, it returns an `AppError` that maps to 404.
