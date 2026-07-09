# File 2: `modules/fundamental/src/advisory/endpoints/mod.rs` (MODIFY)

## Pre-modification inspection

Before modifying this file, inspect it using:
- `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/endpoints/mod.rs")` to see the existing route registration structure.
- Read the file to see how `Router::new().route()` chains are organized and how handler modules are declared.

Also inspect sibling endpoint registration:
- `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/sbom/endpoints/mod.rs")` to compare the SBOM module's route registration pattern.

## Changes

### Add module declaration

Add a new module declaration for the severity summary endpoint handler:

```rust
pub mod severity_summary;
```

This should be placed alongside the existing module declarations (`pub mod get;`, `pub mod list;`), in alphabetical order or following the existing ordering convention.

### Register the new route

In the function that builds the `Router` (likely a `pub fn configure()` or similar), add the new route:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::handler))
```

This follows the existing pattern of `Router::new().route("/path", get(handler))` registrations seen in the sibling endpoints.

### Conventions followed

- **Module declaration**: Matches existing `pub mod get;` and `pub mod list;` declarations in the same file.
- **Route registration**: Follows the `Router::new().route()` chain pattern.
- **Path convention**: Uses Axum's `:id` path parameter syntax (or `{id}` depending on the Axum version used in the project -- inspect the existing routes to confirm).
- **Handler reference**: References `severity_summary::handler` following the pattern of `get::handler`, `list::handler`.

### Backward compatibility

Existing routes are not modified. The new route is additive only. Verified that no existing route conflicts with `/api/v2/sbom/:id/advisory-summary`.
