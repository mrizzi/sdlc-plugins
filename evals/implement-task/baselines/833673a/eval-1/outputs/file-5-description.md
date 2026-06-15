# File 5: modules/fundamental/src/advisory/endpoints/mod.rs (MODIFY)

## Purpose

Register the new severity summary route in the advisory endpoints module so the GET handler is reachable at `/api/v2/sbom/{id}/advisory-summary`.

## Detailed Changes

### Change 1: Add module declaration

**Location**: At the top of the file, alongside existing module declarations (`mod list;`, `mod get;`).

**Add**:
```rust
mod severity_summary;
```

### Change 2: Register the new route

**Location**: Inside the router builder, following the pattern of existing route registrations.

**Add**:
```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::handler))
```

**Placement**: After the existing advisory route registrations, maintaining consistent ordering.

## Conventions Applied

- **Module declaration**: Uses `mod severity_summary;` matching the pattern of existing `mod list;` and `mod get;` declarations.
- **Route registration**: Follows the `Router::new().route("/path", get(handler))` pattern described in the repo's key conventions and task Implementation Notes.
- **Path parameter**: Uses `:id` Axum path syntax matching sibling route registrations.
- **Handler reference**: Uses `severity_summary::handler` following the `<module>::handler` naming convention seen in sibling modules.
