# File 5: Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

## Action: MODIFY

## Purpose

Register the new severity summary endpoint route and declare the new endpoint module.

## Detailed Changes

### 1. Add module declaration at the top of the file

```rust
// Existing module declarations:
mod get;
mod list;

// Add this line:
mod severity_summary;
```

### 2. Add route registration in the router builder

Within the function that builds the advisory routes (likely a `pub fn router()` or similar function), add the new route:

```rust
// Existing route registrations (not modified):
Router::new()
    .route("/api/v2/advisory", get(list::list_advisories))
    .route("/api/v2/advisory/:id", get(get::get_advisory))
    // Add this line:
    .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

Note: The route path `/api/v2/sbom/{id}/advisory-summary` is registered here in the advisory module's router because the feature is advisory-centric (aggregating advisory severities), even though the URL path is nested under the SBOM resource. This follows the task's explicit instruction to register the route in the advisory endpoints module.

## Conventions Applied

- **Module declaration**: Uses `mod module_name;` pattern matching existing declarations for `get` and `list`
- **Route registration**: Uses `Router::new().route(path, get(handler))` pattern observed in sibling `endpoints/mod.rs` files
- **Handler reference**: References the handler as `severity_summary::get_severity_summary` following the `module::function` pattern used for `get::get_advisory` and `list::list_advisories`
- **Path parameter syntax**: Uses Axum's `:id` syntax (or `{id}` depending on the Axum version in use) for path parameters
