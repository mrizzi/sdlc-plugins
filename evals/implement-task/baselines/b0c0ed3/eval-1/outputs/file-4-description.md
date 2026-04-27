# File 4: `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (CREATE)

## Purpose

Define the HTTP handler for `GET /api/v2/sbom/{id}/advisory-summary`. Extracts the SBOM ID from the path, calls `AdvisoryService::severity_summary`, and returns the result as JSON.

## Detailed Changes

Create a new file with the following content:

```rust
use axum::{
    extract::{Path, State},
    Json,
};

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;
use common::db::Transactional;

/// GET /api/v2/sbom/{id}/advisory-summary
///
/// Returns aggregated severity counts for advisories linked to the given SBOM.
pub async fn get_advisory_summary(
    State(service): State<AdvisoryService>,
    Path(id): Path<Id>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id.clone(), &tx)
        .await
        .context("failed to get advisory severity summary")?;

    Ok(Json(summary))
}
```

## Design Decisions

- **Path extraction**: Uses `Path(id): Path<Id>` matching the pattern in `advisory/endpoints/get.rs` and `sbom/endpoints/get.rs`.
- **State extraction**: Extracts `AdvisoryService` from Axum application state, following the existing handler pattern.
- **Return type**: `Result<Json<SeveritySummary>, AppError>` -- returns JSON directly; `AppError` handles error-to-HTTP-status conversion.
- **404 handling**: If the service's `severity_summary` method internally calls `fetch` on the SBOM and it doesn't exist, the error propagates as a 404 via `AppError`. The service method should be designed to return a not-found error when the SBOM ID doesn't exist, consistent with existing SBOM endpoints.
- **Error wrapping**: Uses `.context()` consistent with all sibling endpoint handlers.

## Convention Conformance

- One handler function per file, matching `get.rs` and `list.rs` siblings.
- File name `severity_summary.rs` follows snake_case convention.
- Handler is async, uses Axum extractors, returns `Result<Json<T>, AppError>`.
- No pagination wrapper since this is a single aggregate response (not a collection).
