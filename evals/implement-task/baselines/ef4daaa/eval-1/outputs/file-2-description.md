# File 2: modules/fundamental/src/advisory/endpoints/severity_summary.rs

**Action**: CREATE

## Purpose

Implement the HTTP handler for `GET /api/v2/sbom/{id}/advisory-summary`. This endpoint receives an SBOM ID as a path parameter, calls the `AdvisoryService::severity_summary` method, and returns the `SeveritySummary` struct as JSON.

## Files inspected before writing

Before creating this file, the following siblings would be inspected:

- `modules/fundamental/src/advisory/endpoints/get.rs` -- PRIMARY PATTERN: `mcp__serena_backend__find_symbol("get", include_body=true)` to understand the exact handler signature, `Path<Id>` extraction, service injection pattern (`Extension<Arc<AdvisoryService>>`), transactional context usage, error handling, and return type
- `modules/fundamental/src/advisory/endpoints/list.rs` -- SECONDARY PATTERN: to confirm consistency across handlers in the same module
- `modules/fundamental/src/sbom/endpoints/get.rs` -- CROSS-DOMAIN REFERENCE: to understand how SBOM-scoped endpoints handle path parameters and 404 responses for non-existent SBOMs

## Conventions applied

- Handler function signature follows existing `get.rs` pattern
- `Path<Id>` extraction for the SBOM ID path parameter
- Service injected via `Extension<Arc<AdvisoryService>>` (or equivalent Axum state pattern)
- Returns `Result<Json<SeveritySummary>, AppError>`
- Error wrapping with `.context("Failed to fetch advisory severity summary")`
- 404 handling: if the SBOM does not exist, return `AppError::NotFound` (consistent with SBOM endpoints)

## Detailed changes

```rust
use axum::{
    extract::Path,
    Extension, Json,
};
use std::sync::Arc;

use crate::advisory::{
    model::severity_summary::SeveritySummary,
    service::AdvisoryService,
};
use common::error::AppError;
use common::db::Transactional;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated advisory severity counts for the given SBOM. Each severity
/// level (Critical, High, Medium, Low) is counted with deduplication by advisory ID.
/// Returns 404 if the SBOM does not exist.
pub async fn severity_summary(
    Path(sbom_id): Path<Id>,
    service: Extension<Arc<AdvisoryService>>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(sbom_id, &tx)
        .await
        .context("Failed to fetch advisory severity summary")?;

    Ok(Json(summary))
}
```

## Key design decisions

1. **SBOM-scoped path**: The endpoint is `GET /api/v2/sbom/{id}/advisory-summary`, not `/api/v2/advisory/...`, because it aggregates advisories *for a specific SBOM*. The path parameter is the SBOM ID.
2. **404 delegation**: The 404 for non-existent SBOMs is handled inside the service method (file 4), which returns an `AppError::NotFound` that propagates through the `?` operator. This matches the pattern where service methods validate entity existence.
3. **No pagination**: This endpoint returns a single summary object, not a list, so `PaginatedResults<T>` is not used. This follows the convention that single-entity responses return `Json<T>` directly.
4. **`context()` wrapping**: The `.context()` call adds a descriptive error message for debugging, following the `common/src/error.rs` pattern observed in sibling handlers.

## Integration points

- Registered in `endpoints/mod.rs` (file 5) as a route
- Calls `AdvisoryService::severity_summary()` (file 4)
- Returns `SeveritySummary` (file 1) as JSON
