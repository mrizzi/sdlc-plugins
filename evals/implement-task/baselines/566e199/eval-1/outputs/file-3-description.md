# File 3: modules/fundamental/src/advisory/endpoints/severity_summary.rs (CREATE)

## Purpose
Define the GET handler for the `/api/v2/sbom/{id}/advisory-summary` endpoint.

## Detailed Changes

### Handler function: `severity_summary`

```rust
use axum::extract::Path;
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;
use common::db::Transactional;

/// Handle GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated severity counts for all advisories linked to the
/// specified SBOM. The response includes counts per severity level
/// (critical, high, medium, low) and a total count.
pub async fn severity_summary(
    Path(sbom_id): Path<Id>,
    service: Extension<AdvisoryService>,  // or State, matching sibling pattern
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(sbom_id, &tx)
        .await
        .context("Failed to compute advisory severity summary")?;

    Ok(Json(summary))
}
```

### Design decisions

1. **Path parameter extraction**: Uses `Path<Id>` matching the pattern in `modules/fundamental/src/advisory/endpoints/get.rs`.
2. **Service injection**: Uses the same injection pattern (likely `Extension` or `State`) as sibling handlers in `get.rs` and `list.rs`.
3. **Return type**: `Result<Json<SeveritySummary>, AppError>` -- Axum's `Json` extractor handles serialization. `AppError` implements `IntoResponse` for error mapping.
4. **Error context**: `.context()` wrapping matches the established error handling convention.
5. **No pagination**: This returns a single summary object, not a list, so `PaginatedResults` is not used.

### Conventions followed
- **Handler signature**: matches `get.rs` handler -- `Path` extractor, service injection, `Transactional`, returns `Result<Json<T>, AppError>`.
- **Error handling**: `.context()` wrapping for descriptive error messages.
- **Import organization**: standard library first, external crates, then internal modules.
- **Documentation**: `///` doc comment on the handler function.
- **File naming**: `severity_summary.rs` matches the handler-per-file pattern (`get.rs`, `list.rs`).
