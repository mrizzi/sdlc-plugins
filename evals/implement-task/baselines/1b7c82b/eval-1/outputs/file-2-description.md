# File 2: modules/fundamental/src/advisory/endpoints/severity_summary.rs

## Action: CREATE

## Purpose

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary`. This endpoint receives an SBOM ID as a path parameter, calls `AdvisoryService::severity_summary`, and returns the severity counts as JSON.

## Detailed Changes

### Handler Function

```rust
use axum::extract::Path;
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;
use common::db::Transactional;

/// Returns aggregated advisory severity counts for the specified SBOM.
///
/// Queries all advisories linked to the given SBOM, deduplicates by advisory ID,
/// and returns counts per severity level (Critical, High, Medium, Low) plus a total.
pub async fn get_severity_summary(
    Path(sbom_id): Path<Id>,
    service: AdvisoryService,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(sbom_id, &tx)
        .await
        .context("fetching severity summary for SBOM")?;

    Ok(Json(summary))
}
```

### Design Decisions

- **Pattern match**: Follows the exact pattern observed in `endpoints/get.rs` -- extract `Path<Id>`, call service, return `Json<T>`
- **Error handling**: Uses `Result<T, AppError>` with `.context()` wrapping, matching the established convention from `common/src/error.rs`
- **404 handling**: The `AdvisoryService::severity_summary` method will return an `AppError` with a 404 status when the SBOM ID is not found, consistent with existing SBOM endpoint behavior. The error propagates naturally through the `?` operator.
- **No pagination**: This endpoint returns a single summary object (not a list), so `PaginatedResults<T>` is not used. This is correct since the response is always exactly one object with five numeric fields.
- **Doc comment**: Function has a documentation comment explaining what it does, per implement-task requirements.

### Conventions Applied

- Handler signature matches `endpoints/get.rs` pattern (Path extractor, service injection, transactional context)
- Error wrapping uses `.context()` as per `common/src/error.rs` convention
- File name matches the model/feature name (`severity_summary.rs`)
- Import organization follows the pattern: external crate imports, then internal module imports
