# File 5: modules/fundamental/src/advisory/endpoints/mod.rs

## Action: MODIFY

## Purpose
Register the new severity summary endpoint route and declare the new endpoint module.

## Sibling Reference
Follows the existing route registration pattern in the same file -- uses
`Router::new().route("/path", get(handler))` and `mod` declarations for
endpoint sub-modules (e.g., `mod get;`, `mod list;`).

## Detailed Changes

### Add module declaration

Add the following line alongside the existing module declarations (e.g., next to
`mod get;` and `mod list;`):

```rust
mod severity_summary;
```

### Register the route

In the function that builds the router (likely a `pub fn configure()` or similar
that returns a `Router`), add the new route alongside existing route registrations:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::handler))
```

## Notes
- The route path `/api/v2/sbom/:id/advisory-summary` follows Axum's path parameter syntax (`:id`).
- The route is registered in the advisory module's endpoints even though the URL path starts with `/api/v2/sbom/` -- this is because the endpoint logically belongs to advisory aggregation and the task description specifies it should be registered here.
- The `get()` function is from `axum::routing::get`.
- No changes needed in `server/src/main.rs` since routes auto-mount via module registration.
- The exact placement within the router chain would be determined by reading the current `mod.rs` file structure via Serena.
