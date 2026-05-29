# File 2: modules/fundamental/src/advisory/endpoints/severity_summary.rs (CREATE)

## Purpose

New endpoint handler file implementing `GET /api/v2/sbom/{id}/advisory-summary`.

## Detailed Changes

Create a new file with the following contents:

### Handler Function: `get_severity_summary`

```rust
use axum::{
    extract::{Path, State},
    Json,
};
use common::error::AppError;
use entity::Id;
use crate::advisory::{
    model::severity_summary::SeveritySummary,
    service::advisory::AdvisoryService,
};
use trustify_common::db::Transactional;

/// Handler for `GET /api/v2/sbom/{id}/advisory-summary`.
///
/// Returns a severity breakdown (critical, high, medium, low, total) of
/// advisories linked to the specified SBOM. Returns 404 if the SBOM does
/// not exist.
pub async fn get_severity_summary(
    State(service): State<AdvisoryService>,
    Path(id): Path<Id>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("fetching advisory severity summary")?;

    Ok(Json(summary))
}
```

### Design Decisions

- **Path parameter extraction**: Uses `Path<Id>` following the exact pattern in `advisory/endpoints/get.rs`.
- **Service call**: Calls `service.severity_summary(id, &tx)` matching the method signature pattern of `fetch` and `list` in the service.
- **Error handling**: Returns `Result<Json<SeveritySummary>, AppError>` with `.context()` wrapping, matching the error handling convention in all sibling handlers.
- **Return type**: Returns `Json<SeveritySummary>` directly -- Axum handles serialization.
- **State extraction**: Uses `State(service)` to get the `AdvisoryService` from Axum's shared state, following the same pattern as `get.rs`.
- The handler function has a `///` doc comment explaining what it does.

### Convention Conformance

- Follows the exact endpoint handler pattern from `advisory/endpoints/get.rs` (extract path params via `Path<Id>`, call service, return JSON).
- Error handling uses `Result<T, AppError>` with `.context()`.
- Naming follows `get_<resource>` pattern consistent with `get_advisory` in `get.rs`.
