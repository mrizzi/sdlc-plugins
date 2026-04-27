# File 5 -- Create: `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

## Purpose

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary`. This endpoint
extracts the SBOM ID from the path, calls `AdvisoryService::severity_summary`, and
returns the result as JSON.

## Pre-Implementation Inspection

Before creating, inspect sibling endpoint files to match conventions:
- `modules/fundamental/src/advisory/endpoints/get.rs` -- primary pattern reference for
  single-resource endpoint with `Path<Id>` extraction.
- `modules/fundamental/src/sbom/endpoints/get.rs` -- cross-module sibling for
  additional pattern validation.
- `modules/fundamental/src/advisory/endpoints/list.rs` -- to understand list patterns
  and confirm the single-resource pattern is different.

## Full File Content

```rust
//! Handler for the advisory severity summary endpoint.

use axum::{
    extract::Path,
    Json,
};
use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;
use common::db::Transactional;

/// Handles GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated severity counts for advisories linked to the specified
/// SBOM. Advisories are deduplicated by advisory ID before counting.
///
/// Returns 404 if the specified SBOM does not exist.
pub async fn handler(
    Path(id): Path<Id>,
    service: AdvisoryService,
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

- **Handler function named `handler`**: follows the convention seen in sibling endpoint files
  where each file exports a single `handler` (or `get`, `list`) function. The module name
  (`severity_summary`) provides the namespace.
- **`Path<Id>` extraction**: matches the pattern in `advisory/endpoints/get.rs` and
  `sbom/endpoints/get.rs`.
- **`AdvisoryService` as extractor**: Axum state extraction pattern matching sibling handlers.
- **`Transactional<'_>`**: database transaction context matching sibling handler signatures.
- **Error propagation**: `.context()` wrapping matching the established error handling pattern.
- **No pagination**: this is an aggregation endpoint returning a single summary object, not a
  list, so `PaginatedResults` is not used.

## Conventions Applied

- Return type: `Result<Json<T>, AppError>`.
- Error wrapping with `.context()`.
- Doc comment on the handler function explaining the endpoint behavior and error cases.
- Module-level doc comment (`//!`).
- Import organization: standard library, external crates, then local crate imports.

## Notes

- The exact import paths for `Id`, `Transactional`, `AdvisoryService`, and `AppError` will be
  confirmed by inspecting the sibling `get.rs` file at implementation time. The paths above
  are based on the repository structure and conventions described in the repo documentation.
- The `context()` call requires `use anyhow::Context;` -- this import may already be in scope
  via a prelude or must be added explicitly, following the pattern in sibling files.
