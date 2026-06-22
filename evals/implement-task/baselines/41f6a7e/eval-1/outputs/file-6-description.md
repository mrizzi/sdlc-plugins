# File 6: modules/fundamental/src/advisory/endpoints/mod.rs (MODIFY)

## Purpose

Register the new `GET /api/v2/sbom/{id}/advisory-summary` route in the advisory module's endpoint registration.

## Detailed Changes

### Add module declaration

Add a `mod severity_summary;` declaration alongside the existing endpoint module declarations (`mod get;`, `mod list;`).

### Add route registration

Add a new `.route()` call in the router builder, following the pattern of existing route registrations.

### Before (expected current state)

```rust
mod get;
mod list;

// ... imports ...

pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
}
```

### After

```rust
mod get;
mod list;
mod severity_summary;

// ... imports ...

pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
        .route(
            "/api/v2/sbom/:id/advisory-summary",
            get(severity_summary::get_advisory_summary),
        )
}
```

## Conventions followed

- **Module declaration**: `mod severity_summary;` follows the pattern of `mod get;` and `mod list;`
- **Route registration**: Uses `Router::new().route("/path", get(handler))` pattern matching existing registrations
- **Path convention**: Uses `:id` parameter syntax (or `{id}` depending on Axum version -- would confirm from sibling routes)
- **Handler reference**: Uses `module::function` pattern (e.g., `severity_summary::get_advisory_summary`)
- **Placement**: New route added after existing routes, maintaining logical grouping

## Notes

- The exact route path parameter syntax (`:id` vs `{id}`) would be confirmed by inspecting the existing routes via Serena
- The endpoint path `/api/v2/sbom/{id}/advisory-summary` is an SBOM-scoped path registered in the advisory module -- this cross-domain scoping would be verified as acceptable by checking if similar patterns exist in the codebase
- If the advisory module's router does not handle SBOM-scoped routes, the route might need to be registered in the SBOM module's `endpoints/mod.rs` instead. This would be determined during Step 4's code inspection and flagged as a deviation.
- `server/src/main.rs` requires no changes as routes auto-mount via module registration
