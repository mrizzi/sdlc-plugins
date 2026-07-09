# File 5: `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (CREATE)

## Pre-creation inspection

Before creating this file, inspect sibling endpoint handlers to match conventions:
- `mcp__serena_backend__find_symbol` on the handler function in `modules/fundamental/src/advisory/endpoints/get.rs` with `include_body=true` to see the exact handler signature, Path extraction, service invocation, and JSON response pattern.
- `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/endpoints/list.rs")` to see the list handler pattern for comparison.
- `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/sbom/endpoints/get.rs")` to see the SBOM get handler as a cross-module reference.

Also verify error handling:
- `mcp__serena_backend__find_symbol("AppError", include_body=true)` in `common/src/error.rs` to confirm the error enum and how `.context()` wrapping works.

## File content

```rust
use axum::{
    extract::{Path, State},
    Json,
};

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;
use common::model::Id;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns an aggregated severity summary of all advisories linked to the
/// specified SBOM, with counts per severity level and a total. Returns 404
/// if the SBOM ID does not exist.
pub async fn handler(
    Path(id): Path<Id>,
    State(service): State<AdvisoryService>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &Default::default())
        .await
        .context("fetching advisory severity summary")?;

    Ok(Json(summary))
}
```

## Design decisions

- **Handler signature**: Follows the exact pattern from `advisory/endpoints/get.rs` -- `Path<Id>` for path parameter extraction, `State<T>` for service injection, `Result<Json<T>, AppError>` return type.
- **Service call**: Calls `AdvisoryService::severity_summary()` with the extracted ID and a default `Transactional` reference, matching how existing handlers invoke service methods.
- **Error handling**: Uses `.context()` wrapping on the service call, propagating any `AppError` (including the 404 from the service layer when SBOM is not found).
- **JSON response**: Returns `Json<SeveritySummary>` directly -- Axum handles serialization automatically.
- **No manual serialization**: The response struct derives `Serialize`, so `Json(summary)` suffices.

## Conventions followed

- **Handler function name**: `handler` -- matches the pattern in `get.rs` where the handler is named `handler` (or the specific name used by siblings; adjusted during implementation).
- **Import organization**: Standard library (none needed), external crates (axum), internal modules (crate, common) -- each group separated by blank line.
- **Error propagation**: All errors propagated with `?` and wrapped with `.context()`.
- **Path parameter**: Uses Axum's `Path<Id>` extractor, matching the pattern referenced in Implementation Notes.
- **Documentation**: Doc comment on the handler function explaining the endpoint, its behavior, and its error case.

## State extraction note

The exact `State` type depends on how the Axum application state is structured. During implementation, inspect `get.rs` to confirm whether the state provides `AdvisoryService` directly or wraps it in an `AppState` struct. Adjust the extractor accordingly (e.g., `State(state): State<AppState>` followed by `state.advisory_service.severity_summary(...)`).
