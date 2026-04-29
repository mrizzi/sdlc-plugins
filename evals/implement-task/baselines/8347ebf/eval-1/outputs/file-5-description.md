# File 5: modules/fundamental/src/advisory/endpoints/severity_summary.rs

## Change Type: Create

## Purpose

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary` that extracts the SBOM ID from the path, calls the `AdvisoryService::severity_summary` method, and returns the `SeveritySummary` as a JSON response.

## Detailed Changes

### Full file content

```rust
use axum::extract::{Path, State};
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::db::Transactional;
use common::error::AppError;
use common::model::Id;

/// Handler for `GET /api/v2/sbom/{id}/advisory-summary`.
///
/// Returns aggregated advisory severity counts for the specified SBOM,
/// including counts per severity level (Critical, High, Medium, Low) and a total.
pub async fn get_severity_summary(
    State(service): State<AdvisoryService>,
    Path(id): Path<Id>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("failed to get severity summary")?;

    Ok(Json(summary))
}
```

## Conventions Applied

- **Path parameter extraction**: Uses `Path<Id>` extractor matching the pattern in `modules/fundamental/src/advisory/endpoints/get.rs`
- **State extraction**: Uses `State<AdvisoryService>` to get the shared service instance, matching sibling handlers
- **Transaction parameter**: Includes `tx: Transactional<'_>` as the last parameter, matching sibling handler signatures
- **Return type**: `Result<Json<SeveritySummary>, AppError>` -- matches the pattern where single-item responses use `Json<T>` directly (not `PaginatedResults`)
- **Error handling**: Uses `.context()` wrapping on the service call, consistent with all existing handlers
- **Documentation**: `///` doc comment on the handler function explaining what it does
- **Import organization**: Grouped by external crate (axum), then internal crate modules, then common crate

## Sibling Parity

Compared against sibling endpoint files:
- `modules/fundamental/src/advisory/endpoints/get.rs` -- same parameter extraction pattern, same return type pattern, same error handling
- `modules/fundamental/src/advisory/endpoints/list.rs` -- similar structure (but uses `PaginatedResults` since it's a list endpoint)
- `modules/fundamental/src/sbom/endpoints/get.rs` -- same pattern for single-item retrieval

The new handler follows the same conventions as all siblings. No cross-cutting concerns (logging, caching) are missing compared to siblings -- if sibling `get.rs` handlers include specific middleware or tracing, that would be replicated here as well (to be confirmed during actual code inspection).

## Data-flow Completeness

- Input: HTTP GET request with SBOM ID path parameter -- extracted via `Path<Id>`
- Processing: Delegates to `AdvisoryService::severity_summary` which queries DB
- Output: Returns `Json<SeveritySummary>` or `AppError` (404 for missing SBOM)
- All stages connected -- data flow is COMPLETE
