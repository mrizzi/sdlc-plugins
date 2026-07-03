# File 2: modules/fundamental/src/advisory/endpoints/severity_summary.rs

## Action: CREATE

## Purpose
Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary` that extracts the SBOM ID from the path, calls the service layer, and returns the severity summary as JSON.

## Detailed Changes

Create a new file following the pattern established in `advisory/endpoints/get.rs`:

```rust
use axum::extract::Path;
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::db::Transactional;
use common::error::AppError;
use common::model::Id;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated severity counts for all vulnerability advisories
/// linked to the specified SBOM. Returns 404 if the SBOM does not exist.
pub async fn get(
    service: axum::extract::Extension<AdvisoryService>,
    Path(id): Path<Id>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("failed to compute advisory severity summary")?;

    Ok(Json(summary))
}
```

## Conventions Applied
- **Handler signature**: Follows the exact pattern from `get.rs` -- extract path params via `Path<Id>`, accept `Transactional` for database access, return `Result<Json<T>, AppError>`.
- **Error handling**: Uses `.context()` wrapping on the service call result, matching the error handling convention in all existing handlers.
- **Service injection**: Uses `axum::extract::Extension<AdvisoryService>` to receive the service instance, matching how other handlers obtain their service.
- **Documentation**: Doc comment on the handler function explaining the endpoint's purpose and behavior.
- **Import organization**: External crate imports (`axum`) first, then local module imports.
- **File naming**: Named `severity_summary.rs` matching the endpoint concept, consistent with `get.rs` and `list.rs` in the same directory.
