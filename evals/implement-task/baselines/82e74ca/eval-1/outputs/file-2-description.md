# File 2: modules/fundamental/src/advisory/endpoints/severity_summary.rs

**Action**: CREATE

## Purpose

Define the Axum GET handler for `GET /api/v2/sbom/{id}/advisory-summary`. This handler extracts the SBOM ID from the path, calls the `AdvisoryService::severity_summary` method, and returns the `SeveritySummary` as a JSON response.

## Conventions Applied

- **Handler pattern**: Follows the pattern in sibling `get.rs` -- extract path params via `Path<Id>`, call service, return `Json<T>`
- **Error handling**: Returns `Result<Json<SeveritySummary>, AppError>` with `.context()` wrapping, matching `common/src/error.rs`
- **Import organization**: Groups standard library, external crates, then internal modules
- **Doc comments**: Documentation on the handler function per SKILL.md requirement

## Detailed Changes

```rust
use axum::extract::Path;
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;
use common::db::Transactional;

/// Handler for `GET /api/v2/sbom/{id}/advisory-summary`.
///
/// Returns aggregated severity counts for all vulnerability advisories
/// linked to the specified SBOM. Returns 404 if the SBOM does not exist.
pub async fn get_severity_summary(
    service: axum::extract::Extension<AdvisoryService>,
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

## Design Decisions

1. **Extension extractor for service**: Follows how other handlers in the advisory module access the `AdvisoryService` -- via Axum's `Extension` or state extractor (exact mechanism depends on codebase; would verify from sibling `get.rs` during actual implementation).
2. **`Path<Id>` extractor**: Consistent with the pattern referenced in Implementation Notes and used by `get.rs`.
3. **`.context()` wrapping**: Provides descriptive error context per the error handling convention.
4. **404 handling**: The `AdvisoryService::severity_summary` method returns an `AppError` with 404 status when the SBOM is not found. The handler propagates this via `?`.
5. **No pagination**: This is a single-object response (aggregation result), not a list -- so `PaginatedResults<T>` is not used.

## Notes

- The exact import paths and extractor types would be verified against the actual `get.rs` handler during implementation using Serena's `get_symbols_overview` and `find_symbol`.
- If the codebase uses Axum's `State` extractor instead of `Extension`, the handler signature would be adjusted accordingly.
