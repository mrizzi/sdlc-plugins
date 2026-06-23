# File 4: modules/fundamental/src/advisory/endpoints/severity_summary.rs

**Action**: CREATE

**Purpose**: Define the GET handler for `/api/v2/sbom/{id}/advisory-summary` that extracts the path parameter, calls the service method, and returns the JSON response.

## Detailed Changes

This is a new endpoint handler file. It follows the pattern established by the sibling `get.rs` handler in the same directory.

### Contents

```rust
use axum::extract::Path;
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;
use common::db::Transactional;

/// Handler for `GET /api/v2/sbom/{id}/advisory-summary`.
///
/// Returns aggregated advisory severity counts for the specified SBOM,
/// including critical, high, medium, and low counts plus a total.
pub async fn severity_summary(
    service: /* injected AdvisoryService — extracted via Axum State or Extension, matching sibling pattern */,
    Path(id): Path<Id>,
    tx: /* Transactional extractor, matching sibling pattern */,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to retrieve advisory severity summary")?;

    Ok(Json(summary))
}
```

### Implementation approach

1. **Path parameter extraction**: Use `Path<Id>` to extract the SBOM ID from the URL path, matching the pattern in `get.rs`

2. **Service injection**: The `AdvisoryService` is injected via Axum's dependency injection mechanism (State or Extension extractor). The exact pattern would be confirmed by reading the sibling `get.rs` handler during Step 4.

3. **Transaction handling**: The `Transactional` parameter is extracted the same way as in sibling handlers.

4. **Response**: Return `Json(summary)` directly -- Axum's `Json` extractor handles serialization to the response body.

5. **Error propagation**: Errors from the service method bubble up as `AppError`, which implements `IntoResponse` and will produce appropriate HTTP error responses (e.g., 404 for not-found).

### Conventions Applied

- **Handler signature**: matches sibling `get.rs` pattern with `Path<Id>`, service injection, and `Transactional` parameter
- **Return type**: `Result<Json<SeveritySummary>, AppError>` per convention
- **Error handling**: `.context()` wrapping on the service call
- **Documentation**: doc comment on the handler function
- **File naming**: `severity_summary.rs` matches the naming pattern of `get.rs`, `list.rs` (action-oriented names)
