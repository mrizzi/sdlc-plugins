# File 2: modules/fundamental/src/advisory/endpoints/severity_summary.rs

**Action:** CREATE

## Purpose

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary` that extracts the SBOM ID from the path, calls the `AdvisoryService::severity_summary` method, and returns the result as JSON.

## Pre-Implementation Inspection

Before creating this file, inspect the sibling endpoint handler to replicate its exact pattern:
- **`modules/fundamental/src/advisory/endpoints/get.rs`** -- understand the handler function signature (path parameter extraction via `Path<Id>`, service injection, transactional parameter), return type (`Result<Json<T>, AppError>`), `.context()` error wrapping, and import organization.
- **`modules/fundamental/src/advisory/endpoints/list.rs`** -- confirm the pattern is consistent across sibling handlers.

## Detailed Changes

### Handler Function

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
/// Returns aggregated severity counts for all unique advisories linked to the
/// specified SBOM. Returns 404 if the SBOM does not exist.
pub async fn get_severity_summary(
    Path(sbom_id): Path<Id>,
    service: AdvisoryService,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(sbom_id, &tx)
        .await
        .context("Failed to retrieve advisory severity summary")?;

    Ok(Json(summary))
}
```

### Design Decisions

- **Path extractor**: `Path<Id>` to extract the SBOM ID from the URL, matching the pattern in `get.rs` siblings.
- **Service injection**: `AdvisoryService` injected by Axum's dependency injection, matching existing handler patterns.
- **Transaction parameter**: `Transactional<'_>` passed through to the service method, consistent with all sibling handlers.
- **Error wrapping**: `.context()` wrapping on the service call, matching the error handling convention in `common/src/error.rs`.
- **Return type**: `Result<Json<SeveritySummary>, AppError>` following the standard handler return pattern.
- **No pagination**: this is a single-entity aggregation endpoint (not a list), so it returns the struct directly (no `PaginatedResults<T>` wrapper).

### Conventions Applied

- **File naming**: snake_case matching sibling `get.rs`, `list.rs`
- **Handler signature**: matches the `Path<Id>` + service + transactional pattern from sibling `get.rs`
- **Error handling**: `Result<T, AppError>` with `.context()` wrapping
- **Documentation**: doc comment on the handler function explaining what it does
- **Import organization**: standard library first, then external crates (`axum`), then internal modules (`crate::`, `common::`)
