# File 5: modules/fundamental/src/advisory/endpoints/mod.rs (MODIFY)

## Purpose

Register the new severity summary endpoint route and declare the new submodule.

## Detailed Changes

### Add module declaration

Add the following line alongside existing module declarations (e.g., next to `mod get;`
and `mod list;`):

```rust
mod severity_summary;
```

### Add route registration

In the router construction function (where `Router::new()` chains `.route(...)` calls),
add the new route:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_advisory_summary))
```

This follows the existing pattern of route registration in the same file. The route path
uses Axum's `:id` syntax for path parameters (matching the pattern seen in sibling routes
like `/api/v2/advisory/:id`).

## Example of the change in context

Before:
```rust
mod get;
mod list;

pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
}
```

After:
```rust
mod get;
mod list;
mod severity_summary;

pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
        .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_advisory_summary))
}
```

## Conventions followed

- Module declaration alphabetically ordered or grouped logically with siblings
- Route registration follows existing `Router::new().route(...)` pattern
- Route path uses kebab-case (`advisory-summary`) matching API convention
- Handler reference uses `module::function` pattern
