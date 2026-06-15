# File 5: modules/fundamental/src/advisory/endpoints/mod.rs

## Action: MODIFY

## Purpose

Register the new `severity_summary` endpoint handler and declare the new `severity_summary` module in the advisory endpoints module.

## Detailed Changes

### Change 1: Add module declaration

Add the module declaration for the new handler file alongside the existing declarations for `get` and `list`:

```rust
// Existing:
mod get;
mod list;

// Add:
mod severity_summary;
```

### Change 2: Register the new route

In the route registration function (where `Router::new().route(...)` calls are chained), add the new route for the advisory summary endpoint:

```rust
// Add to the router chain:
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

This follows the pattern of existing `.route("/path", get(handler))` registrations in the same file.

## Notes

- The exact location and syntax of the route addition depends on how the existing routes are structured in this file. Before implementing, I would use `mcp__serena_backend__get_symbols_overview` on this file to see the full route registration pattern, then use `mcp__serena_backend__find_symbol` to read the specific router-building function.
- The route path `/api/v2/sbom/:id/advisory-summary` is scoped under the SBOM resource (not the advisory resource) because the endpoint returns advisory data in the context of a specific SBOM. This is a cross-resource endpoint. If the project convention places such endpoints differently, I would adapt based on the actual codebase inspection.
- Alternatively, if this route should be registered in the SBOM endpoints module instead of the advisory endpoints module, I would move the registration there. The task description says to register in `advisory/endpoints/mod.rs`, so I follow the task unless codebase inspection reveals otherwise.

## Conventions Applied

- **Route registration**: Follows the `Router::new().route("/path", get(handler))` pattern used by existing routes
- **Module declaration**: Uses `mod severity_summary;` following the same pattern as `mod get;` and `mod list;`
- **Handler reference**: References `severity_summary::get_severity_summary` using the module::function pattern
