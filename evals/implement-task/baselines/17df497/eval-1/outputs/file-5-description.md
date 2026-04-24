# File 5: modules/fundamental/src/advisory/endpoints/mod.rs

**Action:** MODIFY

## Purpose

Register the new `GET /api/v2/sbom/{id}/advisory-summary` route in the advisory module's endpoint registration file.

## Detailed Changes

### Add Module Declaration

At the top of the file, alongside existing module declarations (e.g., `mod get;`, `mod list;`), add:

```rust
mod severity_summary;
```

### Add Route Registration

In the route builder function (where existing routes like `get.rs` and `list.rs` handlers are registered), add the new route:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

This follows the existing pattern of `Router::new().route("/path", get(handler))` registrations seen in sibling `endpoints/mod.rs` files.

### Before (Conceptual)

```rust
mod get;
mod list;

pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
}
```

### After (Conceptual)

```rust
mod get;
mod list;
mod severity_summary;

pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
        .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
}
```

### Design Notes

- The route path uses `/api/v2/sbom/{id}/advisory-summary` as specified in the task's API Changes section. Even though this is registered in the advisory module's endpoints, the URL path is SBOM-scoped because the feature aggregates advisories for a given SBOM.
- The route uses Axum's `:id` path parameter syntax (equivalent to `{id}` in OpenAPI notation).

### Conventions Applied

- **Module registration**: `mod severity_summary;` declaration at the top of the file
- **Route pattern**: `Router::new().route("/path", get(handler))` matching existing registrations
- **Handler reference**: `severity_summary::get_severity_summary` using the module::function pattern
