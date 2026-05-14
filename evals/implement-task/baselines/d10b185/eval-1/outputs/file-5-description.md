# File 5: modules/fundamental/src/advisory/endpoints/mod.rs

**Action**: MODIFY

## Purpose

Register the new severity summary route in the advisory module's endpoint router.

## Detailed Changes

Add the module declaration and route registration:

**1. Add module declaration** (at the top of the file, alongside existing module declarations):

```rust
pub mod severity_summary;
```

This should be placed alphabetically or after the existing `get` and `list` module declarations, following the file's current ordering.

**2. Add route registration** (inside the router builder function, alongside existing `.route()` calls):

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

### Example of the modified router builder (conceptual diff):

```diff
 pub fn router() -> Router<AppState> {
     Router::new()
         .route("/api/v2/advisory", get(list::list_advisories))
         .route("/api/v2/advisory/:id", get(get::get_advisory))
+        .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
 }
```

Also add the import if needed:

```rust
use axum::routing::get;
```

## Conventions Applied

- **Route registration pattern**: Follows the existing `Router::new().route("/path", get(handler))` chaining pattern visible in sibling `endpoints/mod.rs` files.
- **Path parameter syntax**: Uses Axum's `:id` syntax for path parameters (or `{id}` if the codebase uses the newer Axum version with brace syntax).
- **Module declaration**: Simple `pub mod severity_summary;` to make the handler accessible.
- **Route path**: `/api/v2/sbom/:id/advisory-summary` as specified in the task's API Changes section.

## Design Note

The route is registered in the advisory module's endpoint router even though the URL path starts with `/api/v2/sbom/`. This is because the endpoint aggregates advisory data (the advisory domain owns the logic), and the route will be mounted correctly regardless of which module registers it since `server/main.rs` mounts all module routers at the root level.
