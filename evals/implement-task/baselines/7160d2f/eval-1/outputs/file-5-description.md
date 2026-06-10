# File 5: modules/fundamental/src/advisory/endpoints/mod.rs

**Action**: MODIFY

**Purpose**: Register the new severity summary route in the advisory endpoint module's router.

## Detailed Changes

1. Add import for the new handler module at the top of the file:

```rust
mod severity_summary;
```

2. Add the new route registration in the router builder, following the existing pattern of `Router::new().route(...)` calls:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

This line would be added alongside the existing route registrations in the router construction.

## Conventions Followed

- **Route registration pattern**: `Router::new().route("/path", get(handler))` -- matching the existing pattern in `endpoints/mod.rs` for advisory routes.
- **Path parameter syntax**: `:id` or `{id}` depending on which Axum version/syntax the project uses (would confirm by inspecting existing route definitions).
- **Module import**: `mod severity_summary;` at the top of the file, following the same pattern as existing handler module imports.
- **HTTP method**: `get(...)` for the GET endpoint.

## Serena Usage

Would use:
1. `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/mod.rs` to see current route registration structure
2. `mcp__serena_backend__find_symbol` with `include_body=true` on the router function/builder to see exact syntax
3. `mcp__serena_backend__insert_after_symbol` or Edit tool to add the new route

## Notes

- The route path `/api/v2/sbom/{id}/advisory-summary` is specified in the task's API Changes section. The exact path parameter syntax (`:id` vs `{id}`) would be confirmed from sibling routes.
- The route is under `/api/v2/sbom/` namespace even though the handler is in the advisory module -- this is because the endpoint aggregates advisories *for a given SBOM*. Would verify this cross-module route registration is consistent with how the project organizes routes, or if it should be registered in the SBOM endpoints module instead.
