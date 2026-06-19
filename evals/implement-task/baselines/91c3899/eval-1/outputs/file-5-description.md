# File 5: modules/fundamental/src/advisory/endpoints/mod.rs

**Action**: MODIFY

## Purpose

Register the new `GET /api/v2/sbom/{id}/advisory-summary` route in the advisory module's route configuration.

## Sibling Reference

The existing `endpoints/mod.rs` registers routes using the pattern:
```rust
mod list;
mod get;

// In the router function:
Router::new()
    .route("/api/v2/advisory", get(list::list_advisories))
    .route("/api/v2/advisory/:id", get(get::get_advisory))
```

Following this exact pattern for the new endpoint.

## Detailed Changes

### 1. Add module declaration

Add at the top with existing module declarations:

```rust
mod severity_summary;
```

### 2. Add route registration

Add a new `.route()` call to the `Router` builder:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

### Before (expected current state)

```rust
mod list;
mod get;

// ... router setup
pub fn router() -> Router<AppState> {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
}
```

### After

```rust
mod list;
mod get;
mod severity_summary;

// ... router setup
pub fn router() -> Router<AppState> {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
        .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
}
```

## Design Notes

- The route path `/api/v2/sbom/{id}/advisory-summary` is nested under the SBOM resource since it returns advisory data for a specific SBOM
- Even though this endpoint is registered in the advisory module's router, the path reflects the SBOM-centric nature of the query -- this is acceptable since the advisory module owns the advisory aggregation logic
- The route uses Axum's `:id` path parameter syntax (equivalent to `{id}` in the API spec)
- The `get()` function import is from `axum::routing::get`, matching the existing pattern
- Route registration follows the chained `.route()` builder pattern used by sibling routes
