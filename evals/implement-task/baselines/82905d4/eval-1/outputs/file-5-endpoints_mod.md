# File 5: `modules/fundamental/src/advisory/endpoints/mod.rs` (MODIFY)

## Purpose

Register the new severity summary endpoint route so it is served by the application.

## Changes

### Change 1: Add module declaration

At the top of the file, alongside existing endpoint module declarations:

```rust
// Existing declarations (example):
mod get;
mod list;

// ADD:
mod severity_summary;
```

### Change 2: Register the route

In the router construction function (wherever `Router::new()` or route mounting happens), add the new route:

```rust
// Existing routes (example):
Router::new()
    .route("/api/v2/advisory/:id", get(get::get_advisory))
    .route("/api/v2/advisory", get(list::list_advisories))
    // ADD:
    .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

## Design Decisions

1. **Route path**: `/api/v2/sbom/:id/advisory-summary` — uses the colon-prefixed parameter style if Axum, or curly-brace style `{id}` depending on the router. The exact syntax will match whatever existing routes use.

2. **Placement in advisory endpoints module**: Although the route path is under `/sbom/`, the handler logically belongs with advisory endpoints because it aggregates advisory data. The service method lives on `AdvisoryService`. This follows the task description's explicit instruction to register the route in the advisory endpoints module.

3. **HTTP method**: `get` — this is a read-only aggregation query. Consistent with similar summary/dashboard endpoints.

## Notes

The exact router syntax and import for `get` (e.g., `axum::routing::get` vs `axum::extract::get`) will be confirmed by inspecting the existing `mod.rs` file during pre-implementation inspection. The registration follows whatever pattern is already established.
