# File 2: modules/fundamental/src/advisory/endpoints/severity_summary.rs

**Action**: CREATE

**Purpose**: Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary` that calls the service method and returns the aggregated severity counts as JSON.

## Detailed Changes

Create a new file with the following contents:

```rust
//! Endpoint handler for advisory severity summary aggregation.

use actix_web::web;
use axum::{
    extract::Path,
    Json,
};

use crate::advisory::{
    model::severity_summary::SeveritySummary,
    service::AdvisoryService,
};
use common::error::AppError;
use common::db::Transactional;

/// Returns aggregated advisory severity counts for the specified SBOM.
///
/// Queries all advisories linked to the given SBOM via the `sbom_advisory` join
/// table, deduplicates by advisory ID, and counts occurrences per severity level
/// (Critical, High, Medium, Low). Returns a `SeveritySummary` with per-level
/// counts and a total.
///
/// Returns 404 if the SBOM ID does not exist.
pub async fn get_severity_summary(
    service: web::Data<AdvisoryService>,
    Path(sbom_id): Path<Id>,
    tx: web::Data<Transactional<'_>>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(sbom_id, &tx)
        .await
        .context("fetching advisory severity summary")?;

    Ok(Json(summary))
}
```

## Conventions Followed

- **Handler pattern**: follows the existing pattern in `advisory/endpoints/get.rs` -- extract path params via `Path<Id>`, call service method, return `Json<T>`.
- **Return type**: `Result<Json<SeveritySummary>, AppError>` matching sibling handlers.
- **Error handling**: `.context("descriptive message")` wrapping, matching the pattern from `common/src/error.rs`.
- **Documentation**: doc comment on the public function explaining what it does, parameters, and error behavior.
- **Import organization**: framework imports first (axum), then crate imports, then local module imports.

## Notes

- The exact import paths and parameter types (e.g., `web::Data` vs direct injection) would be confirmed by inspecting the actual `get.rs` sibling via Serena's `find_symbol` with `include_body=true`. The above is representative of the pattern described in the task and repo structure.
- The `Id` type would be the same type used in sibling endpoint handlers.
