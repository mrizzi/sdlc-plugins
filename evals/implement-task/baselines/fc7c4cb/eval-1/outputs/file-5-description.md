# File 5: modules/fundamental/src/advisory/endpoints/mod.rs (MODIFY)

## Purpose

Register the new `GET /api/v2/sbom/{id}/advisory-summary` route in the advisory endpoint module.

## Pre-Implementation Inspection

Before modifying, inspect this file using:
- `mcp__serena_backend__get_symbols_overview` to see the current route registration structure
- Read the file to see the existing `Router::new().route(...)` chain and module declarations
- Inspect `modules/fundamental/src/sbom/endpoints/mod.rs` as a sibling to confirm the registration pattern

## Detailed Changes

### Add module declaration

At the top of the file, alongside existing module declarations (e.g., `mod get;`, `mod list;`):

```rust
mod severity_summary;
```

### Add route registration

In the router builder, add the new route following the existing pattern:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

This line is added within the existing `Router::new()` chain, alongside the existing route registrations like `.route("/api/v2/advisory", get(list::list_advisories))` and `.route("/api/v2/advisory/:id", get(get::get_advisory))`.

### Design Decisions

- **Route path**: `/api/v2/sbom/:id/advisory-summary` -- the path is scoped under `/sbom/{id}` because the summary is per-SBOM, matching the API design in the task description.
- **Module registration**: `mod severity_summary;` follows the same pattern as `mod get;` and `mod list;` in the file.
- **Handler reference**: Uses `severity_summary::get_severity_summary` to reference the handler function from the new endpoint file.
- **Axum path parameter syntax**: Uses `:id` (Axum's path parameter syntax) rather than `{id}` (OpenAPI notation).

### Convention Conformance

- Route registration follows the `Router::new().route("/path", get(handler))` pattern used by all existing routes.
- Module declaration follows the existing `mod <name>;` pattern.
