# File 4: modules/fundamental/src/advisory/endpoints/severity_summary.rs (CREATE)

## Purpose

Define the GET handler for `/api/v2/sbom/{id}/advisory-summary` that extracts the SBOM ID from the path, calls `AdvisoryService::severity_summary`, and returns the `SeveritySummary` as JSON.

## Detailed Changes

Create a new file following the pattern of `get.rs` in the same directory:

```rust
//! GET handler for advisory severity summary.
//!
//! Returns aggregated advisory severity counts for a given SBOM.

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use axum::extract::{Path, State};
use axum::Json;
use common::error::AppError;
use common::db::Transactional;

/// Returns the advisory severity summary for the specified SBOM.
///
/// Responds with a JSON object containing counts per severity level
/// (critical, high, medium, low) and a total count.
///
/// # Errors
///
/// Returns 404 if the SBOM ID does not exist.
pub async fn get_advisory_summary(
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

## Convention Conformance

- **Handler signature**: Follows the exact pattern in `get.rs` -- `Path<Id>` for path parameter extraction, `State` for service injection, returns `Result<Json<T>, AppError>`.
- **Error propagation**: Uses `?` operator to propagate `AppError` from the service layer, matching sibling handlers.
- **Response type**: Returns the struct directly wrapped in `Json`, as specified in implementation notes ("Axum's `Json` extractor handles serialization").
- **Documentation**: Full `///` doc comment on the handler function explaining behavior and error semantics.
- **Module-level docs**: `//!` doc comment at the top of the file.
- **Import organization**: Standard Rust convention -- external crates first, internal modules second.

## Notes

The exact parameter types (`Id`, `Transactional`) and state extraction pattern would be confirmed by reading `get.rs` during Step 4. The code above represents the intended pattern; adjustments would be made based on actual sibling inspection.
