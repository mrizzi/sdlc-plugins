# File 4: modules/fundamental/src/advisory/endpoints/severity_summary.rs (CREATE)

## Purpose

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary` that extracts path parameters, calls the service method, and returns the JSON response.

## Detailed Changes

Create a new endpoint handler file following the pattern in `get.rs`:

```rust
use axum::{
    extract::Path,
    Json,
};
use crate::advisory::service::AdvisoryService;
use crate::advisory::model::severity_summary::SeveritySummary;
use common::error::AppError;
use common::db::Transactional;

/// GET handler for /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated advisory severity counts for the specified SBOM.
/// Responds with a JSON `SeveritySummary` containing counts per severity level
/// (critical, high, medium, low) and a total.
pub async fn get_advisory_summary(
    Path(sbom_id): Path<Id>,
    service: /* injected AdvisoryService -- match the extraction pattern from get.rs */,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(sbom_id, &tx)
        .await
        .context("Failed to compute advisory severity summary")?;

    Ok(Json(summary))
}
```

## Conventions Applied

- **Path extraction**: `Path<Id>` matching the pattern in `modules/fundamental/src/advisory/endpoints/get.rs`
- **Service injection**: uses the same dependency injection pattern as `get.rs` (Axum State or Extension extractor)
- **Return type**: `Result<Json<SeveritySummary>, AppError>` -- struct returned directly via Json extractor as noted in Implementation Notes
- **Error handling**: `.context()` wrapping matching `common/src/error.rs` pattern
- **Documentation**: `///` doc comment on the handler function
- **Naming**: handler function named `get_advisory_summary` following `verb_noun` convention

## Inspection Required

Before creating, would:
1. `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/get.rs` to see exact handler signature, imports, and service injection pattern
2. `mcp__serena_backend__find_symbol` on the get handler with `include_body=true` to see full implementation
3. Verify the exact `Id` type used for path parameters
4. Check how `Transactional` is obtained in endpoint handlers

## Sibling Parity

Compared with `get.rs` and `list.rs` in the same directory:
- Same import structure
- Same parameter extraction pattern
- Same error handling approach
- Same return type wrapping
