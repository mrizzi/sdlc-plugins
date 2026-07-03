# File 5: modules/fundamental/src/advisory/endpoints/mod.rs

**Action**: MODIFY

## Purpose

Register the new `GET /api/v2/sbom/{id}/advisory-summary` route by adding the
severity summary handler module and adding its route to the router.

## Detailed Changes

### Add module declaration

Add a `mod severity_summary;` declaration alongside the existing `mod get;` and `mod list;` declarations:

```rust
mod get;
mod list;
mod severity_summary;  // NEW
```

### Add route registration

Add the new route to the existing `Router::new()` chain. Following the pattern of existing
route registrations in this file:

```rust
// Existing routes (example pattern):
Router::new()
    .route("/api/v2/advisory", get(list::list_advisories))
    .route("/api/v2/advisory/:id", get(get::get_advisory))
    // NEW: Advisory severity summary for an SBOM
    .route(
        "/api/v2/sbom/:id/advisory-summary",
        get(severity_summary::get_severity_summary),
    )
```

## Conventions Applied

- **Module declaration**: Uses `mod <name>;` in the endpoints `mod.rs`, matching the pattern for `get` and `list` modules.
- **Route registration**: Uses `Router::new().route("/path", get(handler))` chaining, matching the existing registration pattern.
- **Path parameters**: Uses `:id` syntax for path parameters, consistent with Axum routing conventions.
- **Handler reference**: References the handler as `module::function_name`, matching how `get::get_advisory` and `list::list_advisories` are referenced.

## Notes

- The route path `/api/v2/sbom/{id}/advisory-summary` is nested under the SBOM resource path since it returns data about a specific SBOM's advisories, even though it lives in the advisory module's endpoints. This is specified in the task description.
- No changes to `server/src/main.rs` are needed because routes auto-mount via module registration, as stated in the task description.
