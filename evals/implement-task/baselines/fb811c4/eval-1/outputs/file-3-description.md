# File 3: modules/fundamental/src/advisory/endpoints/severity_summary.rs (CREATE)

## Purpose
Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary` that returns severity counts.

## Detailed Changes

Create a new file with the following content:

```rust
use axum::extract::Path;
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;
use common::db::Transactional;

/// Handles GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a severity breakdown (critical, high, medium, low, total) for all
/// unique advisories linked to the specified SBOM. Returns 404 if the SBOM
/// does not exist.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: AdvisoryService,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to retrieve advisory severity summary")?;

    Ok(Json(summary))
}
```

## Conventions Applied
- **Pattern match**: follows the existing endpoint pattern in `modules/fundamental/src/advisory/endpoints/get.rs`
  - Extract path params via `Path<Id>`
  - Call service method
  - Return JSON response directly
- **Error handling**: uses `Result<Json<T>, AppError>` with `.context()` wrapping
- **Response type**: returns the struct directly wrapped in `Json()` (Axum handles serialization)
- **Documentation**: doc comment on the handler function explaining what it does
- **Naming**: function named `get_severity_summary` following the `verb_noun` convention
- **File naming**: named `severity_summary.rs` following the sibling pattern (`get.rs`, `list.rs`)
