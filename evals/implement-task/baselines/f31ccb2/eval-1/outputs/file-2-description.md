# File 2: `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (CREATE)

## Purpose

Define the GET handler for `/api/v2/sbom/{id}/advisory-summary` that returns aggregated severity counts for advisories linked to a given SBOM.

## Detailed Changes

Create a new file with the following content:

### Imports

```rust
use axum::{
    extract::Path,
    Json,
};
use crate::advisory::{
    model::severity_summary::SeveritySummary,
    service::AdvisoryService,
};
use common::error::AppError;
```

The exact import path for the service extractor (Extension vs. State) should be confirmed by inspecting `advisory/endpoints/get.rs`, but the pattern is consistent: the service is injected as an Axum extractor.

### Handler Function

```rust
/// Get advisory severity summary for an SBOM
#[utoipa::path(
    get,
    path = "/api/v2/sbom/{id}/advisory-summary",
    params(
        ("id" = Id, Path, description = "SBOM identifier"),
    ),
    responses(
        (status = 200, description = "Advisory severity summary", body = SeveritySummary),
        (status = 404, description = "SBOM not found"),
    ),
)]
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: Extension<AdvisoryService>,  // or State<AdvisoryService> — match sibling pattern
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to fetch advisory severity summary")?;

    Ok(Json(summary))
}
```

### Design Decisions

1. **Path extraction**: Uses `Path<Id>` to extract the SBOM identifier from the URL, matching `advisory/endpoints/get.rs`.

2. **Service injection**: Injected via Axum extractor (Extension or State), matching the existing endpoint pattern.

3. **Transactional parameter**: Included as `tx: Transactional<'_>` to pass through to the service method, ensuring the query runs within a transaction context.

4. **Error handling**: Uses `.context()` wrapping to add a descriptive message, then `?` propagation converts to `AppError` which maps to appropriate HTTP status codes (404 for not found, 500 for internal errors).

5. **Return type**: `Result<Json<SeveritySummary>, AppError>` — Axum automatically serializes the `SeveritySummary` to JSON and sets the content-type header.

6. **OpenAPI annotation**: `#[utoipa::path(...)]` attribute provides API documentation, following the pattern used by other endpoints.

7. **404 handling**: The service method returns an `AppError` with a not-found variant when the SBOM ID does not exist. This is propagated through `?` and automatically rendered as a 404 response by `AppError`'s `IntoResponse` implementation.

## Conventions Applied

- Handler function signature matches `advisory/endpoints/get.rs` pattern
- Error handling via `.context()` wrapping matches `common/src/error.rs` patterns
- `utoipa::path` annotation for OpenAPI spec generation
- Function named descriptively (`get_severity_summary`)
- Module will be registered and route added in `endpoints/mod.rs` (see file-6-description.md)
