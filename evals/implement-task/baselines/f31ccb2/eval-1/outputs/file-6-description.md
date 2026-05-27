# File 6: `modules/fundamental/src/advisory/endpoints/mod.rs` (MODIFY)

## Purpose

Register the new `severity_summary` endpoint module and add its route to the advisory router.

## Detailed Changes

### Current State (inferred from repository structure)

The file currently declares endpoint submodules and builds a router:

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

(Exact handler function names and route paths are inferred from the endpoint pattern; actual names should be confirmed via code intelligence.)

### Changes

1. **Add module declaration** for the new endpoint file:

```rust
mod severity_summary;
```

2. **Add route registration** for the new endpoint in the `router()` function:

```rust
.route(
    "/api/v2/sbom/:id/advisory-summary",
    get(severity_summary::get_severity_summary),
)
```

### Result After Modification

```rust
mod list;
mod get;
mod severity_summary;

use axum::{routing::get, Router};

pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
        .route(
            "/api/v2/sbom/:id/advisory-summary",
            get(severity_summary::get_severity_summary),
        )
}
```

### Design Decisions

1. **Route path**: `/api/v2/sbom/:id/advisory-summary` — the endpoint is nested under the SBOM resource because it returns advisory data scoped to a specific SBOM. This follows REST conventions where the parent resource is in the path. The `:id` syntax is Axum's path parameter notation.

2. **Route registration in advisory module**: Although the path is under `/sbom/`, the route is registered in the advisory endpoints module because it is an advisory aggregation service. This is a judgment call — if the codebase prefers routes to be registered by path prefix, it might belong in `sbom/endpoints/mod.rs` instead. The task description specifies modifying `advisory/endpoints/mod.rs`, so we follow that guidance.

3. **HTTP method**: `get` — this is a read-only aggregation query, appropriate for GET.

4. **No changes to `server/src/main.rs`**: The server mounts all module routers automatically, so adding the route to the advisory module's router is sufficient.

## Conventions Applied

- Module declaration follows existing `mod list;` / `mod get;` pattern
- Route added via `.route()` chain on the existing `Router::new()` builder
- Uses `axum::routing::get` for GET endpoints
- Handler referenced as `module::function_name`
