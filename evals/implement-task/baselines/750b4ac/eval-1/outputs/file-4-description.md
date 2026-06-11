# File 4: `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (CREATE)

## Purpose

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary` that extracts the
SBOM ID from the path, calls the `AdvisoryService::severity_summary` method, and returns
the `SeveritySummary` as JSON.

## Detailed Changes

Create a new file with the following contents:

```rust
//! GET handler for advisory severity summary endpoint.
//!
//! Returns aggregated severity counts for advisories linked to a given SBOM.

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use actix_web::web; // or axum extractors, depending on actual framework usage
use axum::{
    extract::{Path, State},
    Json,
};
use common::error::AppError;
use trustify_common::db::Transactional;

/// Handle GET /api/v2/sbom/{id}/advisory-summary.
///
/// Extracts the SBOM ID from the path, invokes the advisory service to
/// compute severity counts, and returns the aggregated summary as JSON.
/// Returns 404 if the SBOM does not exist.
pub async fn get_severity_summary(
    State(service): State<AdvisoryService>,
    Path(id): Path<Id>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("fetching advisory severity summary")?;

    Ok(Json(summary))
}
```

**Note**: The exact extractor types (`State`, `Path`, `Id`, `Transactional`) and import
paths would be confirmed by reading the actual `advisory/endpoints/get.rs` sibling file
via Serena. The pattern above follows the Implementation Notes instruction to:
- Extract path params via `Path<Id>`
- Call service method
- Return JSON (Axum's `Json` extractor handles serialization)
- Wrap errors with `.context()` matching the `AppError` pattern

## Conventions Applied

- **Handler signature**: async function taking Axum extractors and returning `Result<Json<T>, AppError>`, matching `get.rs` pattern
- **Path extraction**: `Path<Id>` for the SBOM ID, matching existing endpoint patterns
- **Error handling**: `.context()` wrapping for descriptive error messages
- **Direct return**: returns `Json<SeveritySummary>` directly (no manual serialization)
- **Documentation**: `///` doc comment on the handler function
- **Module-level docs**: `//!` doc comment at the top
