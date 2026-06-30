# File 2: `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (CREATE)

## Purpose

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary` that returns aggregated severity counts.

## Detailed Changes

### Handler function

```rust
use axum::{
    extract::{Path, State},
    Json,
};
use crate::advisory::{
    model::severity_summary::SeveritySummary,
    service::advisory::AdvisoryService,
};
use common::error::AppError;
use trustify_common::db::Transactional;
use trustify_common::id::Id;

/// GET /api/v2/sbom/{id}/advisory-summary
///
/// Returns aggregated severity counts for advisories linked to the given SBOM.
#[utoipa::path(
    get,
    path = "/api/v2/sbom/{id}/advisory-summary",
    params(("id" = Id, Path, description = "SBOM identifier")),
    responses(
        (status = 200, description = "Severity summary", body = SeveritySummary),
        (status = 404, description = "SBOM not found"),
    ),
)]
pub async fn severity_summary(
    Path(id): Path<Id>,
    State(service): State<AdvisoryService>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &Transactional::default())
        .await?;
    Ok(Json(summary))
}
```

### Design decisions

- **Follows `get.rs` pattern exactly**: The handler signature mirrors the existing `get` endpoint -- extracts `Path<Id>`, uses `State` for service injection, returns `Result<Json<T>, AppError>`.
- **utoipa annotation**: Includes OpenAPI path annotation following the convention observed in sibling endpoint files, enabling automatic API documentation generation.
- **Error propagation**: Uses the `?` operator which propagates `AppError` directly. The service method handles returning 404 when the SBOM is not found, consistent with existing SBOM endpoints.
- **Transactional::default()**: Uses the default transactional context, matching the pattern in sibling handlers.
