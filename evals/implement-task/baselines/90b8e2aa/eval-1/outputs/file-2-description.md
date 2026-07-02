# File 2: modules/fundamental/src/advisory/endpoints/severity_summary.rs (CREATE)

## Purpose

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary` that extracts the SBOM ID from the path, calls the `AdvisoryService::severity_summary` method, and returns the `SeveritySummary` as JSON.

## Pre-implementation Inspection

Before creating this file, inspect the sibling endpoint file to confirm the exact handler pattern:
- Use `mcp__serena_backend__find_symbol` with `include_body=true` on the handler function in `modules/fundamental/src/advisory/endpoints/get.rs` to see the full implementation: Path extraction, State usage, service call, error handling, and return type
- Use `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/list.rs` to see the list handler pattern for comparison
- Confirm the exact `Path<T>` type used for ID parameters and the `State<T>` type for accessing the service

## Planned Content

```rust
use axum::{
    extract::{Path, State},
    Json,
};

use crate::advisory::{
    model::severity_summary::SeveritySummary,
    service::AdvisoryService,
};
use common::error::AppError;
use trustify_common::db::Transactional;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a severity breakdown of advisories linked to the specified SBOM,
/// with counts per severity level and a deduplicated total.
pub async fn get_severity_summary(
    State(service): State<AdvisoryService>,
    Path(sbom_id): Path<Id>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(&sbom_id, &tx)
        .await
        .context("Failed to retrieve severity summary")?;

    Ok(Json(summary))
}
```

## Design Decisions

- **Handler signature**: Follows the exact pattern from `get.rs` -- `Path(id)` for path extraction, `State(service)` for the advisory service, transactional parameter
- **Error handling**: Uses `.context()` wrapping to produce descriptive `AppError` messages, matching the convention in `common/src/error.rs`
- **Return type**: `Result<Json<SeveritySummary>, AppError>` -- Axum handles serialization via `Json` and error conversion via `IntoResponse` on `AppError`
- **Doc comment**: Per code quality requirements, the handler has a `///` doc comment explaining what it does

## Notes

- The exact import paths and type names (`Id`, `Transactional`, `State`) will be confirmed by inspecting `get.rs` before implementation
- If `get.rs` uses a different state extraction pattern (e.g., `Extension` instead of `State`), the handler will be adjusted to match
- The handler does not need explicit 404 logic -- the service layer returns an `AppError` variant that maps to 404 when the SBOM is not found

## Conventions Applied

- Async handler function with Axum extractors
- Error handling via `.context()` on the `Result` chain
- `Json<T>` wrapper for response serialization
- Module declared in parent `mod.rs` (see file-5-description.md)
