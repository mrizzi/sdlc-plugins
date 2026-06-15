# File 2: modules/fundamental/src/advisory/endpoints/severity_summary.rs

## Action: CREATE

## Purpose

Define the Axum GET handler for `/api/v2/sbom/{id}/advisory-summary`. This handler extracts the SBOM ID from the path, calls the `AdvisoryService::severity_summary` method, and returns the result as JSON.

## Detailed Changes

Create a new file with the following contents:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use axum::extract::{Path, State};
use axum::Json;
use common::error::AppError;
use common::id::Id;

/// Handler for `GET /api/v2/sbom/{id}/advisory-summary`.
///
/// Returns aggregated severity counts for all vulnerability advisories
/// linked to the specified SBOM. Deduplicates advisories by advisory ID
/// before counting.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    State(service): State<AdvisoryService>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &())
        .await
        .context("fetching advisory severity summary")?;

    Ok(Json(summary))
}
```

## Conventions Applied

- **Handler signature**: Follows the exact pattern from `modules/fundamental/src/advisory/endpoints/get.rs` -- `async fn handler(Path(id): Path<Id>, State(service): State<ServiceType>) -> Result<Json<T>, AppError>`
- **Error handling**: Uses `.context()` wrapping with a descriptive message, matching the established pattern in all endpoint handlers
- **Path parameter extraction**: Uses Axum's `Path<Id>` extractor, consistent with `get.rs`
- **Return type**: Returns the struct directly wrapped in `Json`, letting Axum handle serialization (as noted in Implementation Notes)
- **Transactional**: Passes `&()` for the transaction parameter when no explicit transaction is needed (following the pattern if that is how sibling handlers invoke service methods; would verify via Serena before implementing)
- **Documentation**: Handler function has a doc comment describing the endpoint path and behavior
- **File naming**: Named `severity_summary.rs` matching the handler-per-file convention seen in `get.rs`, `list.rs`
