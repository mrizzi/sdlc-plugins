# File 5: modules/fundamental/src/advisory/endpoints/mod.rs

**Action:** MODIFY

## Purpose

Register the new severity summary route in the advisory endpoints module so it is automatically mounted when the server starts.

## Detailed Changes

### 1. Add module declaration

Add at the top with existing module declarations:

```rust
mod severity_summary;
```

### 2. Add route registration

Add the new route to the existing `Router::new()` chain. Following the pattern of existing route registrations:

```rust
// In the router builder function (e.g., pub fn router() -> Router<...>)
// Add alongside existing routes:
.route(
    "/api/v2/sbom/:id/advisory-summary",
    get(severity_summary::get_severity_summary),
)
```

### Before (conceptual):

```rust
mod get;
mod list;

pub fn router() -> Router<AppState> {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
}
```

### After (conceptual):

```rust
mod get;
mod list;
mod severity_summary;

pub fn router() -> Router<AppState> {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
        .route(
            "/api/v2/sbom/:id/advisory-summary",
            get(severity_summary::get_severity_summary),
        )
}
```

## Conventions Applied

- **Module declaration:** Uses `mod severity_summary;` following the pattern of `mod get;` and `mod list;` in the same file
- **Route registration:** Uses `Router::new().route("/path", get(handler))` pattern matching existing registrations
- **Path parameter syntax:** Uses `:id` for Axum path parameters (would verify whether the project uses `:id` or `{id}` -- Axum supports both, but consistency with siblings matters)
- **Handler reference:** Uses `module::function_name` pattern for the handler reference
- **Alphabetical ordering:** Module declaration placed in alphabetical order among siblings

## Notes

- The exact path parameter syntax (`:id` vs `{id}`) would be confirmed by inspecting the existing route registrations in the file
- The router function name and return type would be confirmed by inspecting the actual `mod.rs` with Serena
- The route path `/api/v2/sbom/:id/advisory-summary` is defined by the API Changes in the task description, even though this endpoint is registered in the advisory module's routes. This cross-domain routing pattern would be verified against existing patterns in the codebase
