# File 2: modules/fundamental/src/advisory/endpoints/severity_summary.rs (CREATE)

## Purpose

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary` that calls `AdvisoryService::severity_summary` and returns the `SeveritySummary` as JSON.

## Detailed Changes

### Inspect before writing

Before creating this file, inspect sibling endpoint handlers to confirm patterns:
- Use `mcp__serena_backend__find_symbol` with `include_body=true` on the handler function in `modules/fundamental/src/advisory/endpoints/get.rs` to see exact parameter extraction, service invocation, and response patterns
- Use `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/list.rs` to see alternative endpoint pattern
- Inspect `common/src/error.rs` via `mcp__serena_backend__find_symbol` on `AppError` to understand error variants available

### New file content

```rust
use axum::extract::Path;
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;
use sea_orm::TransactionTrait;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated severity counts for all advisories linked to the
/// specified SBOM. Deduplicates advisories by ID before counting.
pub async fn get_severity_summary(
    Path(sbom_id): Path<Id>,
    service: Extension<AdvisoryService>,
    db: Extension<Database>,
) -> Result<Json<SeveritySummary>, AppError> {
    let tx = db.begin().await.context("starting transaction")?;
    let summary = service
        .severity_summary(sbom_id, &tx)
        .await
        .context("fetching severity summary")?;
    Ok(Json(summary))
}
```

### Notes

- The exact parameter types (`Id`, `Extension`, `Database`, `Transactional`) will be confirmed by inspecting the sibling `get.rs` handler — adjust imports accordingly
- Error handling uses `.context()` wrapping into `AppError` per discovered convention
- The handler returns `Result<Json<SeveritySummary>, AppError>` matching the sibling pattern
- If the sibling uses `State` instead of `Extension` for dependency injection, adjust accordingly
- If the sibling uses a different transaction pattern (e.g., passing `&Transactional<'_>` directly), match that pattern
- Doc comment on the handler function per code quality requirements
