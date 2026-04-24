# File 2: Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

## Action: CREATE

## Purpose

Implement the `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler that calls
`AdvisoryService::severity_summary` and returns the `SeveritySummary` as JSON.

## Sibling Reference

- `modules/fundamental/src/advisory/endpoints/get.rs` -- GET handler for `/api/v2/advisory/{id}`
- `modules/fundamental/src/sbom/endpoints/get.rs` -- GET handler for `/api/v2/sbom/{id}`

These siblings show the pattern: extract `Path<Id>`, obtain the service from application
state, call the service method, handle errors with `AppError` and `.context()`, return
`Json<T>`.

## Detailed Changes

```rust
use axum::{
    extract::{Path, State},
    Json,
};
use trustify_common::error::AppError;
use trustify_common::db::Transactional;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated severity counts for all vulnerability advisories
/// linked to the specified SBOM.
pub async fn get_severity_summary(
    State(service): State<AdvisoryService>,
    Path(sbom_id): Path<Id>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(sbom_id, &tx)
        .await
        .context("Failed to retrieve advisory severity summary")?;

    Ok(Json(summary))
}
```

## Conventions Applied

- **Handler signature**: Matches sibling `get.rs` handlers -- `State` for service extraction,
  `Path` for ID, `Transactional` for DB transaction context.
- **Return type**: `Result<Json<SeveritySummary>, AppError>` -- consistent with all endpoint
  handlers in the project.
- **Error handling**: `.context()` wrapping for descriptive error messages, matching the
  pattern in `common/src/error.rs`.
- **Doc comment**: `///` doc comment on the handler function explaining what it does.
- **Single responsibility**: One handler per file, following the project convention
  (`list.rs`, `get.rs` each contain one handler).

## Notes

- The exact import paths and type names for `Id`, `State`, and `Transactional` would be
  confirmed by inspecting sibling endpoint files via Serena's `get_symbols_overview` or
  `find_symbol` in a real implementation.
- If the SBOM does not exist, the service method should return an `AppError` 404 variant,
  which propagates through the `?` operator automatically.
