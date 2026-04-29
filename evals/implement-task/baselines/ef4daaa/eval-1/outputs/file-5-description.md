# File 5: modules/fundamental/src/advisory/endpoints/mod.rs

**Action**: MODIFY

## Purpose

Register the new `GET /api/v2/sbom/{id}/advisory-summary` route in the advisory module's endpoint router, and declare the `severity_summary` endpoint module.

## Files inspected before writing

Before modifying this file, the following would be inspected:

- `modules/fundamental/src/advisory/endpoints/mod.rs` -- PRIMARY: `mcp__serena_backend__get_symbols_overview` to see the full module structure, existing `mod` declarations, and the router construction function. Then `mcp__serena_backend__find_symbol` on the router function to see the exact `Router::new().route(...)` chain pattern.
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- SIBLING: to see how SBOM-scoped routes are registered, especially routes that include `{id}` path parameters
- `mcp__serena_backend__find_referencing_symbols` on the router function to understand how the module router is mounted in `server/main.rs`

## Conventions applied

- Module declaration: `pub mod severity_summary;` following existing `pub mod get;` and `pub mod list;` declarations
- Route registration: `.route("/sbom/:id/advisory-summary", get(severity_summary::severity_summary))` chained onto the existing `Router::new()` builder
- Import pattern: uses module-level import or inline path reference for the handler function

## Detailed changes

### 1. Add module declaration

Add the new module declaration alongside existing ones. Would use `mcp__serena_backend__insert_after_symbol` after the last existing `mod` declaration (e.g., after `pub mod get;`):

```rust
pub mod severity_summary;
```

### 2. Register the route

Add the new route to the router builder chain. Would use `mcp__serena_backend__find_symbol` to locate the router construction function, then use Edit to append the new route:

```rust
// Existing code (approximate):
pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list))
        .route("/api/v2/advisory/:id", get(get::get))
        // Add the new route:
        .route(
            "/api/v2/sbom/:id/advisory-summary",
            get(severity_summary::severity_summary),
        )
}
```

**Note on path prefix**: The exact route path format (`:id` vs `{id}` vs `<id>`) would be determined by inspecting the existing routes in `mod.rs`. Axum uses `:id` for path parameters. The path uses the SBOM scope (`/api/v2/sbom/:id/...`) rather than the advisory scope because the endpoint aggregates advisories *for* a specific SBOM.

## Key design decisions

1. **Route placement**: The SBOM-scoped advisory summary route is registered in the advisory module's router, not the SBOM module's router, because the logic and service belong to the advisory domain. This follows the pattern where the route's implementation module owns its registration, even if the URL path is scoped under a different entity.
2. **No middleware changes**: No additional middleware (caching, rate limiting) is added unless observed in sibling route registrations. The `tower-http` caching middleware mentioned in the repo conventions would be applied only if existing routes demonstrate it.
3. **Handler reference**: The handler is referenced as `severity_summary::severity_summary` (module::function). This matches the existing pattern of `get::get` and `list::list`.

## Integration points

- References the handler in `severity_summary.rs` (file 2)
- The router is mounted by `server/main.rs` (no changes needed -- auto-mount via module registration)
- Alongside existing route registrations for `/api/v2/advisory` and `/api/v2/advisory/:id`
