# File 4: modules/fundamental/src/advisory/endpoints/mod.rs (MODIFY)

## Purpose
Register the new severity summary route in the advisory endpoints module.

## Detailed Changes

### Add module declaration

Add at the top of the file alongside existing module declarations:

```rust
mod severity_summary;
```

### Register route

Add a new `.route()` call to the existing `Router::new()` chain. Following the pattern of existing route registrations in this file:

```rust
// Existing pattern (example):
// Router::new()
//     .route("/api/v2/advisory", get(list::list))
//     .route("/api/v2/advisory/:id", get(get::get))

// Add new route:
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::severity_summary))
```

### Design decisions

1. **Route path**: `/api/v2/sbom/:id/advisory-summary` -- the endpoint is scoped under SBOM because it returns advisory data for a specific SBOM. This follows the REST pattern of nesting sub-resources.
2. **HTTP method**: `get()` -- this is a read-only aggregation endpoint.
3. **Handler reference**: `severity_summary::severity_summary` -- module name matches file, function name matches the handler.

### Conventions followed
- **Route registration pattern**: follows the existing `Router::new().route("/path", get(handler))` chaining style.
- **Module declaration**: `mod severity_summary;` follows the pattern of `mod get;` and `mod list;`.
- **Path parameter syntax**: uses `:id` if Axum v1 style, or `{id}` if Axum v2 style -- matches the existing route definitions in this file.

### Note on route location
The Implementation Notes state the route should be registered in `modules/fundamental/src/advisory/endpoints/mod.rs`. While the endpoint path is `/api/v2/sbom/{id}/advisory-summary` (under the SBOM path), the route is registered in the advisory module because the logic and service belong to the advisory domain. This cross-domain routing pattern should be verified against sibling patterns -- if other cross-domain routes exist in advisory's `mod.rs`, this is consistent. If not, flag for user review.
