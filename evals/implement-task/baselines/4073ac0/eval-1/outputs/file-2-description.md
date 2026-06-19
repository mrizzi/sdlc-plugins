# File 2: modules/fundamental/src/advisory/endpoints/mod.rs

**Action**: Modify (add route registration)

## Current State

This file registers routes for the advisory module. It follows the pattern:
```rust
use axum::{routing::get, Router};

mod get;
mod list;

pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
}
```

(Actual route paths and handler names would be confirmed by inspecting the file with Serena before modifying.)

## Changes

### 1. Add module declaration

Add `mod severity_summary;` alongside the existing module declarations:

```rust
mod get;
mod list;
mod severity_summary;  // NEW
```

### 2. Add route registration

Add the new route to the `Router` chain. The endpoint path is `/api/v2/sbom/{id}/advisory-summary` as specified in the API Changes section. Note: this routes through the advisory module's router even though the path includes `/sbom/` -- this is because the endpoint aggregates advisory data for a given SBOM.

```rust
pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
        .route(
            "/api/v2/sbom/:id/advisory-summary",
            get(severity_summary::get_advisory_summary),
        )  // NEW
}
```

## Rationale

- Follows the existing pattern of `Router::new().route(...)` chaining
- Module declaration added alongside siblings (`get`, `list`)
- Route path matches the API Changes specification: `GET /api/v2/sbom/{id}/advisory-summary`
- Handler reference follows the `module::function` pattern used by existing routes
- The task notes that `server/src/main.rs` requires no changes because routes auto-mount via module registration
