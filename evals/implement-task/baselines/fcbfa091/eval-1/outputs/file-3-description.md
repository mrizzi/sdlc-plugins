# File 3: modules/fundamental/src/advisory/endpoints/mod.rs (MODIFY)

## Purpose

Register the new severity summary route in the advisory module's route configuration so that `GET /api/v2/sbom/{id}/advisory-summary` is accessible.

## Current state (inspected via Serena)

The file currently registers advisory-related routes using Axum's `Router`:

```rust
pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
}
```

The pattern uses `Router::new().route("/path", get(handler))` chaining.

## Changes

Add the new route registration and module declaration:

1. Add module import at the top:
```rust
mod severity_summary;
```

2. Add route to the router chain:
```rust
pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
        .route(
            "/api/v2/sbom/:id/advisory-summary",
            get(severity_summary::get_severity_summary),
        )
}
```

## Rationale

The new endpoint is under `/api/v2/sbom/{id}/advisory-summary` (not under `/api/v2/advisory/`) because it is scoped to a specific SBOM -- it returns advisory severity counts for that SBOM. This is consistent with the task's API Changes section. The route is registered in the advisory module because it queries advisory data, even though the path is under the SBOM resource namespace.

## Conventions applied

- Route registration follows the existing `Router::new().route(...)` chaining pattern
- Handler reference uses `module::function` naming consistent with `list::list_advisories` and `get::get_advisory`
- Module import (`mod severity_summary;`) added alongside existing endpoint module imports
