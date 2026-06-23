# File 5: modules/fundamental/src/advisory/endpoints/mod.rs

**Action**: MODIFY

**Purpose**: Register the new severity summary route in the advisory endpoints module.

## Detailed Changes

Add two things to this file:
1. A `mod severity_summary;` declaration to bring the new handler module into scope
2. A new `.route()` call in the router builder to register the endpoint path

### Before (representative existing content)

```rust
mod get;
mod list;

pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list))
        .route("/api/v2/advisory/:id", get(get::get))
}
```

### After

```rust
mod get;
mod list;
mod severity_summary;

pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list))
        .route("/api/v2/advisory/:id", get(get::get))
        .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::severity_summary))
}
```

### Implementation Notes

- The route path `/api/v2/sbom/{id}/advisory-summary` uses Axum's path parameter syntax (`:id` instead of `{id}`)
- The route is registered in the advisory module's router because the handler deals with advisory data, even though the URL is scoped under `/sbom/{id}/`. The exact placement would be confirmed by inspecting how routes are organized -- it may alternatively belong in the sbom endpoints module if routes are organized by URL prefix. The task description places it in the advisory endpoints, so that is followed.
- The `mod severity_summary;` declaration is added in alphabetical order among the existing module declarations

### Conventions Applied

- **Route registration**: follows `Router::new().route("/path", get(handler))` pattern per convention
- **Module declaration**: `mod severity_summary;` added to bring the handler module into scope
- **Alphabetical ordering**: module declarations kept in alphabetical order
