# File 5: Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

## Action: MODIFY

## Purpose

Register the new `GET /api/v2/sbom/{id}/advisory-summary` route by adding the severity_summary handler to the module's router configuration.

## Detailed Changes

### New Module Declaration

Add a module declaration for the new endpoint file:

```rust
mod severity_summary;
```

This should be placed alongside the existing module declarations (`mod list;`, `mod get;`).

### Route Registration

Add the new route to the `Router` builder, following the existing pattern of `.route("/path", get(handler))`:

```rust
// In the function that builds and returns the Router:
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::severity_summary))
```

This should be added after the existing advisory route registrations (e.g., the `/api/v2/advisory` and `/api/v2/advisory/{id}` routes).

### Complete Change Context

The existing `mod.rs` likely looks like:

```rust
mod list;
mod get;

pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list))
        .route("/api/v2/advisory/:id", get(get::get))
}
```

After modification:

```rust
mod list;
mod get;
mod severity_summary;

pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list))
        .route("/api/v2/advisory/:id", get(get::get))
        .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::severity_summary))
}
```

### Note on Route Path

The endpoint path `/api/v2/sbom/{id}/advisory-summary` is registered in the advisory module rather than the SBOM module because it aggregates advisory data. The path is namespaced under `/sbom/{id}` since the query is scoped to a specific SBOM. This is a cross-domain route that lives in the advisory module based on the task specification.

## Conventions Applied

- **Route pattern**: Uses Axum's `.route("/path", get(handler))` pattern matching existing registrations
- **Module declaration**: `mod severity_summary;` follows the naming convention of sibling module declarations
- **Path parameter syntax**: Uses Axum's `:id` syntax for path parameters (Axum convention)
- **Handler reference**: `severity_summary::severity_summary` follows the pattern of `get::get` and `list::list` in siblings
