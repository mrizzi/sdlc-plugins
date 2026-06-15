# File 2: modules/fundamental/src/advisory/endpoints/severity_summary.rs (CREATE)

## Purpose

GET handler for `/api/v2/sbom/{id}/advisory-summary` that returns aggregated severity counts for advisories linked to a given SBOM.

## Detailed Changes

Create a new file with the following content:

```rust
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

/// Handler for `GET /api/v2/sbom/{id}/advisory-summary`.
///
/// Returns aggregated severity counts (critical, high, medium, low, total)
/// for all unique advisories linked to the specified SBOM.
pub async fn handler(
    Path(id): Path<Id>,
    service: AdvisoryService,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to retrieve advisory severity summary")?;

    Ok(Json(summary))
}
```

## Conventions Applied

- **Path extraction**: Uses `Path<Id>` matching the pattern in `advisory/endpoints/get.rs`.
- **Service call pattern**: Calls `service.severity_summary(id, &tx)` following the same `(id, &tx)` parameter pattern as `fetch` and `list` methods.
- **Return type**: `Result<Json<SeveritySummary>, AppError>` matching sibling handlers.
- **Error handling**: Uses `.context()` wrapping on the service call, matching the pattern in sibling endpoint handlers and `common/src/error.rs`.
- **Documentation**: Doc comment on the handler function explaining what it does.

## Notes

- The exact parameter types for the Axum extractors (e.g., how `AdvisoryService` and `Transactional` are injected) would be confirmed by reading the existing `get.rs` handler during Step 4. The pattern shown above follows the structure described in the task's Implementation Notes.
- If the SBOM ID does not exist, the service method returns an appropriate error that maps to HTTP 404 via `AppError`'s `IntoResponse` implementation, consistent with existing SBOM endpoints.
