# File 2: modules/fundamental/src/advisory/endpoints/severity_summary.rs

**Action**: CREATE

## Purpose

Define the HTTP handler for `GET /api/v2/sbom/{id}/advisory-summary`. This handler
extracts the SBOM ID from the path, delegates to `AdvisoryService::severity_summary()`,
and returns the result as JSON.

## Detailed Changes

Create a new file following the pattern in `advisory/endpoints/get.rs`:

```rust
use axum::extract::Path;
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;
use common::db::Transactional;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated advisory severity counts for the specified SBOM,
/// enabling dashboard widgets to render severity breakdowns without
/// client-side counting.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: AdvisoryService,
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

- **Parameter extraction**: Uses `Path<Id>` for the SBOM ID, matching the pattern in `get.rs`.
- **Service call**: Delegates to the service layer, passing `id` and `&tx` as parameters, matching the `fetch` and `list` method call patterns.
- **Return type**: `Result<Json<SeveritySummary>, AppError>` -- returns the struct directly via Axum's `Json` extractor, consistent with single-entity endpoint patterns.
- **Error handling**: Uses `.context()` wrapping for descriptive error messages, matching the error handling convention in `common/src/error.rs`.
- **Documentation**: Handler function has a `///` doc comment explaining the endpoint purpose.
- **File placement**: Own file in `endpoints/` directory, matching `get.rs` and `list.rs` siblings.

## Notes

- The handler does NOT return `PaginatedResults<T>` because this is an aggregation endpoint returning a single summary, not a list. This is consistent with how `get.rs` returns a single entity directly.
- 404 handling for non-existent SBOMs is done in the service layer (the service method checks SBOM existence before querying advisories and returns an appropriate error).
