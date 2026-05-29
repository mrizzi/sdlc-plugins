# File 4: Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

## Action: CREATE

## Purpose

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary` that returns aggregated severity counts.

## Detailed Changes

This is a new file. The complete contents would be:

```rust
use axum::{
    extract::{Path, State},
    Json,
};
use common::error::AppError;
use crate::advisory::service::AdvisoryService;
use crate::advisory::model::severity_summary::SeveritySummary;
use trustify_common::db::Transactional;
use trustify_common::id::Id;

/// GET /api/v2/sbom/{id}/advisory-summary
///
/// Returns aggregated severity counts for all advisories linked to the specified SBOM.
#[utoipa::path(
    get,
    path = "/api/v2/sbom/{id}/advisory-summary",
    params(
        ("id" = Id, Path, description = "SBOM identifier"),
    ),
    responses(
        (status = 200, description = "Severity summary", body = SeveritySummary),
        (status = 404, description = "SBOM not found"),
    ),
)]
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    State(state): State<AppState>,
) -> Result<Json<SeveritySummary>, AppError> {
    let service = AdvisoryService::new(&state.db);
    let tx = Transactional::None;

    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("failed to compute advisory severity summary")?
        .ok_or_else(|| AppError::NotFound(format!("SBOM with id {id} not found")))?;

    Ok(Json(summary))
}
```

## Conventions Applied

- **Handler signature**: `async fn(Path<Id>, State<AppState>) -> Result<Json<T>, AppError>` -- exactly matches the pattern discovered in `advisory/endpoints/get.rs`
- **Path extraction**: Uses `Path(id): Path<Id>` for extracting the SBOM ID from the URL path
- **State extraction**: Uses `State(state): State<AppState>` for accessing the application state (database pool)
- **Service instantiation**: Creates `AdvisoryService::new(&state.db)` matching the pattern in sibling endpoint handlers
- **Error handling**: Uses `.context()` for wrapping the service call error, and `.ok_or_else()` to convert `None` to `AppError::NotFound` -- both patterns observed in `advisory/endpoints/get.rs`
- **404 pattern**: Returns `AppError::NotFound` with a descriptive message when the SBOM does not exist, matching the existing endpoint behavior
- **utoipa annotation**: Includes OpenAPI documentation via the `#[utoipa::path]` macro, consistent with existing endpoint handlers
- **Response type**: Returns `Json<SeveritySummary>` directly -- Axum handles serialization
