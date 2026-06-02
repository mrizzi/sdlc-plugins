# File 4: modules/fundamental/src/advisory/endpoints/mod.rs (MODIFY)

## Purpose
Register the new severity summary endpoint route in the advisory module's endpoint router.

## Current State (expected)
The file registers existing advisory routes:
```rust
mod list;
mod get;

pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
}
```

## Changes
1. Add module declaration for the new endpoint handler:
```rust
mod severity_summary;
```

2. Add route registration for the new endpoint:
```diff
 pub fn router() -> Router {
     Router::new()
         .route("/api/v2/advisory", get(list::list_advisories))
         .route("/api/v2/advisory/:id", get(get::get_advisory))
+        .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
 }
```

## Design Decisions
- The route path `/api/v2/sbom/{id}/advisory-summary` follows the task specification. It is registered in the advisory module's router even though the path is under `/sbom/`, because the functionality belongs to the advisory domain (aggregating advisory data for an SBOM).
- The handler function name `get_severity_summary` follows the `get_<resource>` pattern from the sibling `get_advisory` handler.
- Route registration follows the chained `.route()` pattern used by sibling registrations.

## Conventions Applied
- Route registration pattern: `.route("/path", get(module::handler))` chained on the Router builder.
- Module declaration: `mod severity_summary;` alongside `mod list;` and `mod get;`.
