# File 5: modules/fundamental/src/advisory/endpoints/severity_summary.rs

**Action**: Create (new file)
**Purpose**: GET handler for /api/v2/sbom/{id}/advisory-summary

## Pre-Implementation Inspection

Before creating, would use Serena to inspect sibling endpoint files:
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/get.rs` -- understand the existing GET handler pattern (Path extraction, service call, JSON return)
- `mcp__serena_backend__find_symbol` on the `get` handler function in `get.rs` with `include_body=true` -- read full handler implementation
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/list.rs` -- understand list handler pattern for comparison
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/sbom/endpoints/get.rs` -- cross-domain handler comparison
- `mcp__serena_backend__search_for_pattern` for `Path<` in advisory/endpoints/ -- understand path parameter extraction pattern

## File Contents

```rust
use axum::extract::Path;
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;
use common::db::Transactional;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns an aggregated severity summary for all advisories linked to the
/// specified SBOM, including counts per severity level and a total count.
pub async fn get_severity_summary(
    service: axum::Extension<AdvisoryService>,  // or State<AppState> depending on sibling pattern
    Path(sbom_id): Path<Id>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(sbom_id, &tx)
        .await
        .context("Failed to fetch advisory severity summary")?;

    Ok(Json(summary))
}
```

## Key Patterns Followed

- **Path extraction**: Uses `Path<Id>` extractor matching the pattern in `advisory/endpoints/get.rs` per Implementation Notes.
- **Service injection**: Would verify from siblings whether the service is injected via `axum::Extension`, `State<AppState>`, or another pattern. Follow whatever siblings use.
- **Transaction context**: Passes `&Transactional<'_>` to the service method matching the existing service method pattern.
- **Error handling**: Returns `Result<Json<T>, AppError>` with `.context()` wrapping, matching the convention from `common/src/error.rs`.
- **Return type**: Returns `Json<SeveritySummary>` directly -- Axum handles serialization. Not paginated since this is a single aggregate result.
- **Documentation**: Handler function has a `///` doc comment describing the endpoint.
- **Import organization**: Standard library, then external crates (axum), then internal modules (crate::, common::).

## Notes

- The exact service injection mechanism (Extension vs State) would be determined by inspecting the sibling `get.rs` handler.
- The `Id` type import would be determined from sibling usage.
- Additional middleware or extractors (e.g., authentication) would be replicated from siblings if present.
