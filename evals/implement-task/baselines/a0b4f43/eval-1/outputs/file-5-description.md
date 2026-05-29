# File 5: Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

## Purpose

GET handler for `/api/v2/sbom/{id}/advisory-summary` that returns aggregated severity counts.

## Pre-Change Analysis

Before creating, read the sibling endpoint handler `modules/fundamental/src/advisory/endpoints/get.rs` to understand:
- How `Path<Id>` is used to extract the SBOM ID from the URL
- How the `AdvisoryService` is obtained from Axum state/extensions
- The exact function signature and return type pattern
- How error responses (especially 404) are constructed

## Full File Content

```rust
use axum::{
    extract::{Path, State},
    Json,
};

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;
use common::db::Transactional;
use common::model::Id;

/// GET /api/v2/sbom/{id}/advisory-summary
///
/// Returns aggregated severity counts for advisories linked to the specified SBOM.
pub async fn get(
    State(service): State<AdvisoryService>,
    Path(id): Path<Id>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to retrieve severity summary")?;

    Ok(Json(summary))
}
```

## Design Notes

- Follows the exact same pattern as `advisory/endpoints/get.rs`: extract path param, call service, return JSON
- The `Transactional` extractor provides database transaction context, matching sibling handlers
- Error handling uses `.context()` wrapping and returns `Result<_, AppError>`, which Axum converts to appropriate HTTP error responses (404 for not-found, 500 for internal errors)
- The 404 behavior for non-existent SBOMs is handled by the service layer — if the SBOM does not exist, the query returns an error that maps to a 404 response through `AppError`
