# File 4: modules/fundamental/src/advisory/endpoints/severity_summary.rs

**Action**: CREATE

## Purpose

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary` that returns aggregated severity counts for advisories linked to a given SBOM.

## Sibling Reference

Follows the pattern established by:
- `modules/fundamental/src/advisory/endpoints/get.rs` -- GET handler for `/api/v2/advisory/{id}`
- `modules/fundamental/src/sbom/endpoints/get.rs` -- GET handler for `/api/v2/sbom/{id}`

Key patterns extracted from siblings:
- Path parameter extraction via `Path<Id>`
- Service invocation with transactional context
- JSON response via Axum's `Json` extractor
- Error handling returning `Result<Json<T>, AppError>`

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
use trustify_common::db::Transactional;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated severity counts (critical, high, medium, low, total)
/// for all unique advisories linked to the specified SBOM.
pub async fn get_severity_summary(
    State(service): State<AdvisoryService>,
    Path(sbom_id): Path<Id>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(sbom_id, &tx)
        .await?;

    Ok(Json(summary))
}
```

## Convention Conformance

- Follows the exact handler signature pattern from `get.rs`: extractors for state, path, and transactional context
- Returns `Result<Json<T>, AppError>` matching all sibling handlers
- Uses `State` extractor for the service (matching Axum state management pattern)
- Uses `Path<Id>` for the SBOM ID parameter
- Includes `///` doc comment on the handler function
- File is standalone (one handler per file) matching the sibling pattern of `get.rs` and `list.rs`
- Import paths follow the existing module structure

## Notes

- The exact import paths for `Id`, `Transactional`, and `AppError` would be confirmed by reading the actual `get.rs` sibling file with Serena before implementing. The patterns shown above follow the task's Implementation Notes.
- The endpoint path (`/api/v2/sbom/{id}/advisory-summary`) is registered in `endpoints/mod.rs` (see file-5-description.md), not in this file.
