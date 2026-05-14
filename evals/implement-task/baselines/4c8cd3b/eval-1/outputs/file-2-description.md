# File 2: modules/fundamental/src/advisory/endpoints/severity_summary.rs

**Action:** CREATE

## Purpose

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary` that retrieves severity counts for a given SBOM's linked advisories.

## Detailed Changes

Create a new file with the following contents:

```rust
use axum::extract::Path;
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::db::Transactional;
use common::error::AppError;
use common::model::Id;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated severity counts for all vulnerability advisories
/// linked to the specified SBOM. Returns 404 if the SBOM does not exist.
pub async fn get_severity_summary(
    service: AdvisoryService,
    Path(id): Path<Id>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(&id, &tx)
        .await
        .context("Failed to retrieve advisory severity summary")?;

    Ok(Json(summary))
}
```

## Conventions Applied

- **Handler signature:** Follows the exact pattern from sibling `get.rs` -- extracts `Path<Id>`, receives service and transaction as Axum extractors, returns `Result<Json<T>, AppError>`.
- **Error handling:** Uses `.context()` wrapping consistent with all handlers in the `endpoints/` directory.
- **File naming:** `severity_summary.rs` matching the feature name, consistent with sibling files `get.rs` and `list.rs`.
- **Documentation:** Handler function has a doc comment explaining the endpoint and its error behavior.
- **Import organization:** Framework imports first, then crate-internal imports, following the established convention.
