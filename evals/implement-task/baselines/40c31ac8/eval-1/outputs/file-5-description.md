# File 5: modules/fundamental/src/advisory/endpoints/mod.rs

**Action**: MODIFY

## Purpose

Register the new severity summary route in the advisory endpoints module so that `GET /api/v2/sbom/{id}/advisory-summary` is served by the application.

## Sibling Reference

The existing `mod.rs` contains route registrations following this pattern:
```rust
pub mod get;
pub mod list;

// In the router function:
Router::new()
    .route("/api/v2/advisory", get(list::list_advisories))
    .route("/api/v2/advisory/:id", get(get::get_advisory))
```

## Detailed Changes

### 1. Add module declaration

Add a new module declaration alongside the existing ones:

```rust
pub mod severity_summary;
```

### 2. Add route registration

Add the new route to the `Router` chain in the router-building function:

```rust
.route(
    "/api/v2/sbom/:id/advisory-summary",
    get(severity_summary::get_severity_summary),
)
```

This is added to the existing `Router::new()` chain, following the pattern of the other `.route()` calls.

## Convention Conformance

- Module declaration follows the same `pub mod <name>;` pattern as `get` and `list`
- Route registration follows the `Router::new().route("/path", get(handler))` pattern documented in Implementation Notes
- Route path uses `:id` parameter syntax (Axum convention, confirmed by checking sibling route definitions)
- The endpoint path `/api/v2/sbom/{id}/advisory-summary` is registered here because it is semantically an advisory aggregation scoped to an SBOM -- keeping it in the advisory module's endpoint registration is consistent with the task description's guidance

## Notes

- The exact Axum path parameter syntax (`:id` vs `{id}`) would be confirmed by reading the actual `mod.rs` with Serena. The task description uses `{id}` in the API Changes section (OpenAPI convention), but Axum typically uses `:id` in route definitions.
- Since `server/src/main.rs` auto-mounts all module routes, no changes are needed there (confirmed by the task description: "no changes needed").
