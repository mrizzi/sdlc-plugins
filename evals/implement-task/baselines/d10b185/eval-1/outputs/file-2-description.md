# File 2: modules/fundamental/src/advisory/endpoints/severity_summary.rs

**Action**: CREATE

## Purpose

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary` that calls the service layer and returns the `SeveritySummary` as JSON.

## Detailed Changes

Create a new file with the following contents:

```rust
use axum::{
    extract::{Path, State},
    Json,
};
use uuid::Uuid;

use crate::advisory::{
    model::severity_summary::SeveritySummary,
    service::AdvisoryService,
};
use common::error::AppError;
use common::db::Transactional;

/// GET /api/v2/sbom/{id}/advisory-summary
///
/// Returns aggregated severity counts for advisories linked to the given SBOM.
pub async fn get_severity_summary(
    State(service): State<AdvisoryService>,
    Path(id): Path<Uuid>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &Transactional::None)
        .await
        .context("Failed to fetch advisory severity summary")?;

    Ok(Json(summary))
}
```

## Conventions Applied

- **Handler signature**: Follows the exact pattern from `advisory/endpoints/get.rs` -- async function taking `State` and `Path` extractors, returning `Result<Json<T>, AppError>`.
- **Path extractor**: Uses `Path<Uuid>` (or `Path<Id>` if the codebase uses a type alias) to extract the SBOM ID from the URL, matching the sibling `get.rs` handler.
- **Error handling**: Uses `.context()` wrapping before `?` propagation, consistent with the error handling convention in `common/src/error.rs`. If the service returns `None` for a non-existent SBOM, the service method itself will return an `AppError` 404 (see file-4-description.md).
- **No pagination**: This is a single-resource aggregation endpoint, not a list, so it returns `Json<SeveritySummary>` directly rather than `PaginatedResults<T>`.
- **Transaction context**: Passes `Transactional::None` for a read-only operation, matching the pattern in sibling GET handlers.
