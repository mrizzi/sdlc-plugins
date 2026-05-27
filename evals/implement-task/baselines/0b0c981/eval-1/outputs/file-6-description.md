# File 6: `modules/fundamental/src/advisory/endpoints/mod.rs` (MODIFY)

## Purpose
Register the new severity summary endpoint route in the advisory endpoints module.

## Detailed Changes

### 1. Add module declaration

Add at the top of the file alongside existing module declarations:

```rust
pub mod severity_summary;
```

### 2. Add route registration

Add the new route to the `Router` construction, following the pattern of existing route registrations:

### Before (expected current state)
```rust
pub fn router() -> Router<AppState> {
    Router::new()
        .route("/api/v2/advisory", get(list::list))
        .route("/api/v2/advisory/:id", get(get::get))
        // ... other existing routes
}
```

### After
```rust
pub fn router() -> Router<AppState> {
    Router::new()
        .route("/api/v2/advisory", get(list::list))
        .route("/api/v2/advisory/:id", get(get::get))
        .route(
            "/api/v2/sbom/:id/advisory-summary",
            get(severity_summary::get),
        )
        // ... other existing routes
}
```

## Rationale
- Follows the existing pattern of `Router::new().route("/path", get(handler))` registrations.
- The route path `/api/v2/sbom/:id/advisory-summary` matches the API specification from the task.
- Uses Axum's `:id` path parameter syntax (or `{id}` depending on the Axum version — should match whichever syntax existing routes use).
- The handler function is referenced as `severity_summary::get`, matching the function name in the new endpoint module.

## Note on Route Location
The route is for an SBOM sub-resource (`/api/v2/sbom/{id}/advisory-summary`) but is registered in the advisory endpoints module. This follows the task specification. An alternative would be to register it in the sbom endpoints module — the actual placement should follow whatever the task explicitly requests, which is the advisory endpoints module.

If the project's router composition means the advisory module's routes are mounted under a prefix, the route path may need adjustment. Inspect the server's route composition in `server/src/main.rs` to confirm.
