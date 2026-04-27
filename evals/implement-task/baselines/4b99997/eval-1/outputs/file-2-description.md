# File 2: Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

## Action: CREATE

## Purpose

Define the GET handler for `/api/v2/sbom/{id}/advisory-summary` that extracts the SBOM ID from the path, calls the service method, and returns the severity summary as JSON.

## Detailed Changes

### Imports

```rust
use axum::{
    extract::Path,
    Json,
};
use crate::advisory::service::AdvisoryService;
use crate::advisory::model::severity_summary::SeveritySummary;
use common::error::AppError;
use common::db::Transactional;
```

Imports follow the sibling pattern in `endpoints/get.rs`: Axum extractors, the service, the model, and the error type.

### Handler Function

```rust
/// Retrieves aggregated advisory severity counts for a specific SBOM.
///
/// Returns a breakdown of advisory severities (critical, high, medium, low)
/// and a total count. Returns 404 if the SBOM does not exist.
pub async fn severity_summary(
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

### Pattern Adherence

This handler follows the exact pattern from the existing `get.rs` endpoint:
1. Extract path parameter via `Path<Id>`
2. Receive the service and transaction as Axum extractors/state
3. Call the service method with `(id, &tx)`
4. Wrap errors with `.context()` for descriptive error messages
5. Return `Json<T>` on success

### Error Handling

- If the SBOM ID does not exist, the service method returns an error that maps to HTTP 404, consistent with existing SBOM endpoints
- All other errors are wrapped with `.context()` and map to appropriate HTTP status codes via `AppError`'s `IntoResponse` implementation

## Conventions Applied

- **Handler signature**: Matches sibling `get.rs` pattern -- `async fn` with Axum extractors returning `Result<Json<T>, AppError>`
- **Error wrapping**: Uses `.context()` per project convention
- **Documentation**: Doc comment on the handler function explaining what it does and its error behavior
- **Naming**: snake_case function name matching the module name
