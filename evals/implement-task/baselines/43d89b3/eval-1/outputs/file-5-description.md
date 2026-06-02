# File 5: modules/fundamental/src/advisory/endpoints/severity_summary.rs (CREATE)

## Purpose
Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary` that returns aggregated severity counts.

## Contents

```rust
use axum::extract::Path;
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::advisory::AdvisoryService;
use common::error::AppError;
// Additional imports for Id type, service state extraction, and Transactional as needed

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a JSON response with advisory severity counts (critical, high, medium, low, total)
/// for the specified SBOM. Returns 404 if the SBOM does not exist.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: /* extracted from shared state, matching sibling handler pattern */,
    tx: /* transactional context, matching sibling handler pattern */,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to fetch advisory severity summary for SBOM")?;

    Ok(Json(summary))
}
```

## Design Decisions
- Handler signature follows the pattern from `modules/fundamental/src/advisory/endpoints/get.rs`:
  - `Path<Id>` for path parameter extraction.
  - Service accessed via shared state/extension (exact mechanism matches sibling handlers).
  - Returns `Result<Json<T>, AppError>`.
- Error wrapping uses `.context()` matching the sibling endpoint pattern.
- The handler is minimal -- it delegates all logic to the service layer, consistent with the existing separation of concerns in the codebase.

## Conventions Applied
- Handler naming: `get_severity_summary` follows `get_advisory` pattern from `get.rs`.
- Error handling: `.context()` wrapping with descriptive message.
- Return type: `Result<Json<SeveritySummary>, AppError>` -- struct returned directly, Axum handles serialization.
- Import organization: axum imports first, then crate-internal imports.
- Documentation: `///` doc comment on the handler function describing the endpoint, response, and error behavior.
