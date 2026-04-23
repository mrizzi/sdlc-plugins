# File 3 — Modify: `modules/fundamental/src/advisory/endpoints/mod.rs`

## Purpose

Register the new `severity_summary` handler module and add its route to the Axum router. This is the only wiring change needed to expose the endpoint — `server/src/main.rs` mounts all module routers automatically.

## Inspection Step

Read `modules/fundamental/src/advisory/endpoints/mod.rs` in full to understand:
- Which handler modules are declared (`pub mod get;`, `pub mod list;`)
- How the `Router` is constructed (likely a public function returning `Router<Arc<AdvisoryService>>` or similar)
- How existing routes are joined (`.merge()` or chained `.route()` calls)
- Whether the router function is named `router()`, `routes()`, or another convention

Also read `modules/fundamental/src/sbom/endpoints/mod.rs` as a sibling to confirm the pattern for SBOM-scoped sub-resource routes (since `/sbom/{id}/advisory-summary` is mounted under the sbom path hierarchy).

## Change 1 — Add module declaration

Add `pub mod severity_summary;` alongside the existing handler module declarations:

```rust
pub mod get;
pub mod list;
pub mod severity_summary;   // <-- ADD
```

## Change 2 — Register the route

In the router-building function, add the new route. The path mounts under the SBOM namespace because the endpoint is `/api/v2/sbom/{id}/advisory-summary`. Two possible patterns depending on how existing routes are structured:

**Pattern A** — if the advisory `endpoints/mod.rs` builds a router scoped to `/api/v2/advisory` and the SBOM-scoped route must be registered in the SBOM module's router instead:

In this case, the route `/api/v2/sbom/{id}/advisory-summary` belongs in `modules/fundamental/src/sbom/endpoints/mod.rs`, not the advisory endpoints. However, the task explicitly lists `modules/fundamental/src/advisory/endpoints/mod.rs` as the file to modify, so the intent is that this router also registers SBOM-cross-module routes, or that the advisory router is merged into a parent that handles this path.

**Resolution**: Follow the task description literally — add the route to `modules/fundamental/src/advisory/endpoints/mod.rs`. The path prefix context will be established at mount time in `server/main.rs`. The local route registration would be:

```rust
use axum::routing::get;
use axum::Router;
use std::sync::Arc;
use crate::advisory::service::advisory::AdvisoryService;

pub fn router() -> Router<Arc<AdvisoryService>> {
    Router::new()
        .route("/advisory", get(list::list))           // existing
        .route("/advisory/:id", get(get::get_advisory)) // existing
        .route("/sbom/:id/advisory-summary", get(severity_summary::severity_summary)) // ADD
}
```

The exact method and route path must be confirmed by reading the file. If `axum::routing::get` is already imported, no new import is needed. If the handler module needs an explicit use path, add:

```rust
use crate::advisory::endpoints::severity_summary;
```

(though in Rust this is usually implicit from the `pub mod` declaration in the same file).

## Convention compliance

- New `pub mod` declaration follows the same pattern as `pub mod get;` and `pub mod list;`
- Route registration follows `Router::new().route("/path", get(handler))` pattern documented in repo conventions
- No changes to `server/src/main.rs` required — task description confirms routes auto-mount
