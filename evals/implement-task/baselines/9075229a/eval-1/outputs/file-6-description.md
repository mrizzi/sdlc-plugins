# File 6: modules/fundamental/src/advisory/endpoints/mod.rs

## Action: MODIFY

## Purpose
Register the new severity summary route in the advisory endpoint module so it is accessible via the REST API.

## Detailed Changes

Add a module declaration for the new endpoint file and register the route in the router:

```rust
// Existing module declarations (unchanged):
mod get;
mod list;

// Add this module declaration:
mod severity_summary;

// In the router construction function, add the new route:
// Existing routes (unchanged):
Router::new()
    .route("/api/v2/advisory", get(list::get))
    .route("/api/v2/advisory/:id", get(get::get))
    // Add this route:
    .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get))
```

## Conventions Applied
- **Module declaration**: `mod severity_summary;` follows the pattern of existing `mod get;` and `mod list;` declarations.
- **Route registration**: `.route("/path", get(handler))` chained onto the existing `Router::new()` builder, matching the exact pattern used for other routes.
- **Path parameter syntax**: Uses `:id` (Axum path parameter syntax) consistent with existing routes like `/api/v2/advisory/:id`.
- **Handler reference**: `severity_summary::get` follows the `module::function` convention used for `get::get` and `list::get`.

## Note on Route Placement
The new endpoint path `/api/v2/sbom/{id}/advisory-summary` is scoped under the SBOM path namespace but registered in the advisory endpoints module. This is acceptable because the endpoint is fundamentally an advisory aggregation operation; however, during actual implementation, verify that the route mounts correctly given how `server/main.rs` assembles module routers. If SBOM-prefixed routes must be registered in the SBOM module's `endpoints/mod.rs` instead, move the registration there.
