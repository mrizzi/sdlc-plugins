# File 4: modules/fundamental/src/advisory/endpoints/mod.rs (MODIFY)

## Purpose
Register the new severity summary route in the advisory endpoints module.

## Detailed Changes

### Add module declaration

Add at the top of the file alongside existing module declarations:

```rust
pub mod severity_summary;
```

### Add route registration

In the router builder function, add the new route following the existing pattern of `Router::new().route(...)` registrations:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

## Conventions Applied
- **Route registration**: follows the existing `Router::new().route("/path", get(handler))` pattern used in sibling endpoint modules
- **Module declaration**: `pub mod severity_summary;` follows the pattern of other endpoint module declarations
- **Route path**: uses `/api/v2/sbom/:id/advisory-summary` matching the API specification from the task
- **HTTP method**: uses `get()` for a read-only aggregation endpoint
