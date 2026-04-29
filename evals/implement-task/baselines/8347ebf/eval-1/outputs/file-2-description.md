# File 2: modules/fundamental/src/advisory/endpoints/mod.rs

## Change Type: Modify

## Purpose

Register the new severity summary route in the advisory endpoints module so that `GET /api/v2/sbom/{id}/advisory-summary` is accessible via the API.

## Detailed Changes

### 1. Add module declaration

Add a `mod severity_summary;` declaration at the top of the file alongside existing module declarations (e.g., `mod list;`, `mod get;`):

```rust
mod severity_summary;
```

### 2. Register the new route

Add a new `.route()` call in the router builder, following the existing pattern of `Router::new().route("/path", get(handler))` registrations:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

This should be added in the chain of existing `.route()` calls within the function that builds the advisory router.

## Conventions Applied

- Module declaration style matches existing `mod list;`, `mod get;` pattern
- Route registration uses `Router::new().route()` chain pattern
- Path parameter uses Axum's `:id` syntax for path extraction
- Handler reference follows `module::function_name` pattern
- Route path follows REST conventions consistent with existing endpoints

## Notes

The route is registered under `/api/v2/sbom/{id}/advisory-summary` as specified in the API Changes section. This is a cross-domain route (advisory data scoped by SBOM ID), which is a valid REST pattern. The `server/src/main.rs` does not need changes since routes auto-mount via module registration.
