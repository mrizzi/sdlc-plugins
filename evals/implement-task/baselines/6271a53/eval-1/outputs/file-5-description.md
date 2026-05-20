# File 5: `modules/fundamental/src/advisory/endpoints/mod.rs` (MODIFY)

## Purpose

Register the new severity summary route and import the new endpoint handler module.

## Conventions Applied

- Follows the route registration pattern: `Router::new().route("/path", get(handler))`
- Imports the new endpoint module with `pub mod severity_summary;`
- Adds the route following the pattern of existing route registrations in this file

## Change Description

Two additions to the existing `endpoints/mod.rs`:

### 1. Add module declaration

Add to the module declarations section at the top of the file:

```rust
pub mod severity_summary;
```

### 2. Add route registration

Add to the router builder chain where existing routes are registered:

```rust
.route(
    "/api/v2/sbom/:id/advisory-summary",
    get(severity_summary::severity_summary),
)
```

## Diff (illustrative)

```diff
 pub mod get;
 pub mod list;
+pub mod severity_summary;

 // ... inside the router function ...

 Router::new()
     .route("/api/v2/advisory", get(list::list))
     .route("/api/v2/advisory/:id", get(get::get))
+    .route(
+        "/api/v2/sbom/:id/advisory-summary",
+        get(severity_summary::severity_summary),
+    )
```

## Design Decisions

1. **Route path uses `:id` syntax**: Axum uses `:param` for path parameters (not `{param}` which is OpenAPI/Swagger syntax). The task description uses `{id}` in the API specification, but the actual Axum route registration uses `:id`.

2. **Route placed in advisory endpoints**: Although the URL path starts with `/sbom/`, the route is registered in the advisory module's endpoints because the feature is about advisory severity aggregation. This follows the principle that the module responsible for the business logic owns the route.

3. **Handler name matches module name**: The handler function `severity_summary::severity_summary` follows the convention where the module name and the primary handler function share the same name (similar to `get::get` and `list::list`).
