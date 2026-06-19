# File 5: modules/fundamental/src/advisory/endpoints/mod.rs (MODIFY)

## Purpose

Register the new `GET /api/v2/sbom/{id}/advisory-summary` route by adding the severity_summary handler to the router.

## Detailed Changes

### Inspect before modifying

- Read `modules/fundamental/src/advisory/endpoints/mod.rs` to see:
  - How existing routes are registered (e.g., `Router::new().route("/path", get(handler))`)
  - How handler modules are declared (e.g., `mod get;`, `mod list;`)
  - The router builder pattern and how routes are chained

### Changes

1. Add module declaration for the new endpoint file:

```rust
// Existing:
mod get;
mod list;

// Add:
mod severity_summary;
```

2. Add route registration in the router builder:

```rust
// Add to the existing Router chain:
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

### Notes

- The exact path parameter syntax (`:id` vs `{id}`) depends on the Axum version used — inspect siblings to confirm
- Place the new route registration adjacent to existing advisory routes, following the ordering pattern in the file
- The module declaration should be placed alphabetically with existing declarations
- If the router uses a nested/scoped pattern (e.g., routes scoped under `/api/v2/`), follow that scoping pattern rather than using the full path
