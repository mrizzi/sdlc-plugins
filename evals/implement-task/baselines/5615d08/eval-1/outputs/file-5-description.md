# File 5: `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

**Action**: Create

## What Changes

Create a GET handler for the `/api/v2/sbom/{id}/advisory-summary` endpoint. The handler extracts the SBOM ID from the path, calls the service method, and returns the severity summary as JSON.

## Full File Content

```rust
//! Advisory severity summary endpoint.
//!
//! Provides a GET handler that returns aggregated advisory severity counts
//! for a given SBOM.

use axum::{
    extract::{Path, State},
    Json,
};
use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::db::Transactional;
use common::error::AppError;
use common::model::Id;

/// Returns aggregated advisory severity counts for the specified SBOM.
///
/// Queries all advisories linked to the SBOM via the `sbom_advisory` join table,
/// deduplicates by advisory ID, and returns counts per severity level
/// (critical, high, medium, low) along with a total.
///
/// Returns 404 if the SBOM does not exist.
pub async fn get_severity_summary(
    State(service): State<AdvisoryService>,
    Path(id): Path<Id>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await?;

    Ok(Json(summary))
}
```

## Patterns Followed

- Follows the exact pattern from `modules/fundamental/src/advisory/endpoints/get.rs`:
  - Extract path params via `Path<Id>`
  - Extract service via `State<AdvisoryService>`
  - Accept `Transactional<'_>` for database access
  - Call service method
  - Return `Result<Json<T>, AppError>`
- Error handling is delegated to the service layer (which returns `AppError` with `.context()` wrapping)
- Module-level doc comment (`//!`) describing the endpoint
- Function-level doc comment describing behavior, return value, and error cases
