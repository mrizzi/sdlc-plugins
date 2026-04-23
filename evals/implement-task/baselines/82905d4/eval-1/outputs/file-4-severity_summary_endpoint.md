# File 4: `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (CREATE)

## Purpose

Define the GET handler for `/api/v2/sbom/{id}/advisory-summary` that returns aggregated advisory severity counts for a given SBOM.

## Full Contents

```rust
use axum::extract::{Path, State};
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use trustify_common::db::Transactional;
use trustify_common::error::AppError;
use trustify_common::id::Id;

/// Retrieve advisory severity summary for a given SBOM.
///
/// Returns aggregated counts of advisory severities (critical, high, medium, low)
/// and a total count of unique advisories linked to the SBOM.
#[utoipa::path(
    get,
    path = "/api/v2/sbom/{id}/advisory-summary",
    responses(
        (status = 200, description = "Advisory severity summary", body = SeveritySummary),
        (status = 404, description = "SBOM not found"),
    ),
    params(
        ("id" = Id, Path, description = "SBOM identifier"),
    ),
    tag = "advisory",
)]
pub async fn get_severity_summary(
    State(service): State<AdvisoryService>,
    Path(id): Path<Id>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &Transactional::None)
        .await?;
    Ok(Json(summary))
}
```

## Design Decisions

1. **Follows `get.rs` pattern exactly**: The handler signature mirrors existing GET endpoints — `State<AdvisoryService>` for dependency injection, `Path<Id>` for path parameter extraction, `Result<Json<T>, AppError>` for the return type.

2. **`Transactional::None`**: Matches the pattern in existing handlers where read-only operations don't need an explicit transaction.

3. **Error propagation via `?`**: The `severity_summary` service method already wraps errors with `.context()`, so the handler can use `?` directly. If the service returns an `AppError::NotFound`, Axum will serialize it as a 404 response automatically.

4. **`utoipa::path` annotation**: Generates OpenAPI documentation for the endpoint, consistent with other endpoint files in the codebase. The `tag = "advisory"` groups it with other advisory endpoints in the API docs.

5. **No `.context()` in handler**: The service method already adds context. Adding another layer here would be redundant. However, if pre-implementation inspection reveals that sibling handlers DO add context at the handler level, this should be adjusted to match.

## Notes on Framework

The code above assumes Axum based on the task description mentioning "Axum's `Json` extractor." If pre-implementation inspection reveals the project uses Actix-web instead (or a mix), the handler signature would change to:

```rust
pub async fn get_severity_summary(
    service: web::Data<AdvisoryService>,
    path: web::Path<Id>,
) -> Result<HttpResponse, AppError> {
    let summary = service
        .severity_summary(path.into_inner(), &Transactional::None)
        .await?;
    Ok(HttpResponse::Ok().json(summary))
}
```

The correct framework will be confirmed during pre-implementation inspection of `get.rs`.
