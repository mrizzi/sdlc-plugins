# File 2: modules/fundamental/src/advisory/endpoints/mod.rs

## Action: MODIFY

## Summary

Register the new `/api/v2/sbom/{id}/advisory-summary` route in the advisory module's
endpoint registration file.

## Detailed Changes

### Add module declaration

Add at the top of the file alongside existing module declarations:

```rust
pub mod severity_summary;
```

### Add route registration

Inside the route registration function (following the existing `Router::new().route(...)` pattern), add:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

This follows the existing pattern where each endpoint handler is in its own module file and
the handler function is referenced as `module::function_name`.

### Add import

If not already imported via the module declaration, ensure the `get` function from Axum
routing is available:

```rust
use axum::routing::get;
```

## Conventions Applied

- **Route registration pattern:** Matches the existing `Router::new().route("/path", get(handler))` pattern used for `list.rs` and `get.rs`.
- **Module organization:** Each endpoint handler lives in its own file, declared as `pub mod` in `mod.rs`.
- **Path parameter syntax:** Uses Axum's `:id` syntax for path parameters (or `{id}` depending on Axum version).
- **URL pattern:** Follows the `/api/v2/<resource>/{id}/<sub-resource>` pattern for sub-resource endpoints.
