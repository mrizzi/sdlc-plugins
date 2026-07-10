# File 3: modules/fundamental/src/advisory/endpoints/mod.rs (MODIFY)

## Purpose

Register the new `GET /api/v2/sbom/{id}/advisory-summary` route so incoming HTTP requests are routed to the severity summary handler.

## Pre-change Inspection

Before modifying, inspect the file using:
```
mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/endpoints/mod.rs")
```

Also search for the route registration pattern:
```
mcp__serena_backend__search_for_pattern("Router::new().route")
```

Expect to see existing route registrations like:
```rust
mod get;
mod list;

pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
}
```

## Changes

1. **Add module declaration** for the new endpoint file:

```rust
mod severity_summary;
```

2. **Add route registration** for the new endpoint. Following the existing `Router::new().route(...)` chain pattern:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

## Full Expected State After Change

```rust
mod get;
mod list;
mod severity_summary;

pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
        .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
}
```

## Notes

- The path parameter syntax (`:id` vs `{id}`) depends on the Axum version used in the project. Axum 0.6+ uses `/:id`, while the task description uses `{id}` in the API specification. Would verify the actual syntax by inspecting existing routes.
- The route is under `/api/v2/sbom/{id}/advisory-summary` even though it is registered in the advisory endpoints module, because it is a summary of advisories *for* a specific SBOM. This is consistent with the task description.
- The `server/main.rs` auto-mounts modules, so no changes are needed there.
