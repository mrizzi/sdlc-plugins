# File 2: Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

## Purpose

New endpoint handler for `GET /api/v2/sbom/{id}/advisory-summary` that returns severity counts.

## Detailed Changes

### Handler function

Following the sibling pattern from `advisory/endpoints/get.rs`:

```rust
use axum::{extract::Path, Json};
use crate::advisory::service::AdvisoryService;
use crate::advisory::model::severity_summary::SeveritySummary;
use common::error::AppError;
use common::db::Transactional;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated severity counts for all unique advisories linked to the
/// specified SBOM. Returns 404 if the SBOM does not exist.
pub async fn get_advisory_summary(
    Path(sbom_id): Path<Id>,
    service: Extension<AdvisoryService>,
    tx: Extension<Transactional<'_>>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(sbom_id, &tx)
        .await
        .context("fetching advisory severity summary")?;

    Ok(Json(summary))
}
```

## Convention Compliance

- **Path extraction**: Uses `Path<Id>` extractor matching sibling `get.rs`
- **Return type**: `Result<Json<SeveritySummary>, AppError>` matching established pattern
- **Error handling**: `.context()` wrapping matching all sibling handlers
- **Naming**: `get_advisory_summary` follows `get_<entity>` pattern
- **Documentation**: Doc comment on the handler function explaining the endpoint behavior
- **Import organization**: Standard -> external -> internal grouping
