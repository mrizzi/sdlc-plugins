# File 2: `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (CREATE)

## Purpose

Define the Axum GET handler for `GET /api/v2/sbom/{id}/advisory-summary`. This handler extracts the SBOM ID from the path, calls the service method, and returns the `SeveritySummary` as JSON.

## Conventions Applied

- Follows the exact handler signature pattern from `endpoints/get.rs` (Path extractor, State extractor, Transactional parameter)
- Returns `Result<Json<SeveritySummary>, AppError>` -- matching sibling endpoint return types
- Uses `.context()` for error wrapping -- matching the error handling pattern from `common/src/error.rs`
- Function is `pub async fn` -- matching sibling handlers

## Detailed Content

```rust
use axum::extract::{Path, State};
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use trustify_common::db::Transactional;
use trustify_common::error::AppError;
use trustify_common::id::Id;

/// GET /api/v2/sbom/{id}/advisory-summary
///
/// Returns aggregated severity counts for all advisories linked to the given SBOM.
#[utoipa::path(
    get,
    path = "/api/v2/sbom/{id}/advisory-summary",
    params(
        ("id" = Id, Path, description = "The SBOM identifier"),
    ),
    responses(
        (status = 200, description = "Severity summary for the SBOM", body = SeveritySummary),
        (status = 404, description = "SBOM not found"),
    ),
)]
pub async fn severity_summary(
    Path(id): Path<Id>,
    State(service): State<AdvisoryService>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .get_severity_summary(id, &tx)
        .await
        .context("Failed to compute advisory severity summary")?;

    Ok(Json(summary))
}
```

## Design Decisions

1. **`#[utoipa::path]` annotation**: Provides OpenAPI documentation generation, consistent with other endpoints that use this pattern for API docs.

2. **Error propagation with `.context()`**: Wraps the service error with a descriptive message. The service layer handles 404 logic (returning `AppError::NotFound` when the SBOM does not exist), so the handler propagates with additional context.

3. **`Transactional<'_>` as parameter**: Follows the convention observed in sibling handlers where the transaction context is passed through to the service layer rather than being created in the handler.

4. **No pagination**: This endpoint returns a single summary object, not a list, so `PaginatedResults` is not used -- consistent with the API contract `{ critical: N, high: N, medium: N, low: N, total: N }`.
