# File 2: modules/fundamental/src/advisory/endpoints/severity_summary.rs

## Action: CREATE

## Purpose
Define the GET handler for `/api/v2/sbom/{id}/advisory-summary` that returns
aggregated severity counts for a given SBOM.

## Sibling Reference
Follows the pattern of `modules/fundamental/src/advisory/endpoints/get.rs`
(GET /api/v2/advisory/{id}) -- extracts path params via `Path<Id>`, calls service,
returns JSON.

## Detailed Changes

```rust
use axum::extract::{Path, State};
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::db::Transactional;
use common::error::AppError;
use common::model::Id;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated advisory severity counts for the specified SBOM,
/// enabling dashboard widgets to render severity breakdowns.
pub async fn handler(
    State(service): State<AdvisoryService>,
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

## Notes
- Uses `Path<Id>` to extract the SBOM ID from the URL, matching the pattern in `get.rs`.
- Calls `AdvisoryService::severity_summary()` which handles SBOM existence validation and returns 404 if not found.
- Returns `Result<Json<SeveritySummary>, AppError>` -- Axum's `Json` handles serialization, `AppError` handles error responses.
- Error wrapping uses `.context()` per the convention in `common/src/error.rs`.
- The handler function has a doc comment explaining its purpose.
- The exact State extractor pattern and Transactional parameter should match what sibling endpoint handlers use (inspect `get.rs` to confirm exact signature).
