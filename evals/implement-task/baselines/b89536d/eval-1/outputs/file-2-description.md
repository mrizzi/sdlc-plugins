# File 2: modules/fundamental/src/advisory/endpoints/severity_summary.rs (CREATE)

## Purpose

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary`. This handler extracts
the SBOM ID from the path, calls the service layer to compute severity counts, and returns
the result as JSON.

## Detailed Changes

```rust
use axum::{
    extract::Path,
    Json,
};
use crate::advisory::service::AdvisoryService;
use crate::advisory::model::severity_summary::SeveritySummary;
use common::error::AppError;
use common::db::Transactional;

/// Handles GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a severity count summary for all unique advisories linked to the given SBOM.
/// Returns 404 if the SBOM ID does not exist.
pub async fn get_advisory_summary(
    service: /* Axum state extractor for AdvisoryService */,
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

## Pattern references

- Follows `advisory/endpoints/get.rs` pattern: extract `Path<Id>`, call service method, return `Json<T>`
- Uses `.context()` wrapping for error handling (matches `common/src/error.rs` pattern)
- The service's `severity_summary` method returns `Err(AppError::NotFound)` when the SBOM
  does not exist, which Axum translates to a 404 response via the `IntoResponse` impl

## Conventions followed

- Handler is a standalone async function (not a method on a struct)
- Return type is `Result<Json<T>, AppError>` (matches all sibling handlers)
- Error context string describes the operation in present participle
- Doc comment on the public function explaining the endpoint and error behavior
- Imports follow standard -> external -> internal ordering
