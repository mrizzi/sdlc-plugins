# File 5: modules/fundamental/src/advisory/endpoints/severity_summary.rs (CREATE)

## Purpose

Define the GET handler for `/api/v2/sbom/{id}/advisory-summary` that extracts the SBOM ID from the path, calls the service method, and returns the severity summary as JSON.

## Pre-change Inspection

Before creating, inspect the sibling endpoint handler to understand the exact pattern:
```
mcp__serena_backend__find_symbol("get_advisory", include_body=true)
```
in `modules/fundamental/src/advisory/endpoints/get.rs`

Also inspect:
```
mcp__serena_backend__find_symbol("list_advisories", include_body=true)
```
in `modules/fundamental/src/advisory/endpoints/list.rs`

Understand: imports, function signature, path parameter extraction, service invocation, error handling, and response return.

## File Contents

```rust
use axum::extract::Path;
use axum::Json;

use crate::advisory::service::AdvisoryService;
use common::error::AppError;
use common::id::Id;

/// GET handler for `/api/v2/sbom/{id}/advisory-summary`.
///
/// Returns aggregated vulnerability advisory severity counts for the specified
/// SBOM. The response includes counts per severity level (Critical, High,
/// Medium, Low) and a total count of unique advisories.
///
/// Returns 404 if the SBOM ID does not exist.
pub async fn get_severity_summary(
    service: /* extracted service state -- exact type matches sibling handlers */,
    Path(sbom_id): Path<Id>,
    tx: /* transaction extractor -- matches sibling handlers */,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(sbom_id, &tx)
        .await
        .context("Failed to retrieve advisory severity summary")?;

    Ok(Json(summary))
}
```

## Design Decisions

1. **Function signature**: Follows the exact pattern from `get.rs` -- path parameter via `Path<Id>`, service from application state, transaction from extractor. The exact state and transaction types would be confirmed by reading the sibling handler.

2. **Error handling**: Uses `Result<Json<SeveritySummary>, AppError>` matching sibling handlers. The `.context()` wrapping provides a descriptive error message.

3. **Response type**: Returns `Json<SeveritySummary>` directly. Axum serializes this to JSON automatically. This is not a paginated endpoint (it returns a single summary object), so `PaginatedResults<T>` is not used.

4. **Doc comment**: Comprehensive `///` doc comment on the handler function explaining the endpoint path, what it returns, and the 404 behavior.

## Notes

- The exact parameter types for service state and transaction depend on how the project injects dependencies. Common patterns include:
  - `Extension<Arc<AdvisoryService>>` (Axum Extension)
  - `State<AppState>` (Axum State)
  - Custom extractors
- These would be confirmed by reading the sibling `get.rs` handler body.
- The import paths would be adjusted based on the actual project structure.
