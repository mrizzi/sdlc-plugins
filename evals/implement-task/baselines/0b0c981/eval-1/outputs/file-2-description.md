# File 2: `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (CREATE)

## Purpose
Axum GET handler for `GET /api/v2/sbom/{id}/advisory-summary` that extracts the SBOM ID, invokes the service method, and returns the JSON response.

## Detailed Changes

Create a new file with the following content:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use actix_web::web;
use axum::{
    extract::{Path, State},
    Json,
};
use trustify_common::db::Transactional;
use trustify_common::error::AppError;

/// GET /api/v2/sbom/{id}/advisory-summary
///
/// Returns aggregated severity counts for advisories linked to the specified SBOM.
#[utoipa::path(
    get,
    path = "/api/v2/sbom/{id}/advisory-summary",
    params(
        ("id" = String, Path, description = "SBOM identifier"),
    ),
    responses(
        (status = 200, description = "Severity summary", body = SeveritySummary),
        (status = 404, description = "SBOM not found"),
    ),
)]
pub async fn get(
    State(service): State<AdvisoryService>,
    Path(id): Path<String>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(&id, &tx)
        .await
        .context("fetching advisory severity summary")?;

    Ok(Json(summary))
}
```

## Rationale
- Follows the exact pattern from `endpoints/get.rs`: extract `Path<Id>`, call service, return `Json<T>`.
- Uses `State` extractor for the service, consistent with Axum state injection patterns.
- The `Transactional` parameter is passed through to the service layer, matching existing endpoint signatures.
- Error handling uses `.context()` wrapping as specified in the implementation notes.
- The utoipa macro generates OpenAPI documentation if the project uses it.
- The path parameter type is `String` — the service method will handle parsing/validation and return 404 for invalid or non-existent IDs.

## Note on Exact Patterns
The exact extractor types (`State` vs extension, `Path<String>` vs `Path<Id>` where `Id` is a custom type) should be confirmed by inspecting the actual `get.rs` sibling file. The implementation above follows the most common Axum patterns; the actual parameter types should match whatever `get.rs` uses. If `Id` is a custom type (e.g., a UUID wrapper), the `Path<Id>` type should be used instead of `Path<String>`.
