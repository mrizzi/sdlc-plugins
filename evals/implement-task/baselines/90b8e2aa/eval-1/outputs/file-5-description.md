# File 5: modules/fundamental/src/advisory/endpoints/mod.rs (MODIFY)

## Purpose

Register the new `GET /api/v2/sbom/{id}/advisory-summary` route by declaring the `severity_summary` endpoint module and adding the route to the router.

## Pre-implementation Inspection

Before modifying this file, inspect it thoroughly:

1. **Overview**: Use `mcp__serena_backend__get_symbols_overview` on this file to see the current route registrations and module declarations
2. **Full content**: Use `mcp__serena_backend__find_symbol` with `include_body=true` on the route-building function to see how routes are chained
3. **Pattern confirmation**: Verify the `Router::new().route("/path", get(handler))` pattern and the module declaration style (`mod get;`, `mod list;`)

## Planned Changes

### 1. Add module declaration

Add a new module declaration alongside existing ones:

```rust
mod severity_summary;
```

This is placed alphabetically or after the existing `mod get;` and `mod list;` declarations, following the pattern established by siblings.

### 2. Add route registration

Add the new route to the router chain:

```rust
.route("/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

This is added to the existing `Router::new()` chain in the route registration function.

## Design Decisions

- **Route path**: `/sbom/:id/advisory-summary` -- the route is nested under `/sbom/{id}` because it returns data about a specific SBOM's advisories. The path parameter syntax (`:id` vs `{id}`) will be confirmed by inspecting existing route definitions.
- **HTTP method**: `get()` -- this is a read-only query endpoint
- **Handler reference**: `severity_summary::get_severity_summary` -- fully qualified path to the handler function in the new endpoint module
- **No changes to server/main.rs**: Per the task description, routes auto-mount via module registration, so no changes needed in `server/src/main.rs`

## Notes

- The exact router construction pattern (method chaining, nesting, middleware) will be confirmed from the current file before making changes
- If the router uses nested routers or route groups, the new route will be placed in the appropriate group
- If the advisory endpoints are mounted under a different base path than `/api/v2/advisory`, the route path will be adjusted accordingly

## Conventions Applied

- Module declaration follows existing `mod get;`, `mod list;` pattern
- Route registration follows existing `.route("/path", get(handler))` chaining pattern
