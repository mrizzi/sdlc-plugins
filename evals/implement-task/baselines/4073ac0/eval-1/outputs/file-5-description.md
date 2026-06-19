# File 5: modules/fundamental/src/advisory/endpoints/severity_summary.rs

**Action**: Create

## Purpose

Implements the GET handler for `/api/v2/sbom/{id}/advisory-summary`. Extracts the SBOM ID from the path, calls the `AdvisoryService::severity_summary` method, and returns the result as JSON.

## Full File Content

```rust
//! GET handler for advisory severity summary by SBOM.
//!
//! Returns aggregated severity counts for all advisories linked to the specified SBOM.

use axum::{
    extract::{Path, State},
    Json,
};

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;
use common::db::Transactional;

/// Returns the aggregated advisory severity summary for the given SBOM.
///
/// Queries all advisories linked to the SBOM identified by `id`, deduplicates
/// by advisory ID, and returns counts per severity level (Critical, High,
/// Medium, Low) plus a total count.
///
/// Returns 404 if the SBOM does not exist.
#[utoipa::path(
    get,
    path = "/api/v2/sbom/{id}/advisory-summary",
    responses(
        (status = 200, description = "Advisory severity summary", body = SeveritySummary),
        (status = 404, description = "SBOM not found"),
    ),
    params(
        ("id" = Id, Path, description = "SBOM identifier"),
    ),
)]
pub async fn get_advisory_summary(
    State(service): State<AdvisoryService>,
    Path(id): Path<Id>,
) -> Result<Json<SeveritySummary>, AppError> {
    let tx = Transactional::none();
    let summary = service
        .severity_summary(id, &tx)
        .await?;

    Ok(Json(summary))
}
```

## Design Decisions

- **Handler pattern**: Follows the exact pattern from `advisory/endpoints/get.rs` -- `Path<Id>` extraction, `State<AdvisoryService>` injection, `Result<Json<T>, AppError>` return type
- **Transaction**: Uses `Transactional::none()` for read-only operations, matching the pattern in sibling GET handlers
- **Error propagation**: Uses `?` operator which propagates `AppError` from the service layer. The service's 404 error for non-existent SBOMs flows through naturally.
- **utoipa annotation**: Includes OpenAPI path annotation for API documentation generation, following the pattern of sibling endpoint files (if utoipa is used in the project; would confirm by checking sibling files)
- **Documentation**: Handler function has a doc comment explaining what it does, parameters, and error conditions
- **No explicit `.context()` at handler level**: The service method already wraps its errors with `.context()`. The handler just propagates with `?`, matching sibling GET handlers that delegate error context to the service layer.
