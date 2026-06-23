# File 2: modules/fundamental/src/advisory/endpoints/severity_summary.rs

**Action:** CREATE

## Purpose

Define the GET handler for `/api/v2/sbom/{id}/advisory-summary`. This endpoint extracts the SBOM ID from the path, calls `AdvisoryService::severity_summary()`, and returns the `SeveritySummary` as JSON.

## Detailed Changes

```rust
use crate::advisory::{
    model::severity_summary::SeveritySummary,
    service::AdvisoryService,
};
use axum::{
    extract::{Path, State},
    Json,
};
use common::error::AppError;
use sea_orm::prelude::Uuid;
use trustify_common::db::Transactional;

/// Handler for `GET /api/v2/sbom/{id}/advisory-summary`.
///
/// Returns aggregated severity counts for all unique advisories linked to the
/// specified SBOM. Returns 404 if the SBOM does not exist.
pub async fn get_severity_summary(
    State(service): State<AdvisoryService>,
    Path(id): Path<Uuid>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to fetch advisory severity summary")?;

    Ok(Json(summary))
}
```

## Conventions Applied

- **Path parameter extraction:** Uses `Path<Uuid>` (or `Path<Id>` depending on the existing `Id` type alias) matching the pattern in `advisory/endpoints/get.rs`
- **State extraction:** Uses `State(service)` to access the `AdvisoryService`, following sibling endpoint handlers
- **Error handling:** Returns `Result<T, AppError>` with `.context()` wrapping, matching the established pattern from `common/src/error.rs`
- **Return type:** Returns `Json<SeveritySummary>` directly, letting Axum handle serialization per task implementation notes
- **Transactional parameter:** Accepts `Transactional<'_>` matching sibling handler signatures
- **Documentation:** Handler function has a doc comment describing what it does
- **Import organization:** Standard Rust convention -- external crates, then internal modules

## Notes

- The exact import paths and type aliases (e.g., `Uuid` vs a project-specific `Id` type) would be confirmed by inspecting sibling files with Serena during Step 4
- The `.context()` call requires `use anyhow::Context;` or equivalent -- would verify which error context trait the project uses
