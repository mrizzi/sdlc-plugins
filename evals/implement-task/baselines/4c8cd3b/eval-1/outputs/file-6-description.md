# File 6: modules/fundamental/src/advisory/endpoints/mod.rs

**Action:** MODIFY

## Purpose

Register the new severity summary endpoint route and declare the new endpoint module.

## Detailed Changes

### 1. Add module declaration

Add the module declaration for the new endpoint file at the top of the file alongside existing module declarations:

```rust
// Existing:
mod get;
mod list;

// Add:
mod severity_summary;
```

### 2. Register the route

Add the new route to the existing `Router` configuration, following the pattern of existing route registrations:

```rust
// Existing route registrations (example pattern):
Router::new()
    .route("/api/v2/advisory", get(list::list_advisories))
    .route("/api/v2/advisory/:id", get(get::get_advisory))
    // Add this new route:
    .route(
        "/api/v2/sbom/:id/advisory-summary",
        get(severity_summary::get_severity_summary),
    )
```

## Notes

- The route path `/api/v2/sbom/:id/advisory-summary` is nested under the SBOM path since it returns data scoped to a specific SBOM, even though the handler logic lives in the advisory module. This is consistent with the task specification.
- The route registration follows the exact same `Router::new().route(path, get(handler))` pattern used by existing routes.

## Conventions Applied

- **Module declaration:** `mod severity_summary;` follows the same pattern as `mod get;` and `mod list;`.
- **Route registration:** Uses `.route()` chaining on the existing `Router`, matching the pattern in sibling endpoint `mod.rs` files.
- **Path parameter syntax:** Uses `:id` Axum path parameter syntax, consistent with existing routes like `/api/v2/advisory/:id`.
