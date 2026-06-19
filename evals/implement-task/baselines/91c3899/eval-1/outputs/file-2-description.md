# File 2: modules/fundamental/src/advisory/endpoints/severity_summary.rs

**Action**: CREATE

## Purpose

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary` that extracts the SBOM ID from the path, calls the `AdvisoryService::severity_summary` method, and returns the result as JSON.

## Sibling Reference

Modeled after `modules/fundamental/src/advisory/endpoints/get.rs` which handles `GET /api/v2/advisory/{id}`. The sibling pattern:
- Extracts path parameters via `Path<Id>`
- Calls the corresponding service method
- Returns `Result<Json<T>, AppError>` with `.context()` error wrapping

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

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated severity counts for all vulnerability advisories
/// linked to the specified SBOM. Deduplicates advisories by ID before counting.
pub async fn get_severity_summary(
    State(service): State<AdvisoryService>,
    Path(id): Path<Id>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    // When: retrieve severity summary from the service layer
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to retrieve advisory severity summary")?;

    // Then: return the summary as JSON
    Ok(Json(summary))
}
```

## Design Notes

- Follows the exact handler signature pattern from `get.rs`: extract `State`, `Path`, and `Transactional`
- The service method handles SBOM existence validation and returns a 404 via `AppError` if the SBOM is not found
- Error wrapping uses `.context()` matching the project convention from `common/src/error.rs`
- The handler is deliberately thin -- all business logic lives in the service layer
- Documentation comment on the handler function per code quality requirements
