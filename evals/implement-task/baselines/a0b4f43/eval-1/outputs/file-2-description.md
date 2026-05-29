# File 2: Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

## Purpose

Register the new severity summary route in the advisory module's endpoint router.

## Pre-Change Analysis

Before modifying, read this file to understand:
- How existing routes are registered (the `Router::new().route(...)` chain pattern)
- What handler modules are already declared via `mod` statements
- The exact import/module declaration style used

## Detailed Changes

### Add Module Declaration

Add a new module declaration for the severity summary endpoint handler:

```rust
mod severity_summary;
```

This goes alongside existing declarations like `mod get;` and `mod list;`.

### Register the Route

Add the new route to the existing router chain:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get))
```

This follows the same `Router::new().route("/path", get(handler))` pattern used for existing advisory and SBOM endpoints. The `:id` path parameter matches Axum's path extraction convention used in `get.rs`.

### Complete Change Context

The modification is minimal — two lines added (one `mod` declaration, one `.route()` call) following the exact pattern of sibling routes already in this file.
