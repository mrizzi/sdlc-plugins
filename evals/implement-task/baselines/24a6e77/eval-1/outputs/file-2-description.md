# File 2: `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (CREATE)

## Purpose

HTTP GET handler for `/api/v2/sbom/{id}/advisory-summary` that calls the service layer and returns the severity summary as JSON.

## Detailed Changes

Create a new file with the following content:

```rust
use actix_web::web;
use axum::extract::Path;
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use trustify_common::db::Transactional;
use trustify_common::error::AppError;
use trustify_common::id::Id;

/// GET /api/v2/sbom/{id}/advisory-summary
///
/// Returns aggregated severity counts for all advisories linked to the
/// specified SBOM.
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
pub async fn handler(
    service: web::Data<AdvisoryService>,
    Path(id): Path<Id>,
    tx: web::Data<Transactional<'_>>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("fetching severity summary for SBOM")?;

    Ok(Json(summary))
}
```

## Conventions Applied

- **Follows `get.rs` pattern exactly**: Extracts `Path<Id>` for the SBOM identifier, calls the service method, wraps the result in `Json(...)`.
- **Error handling**: Uses `Result<Json<SeveritySummary>, AppError>` return type with `.context()` wrapping, matching the project-wide convention from `common/src/error.rs`.
- **OpenAPI annotation**: Includes `#[utoipa::path(...)]` attribute for API documentation generation, consistent with existing endpoints.
- **Naming**: Handler function named `handler`, matching the convention in sibling endpoint files (`get.rs`, `list.rs`).
