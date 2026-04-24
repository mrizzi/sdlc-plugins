# File 5: modules/fundamental/src/advisory/endpoints/mod.rs

**Action**: MODIFY

## Purpose

Register the new `GET /api/v2/sbom/{id}/advisory-summary` route in the advisory endpoints module so it is mounted by the server.

## Conventions Applied

- **Route registration pattern**: Uses `Router::new().route("/path", get(handler))` as specified in Implementation Notes and consistent with existing routes for `list.rs` and `get.rs`
- **Module declaration**: Adds `mod severity_summary;` to declare the new endpoint module
- **Import style**: Imports the handler function from the new module

## Current State (expected)

```rust
mod list;
mod get;

use axum::{routing::get, Router};

pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
}
```

## Change Description

Add the module declaration and route registration for the severity summary endpoint:

```rust
mod list;
mod get;
mod severity_summary;

use axum::{routing::get, Router};

pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
        .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
}
```

## Design Decisions

1. **Route path `/api/v2/sbom/:id/advisory-summary`**: Matches the API contract specified in the task description. The path is nested under `/sbom/{id}` because the endpoint is scoped to a specific SBOM, even though the implementation lives in the advisory module.
2. **Axum path syntax**: Uses `:id` (Axum's path parameter syntax) rather than `{id}` (OpenAPI syntax). The exact syntax would be verified from sibling routes during actual implementation.
3. **Module placed in advisory endpoints**: The task specifies this file should live in the advisory endpoints directory, which makes sense because the aggregation logic is advisory-centric even though the path references SBOMs.

## Notes

- The exact structure of the `router()` function (or equivalent) and whether routes are composed via `.merge()`, `.nest()`, or direct `.route()` calls would be verified from the actual `mod.rs` file during implementation.
- If the SBOM module has its own route namespace and the advisory module's `mod.rs` cannot register `/api/v2/sbom/...` paths, the route might need to be registered in the SBOM endpoints module instead. This would be flagged as an out-of-scope deviation and discussed with the user.
