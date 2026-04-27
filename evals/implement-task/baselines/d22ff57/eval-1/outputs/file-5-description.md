# File 5: modules/fundamental/src/advisory/endpoints/severity_summary.rs

## Action: CREATE

## Summary

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary` that extracts the
SBOM ID from the path, calls the `AdvisoryService::severity_summary` method, and returns
the `SeveritySummary` as JSON.

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

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a severity count summary (critical, high, medium, low, total) for all
/// advisories linked to the specified SBOM. Returns 404 if the SBOM does not exist.
pub async fn get_severity_summary(
    State(service): State<AdvisoryService>,
    Path(sbom_id): Path<Id>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(sbom_id, &tx)
        .await
        .context("failed to get severity summary")?;

    Ok(Json(summary))
}
```

## Design Decisions

- **Path extraction:** Uses `Path<Id>` to extract the SBOM ID from the URL path, following the pattern in `advisory/endpoints/get.rs` and `sbom/endpoints/get.rs`.
- **State extraction:** Uses `State<AdvisoryService>` to access the service instance, following Axum's dependency injection pattern.
- **Transaction propagation:** Accepts `Transactional<'_>` and passes it to the service, matching the existing handler pattern.
- **Error propagation:** Uses `.context()` for error wrapping, consistent with the `AppError` pattern in `common/src/error.rs`.
- **Return type:** Returns `Result<Json<SeveritySummary>, AppError>` -- Axum serializes the struct to JSON automatically.
- **Documentation:** Handler function has a doc comment describing the endpoint, HTTP method, and behavior.

## Conventions Applied

- **Handler pattern:** Matches the existing endpoint pattern in `advisory/endpoints/get.rs`: extract path params, call service, return JSON.
- **Error handling:** Uses `Result<T, AppError>` with `.context()` wrapping.
- **File organization:** One handler per file in the `endpoints/` directory.
- **Import style:** Groups Axum imports, then internal crate imports, then common imports.
