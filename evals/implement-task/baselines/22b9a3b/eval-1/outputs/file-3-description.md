# File 3: modules/fundamental/src/advisory/endpoints/severity_summary.rs

## Action: CREATE

## Purpose

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary`. This endpoint extracts the SBOM ID from the path, calls the `AdvisoryService::severity_summary` method, and returns the result as JSON.

## Sibling Reference

Modeled after `modules/fundamental/src/advisory/endpoints/get.rs` which handles `GET /api/v2/advisory/{id}`:
- Extracts path params via `Path<Id>`
- Calls a service method
- Returns `Result<Json<T>, AppError>`

Also references `modules/fundamental/src/sbom/endpoints/get.rs` for the pattern of a GET endpoint scoped to a specific SBOM.

## Detailed Changes

```rust
use axum::{
    extract::{Path, State},
    Json,
};

use crate::advisory::{
    model::severity_summary::SeveritySummary,
    service::AdvisoryService,
};
use common::error::AppError;
use common::db::Transactional;

/// GET /api/v2/sbom/{id}/advisory-summary
///
/// Returns aggregated advisory severity counts for the specified SBOM.
///
/// # Responses
/// - 200: SeveritySummary with counts per severity level
/// - 404: SBOM not found
pub async fn get_severity_summary(
    State(service): State<AdvisoryService>,
    Path(sbom_id): Path<String>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(sbom_id.into(), &tx)
        .await?;

    Ok(Json(summary))
}
```

## Design Notes

- **Handler signature**: Follows the Axum convention of extracting state (service), path parameters, and transactional context as function parameters.
- **Path parameter**: Uses `Path<String>` (or `Path<Id>` depending on the project's `Id` type) to extract the SBOM identifier from the URL.
- **Error propagation**: The `?` operator propagates `AppError` from the service method, including the 404 case when the SBOM does not exist. No additional error handling is needed in the handler.
- **No pagination**: This is an aggregation endpoint returning a fixed-shape summary, so `PaginatedResults` is not used.
- **JSON serialization**: Axum's `Json` wrapper handles serialization of the `SeveritySummary` struct automatically via serde.
