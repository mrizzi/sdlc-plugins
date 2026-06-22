# File 2: modules/fundamental/src/advisory/endpoints/severity_summary.rs (CREATE)

## Purpose

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary` that returns aggregated severity counts.

## Detailed Changes

Create a new endpoint handler file following the pattern in sibling `get.rs`:

```rust
use actix_web::web;
use axum::extract::{Path, State};
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::db::Transactional;
use common::error::AppError;
use common::model::Id;

/// Retrieve aggregated advisory severity counts for a specific SBOM.
///
/// Returns counts of advisories at each severity level (Critical, High, Medium, Low)
/// plus a total count. Returns 404 if the SBOM does not exist.
pub async fn get_advisory_summary(
    State(service): State<AdvisoryService>,
    Path(id): Path<Id>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to retrieve advisory severity summary")?;

    Ok(Json(summary))
}
```

## Conventions followed

- **Path extraction**: Uses `Path<Id>` matching sibling `get.rs` pattern
- **State extraction**: Uses `State<AdvisoryService>` for service access
- **Transaction**: Accepts `Transactional<'_>` parameter, passed through to service
- **Error handling**: Returns `Result<T, AppError>` with `.context()` wrapping, matching sibling handlers
- **Response**: Returns `Json<SeveritySummary>` directly -- Axum handles serialization
- **Documentation**: Function has `///` doc comment explaining behavior and error cases
- **Import organization**: Standard -> external -> internal grouping

## Notes

- The exact import paths and extractor types would be confirmed by inspecting sibling `get.rs` with Serena before implementation. The above is based on the conventions described in the repository structure document and task implementation notes.
- The handler delegates all business logic to the service layer, keeping the endpoint thin -- consistent with sibling endpoint handlers.
