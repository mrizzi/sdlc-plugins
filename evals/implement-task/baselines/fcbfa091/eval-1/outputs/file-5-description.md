# File 5: modules/fundamental/src/advisory/endpoints/severity_summary.rs (CREATE)

## Purpose

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary` that extracts the SBOM ID from the path, calls the advisory service's `severity_summary` method, and returns the result as JSON.

## File content

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use axum::extract::{Path, State};
use axum::Json;
use common::error::AppError;
use common::db::Transactional;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated severity counts for all advisories linked to the specified SBOM.
/// Responds with 404 if the SBOM ID does not exist.
pub async fn get_severity_summary(
    State(service): State<AdvisoryService>,
    Path(sbom_id): Path<String>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(sbom_id.into(), &Transactional::None)
        .await
        .context("fetching severity summary")?;

    Ok(Json(summary))
}
```

## Design decisions

- **Path parameter extraction**: uses `Path<String>` to extract the SBOM ID, then converts to `Id` via `.into()`, matching the pattern in `advisory/endpoints/get.rs`
- **State extraction**: uses Axum's `State` extractor for the advisory service, following the dependency injection pattern in sibling handlers
- **Transactional context**: passes `Transactional::None` for a read-only operation, consistent with `fetch` and `list` handlers
- **Error handling**: wraps the service call result with `.context()` to produce an `AppError`, matching the pattern in `common/src/error.rs`
- **Return type**: returns `Result<Json<SeveritySummary>, AppError>` -- the `Json` wrapper handles serialization, and `AppError` implements `IntoResponse` for error cases (including 404)
- **Documentation**: handler function has a `///` doc comment explaining the endpoint behavior

## Conventions applied

- File placed in `endpoints/` directory following module structure
- Handler function named `get_severity_summary` following `verb_noun` pattern
- Uses `Path<Id>` extraction matching `get.rs` handler
- Returns `Result<Json<T>, AppError>` matching sibling endpoint handlers
- Error wrapping with `.context()` for meaningful error messages
