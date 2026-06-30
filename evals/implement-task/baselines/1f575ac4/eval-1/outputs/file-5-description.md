# File 5: `modules/fundamental/src/advisory/endpoints/mod.rs` (MODIFY)

## Purpose

Register the new severity summary route in the advisory module's endpoint router.

## Detailed Changes

### Add module declaration

At the top of the file, alongside existing module declarations (`mod list;`, `mod get;`), add:

```rust
mod severity_summary;
```

### Add route registration

In the `router()` function, add the new route to the `Router` chain:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::severity_summary))
```

### Full context of the change

The modified `router()` function would look like:

```rust
pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
        .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::severity_summary))
}
```

### Design decisions

- **Follows existing registration pattern**: Uses the same `Router::new().route(path, get(handler))` pattern visible in the existing route registrations.
- **Route path matches API spec**: The route `/api/v2/sbom/:id/advisory-summary` matches the API change specified in the task description (`GET /api/v2/sbom/{id}/advisory-summary`).
- **Module placed in advisory endpoints**: Although the route is under `/sbom/`, the business logic is advisory-focused, so it lives in the advisory module. This follows the pattern where the domain owning the logic owns the endpoint.
