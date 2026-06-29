# File 5: Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

## Purpose

Register the new severity summary endpoint route in the advisory module's route configuration.

## Detailed Changes

### Add module declaration

Add the module declaration for the new endpoint file:

```rust
mod severity_summary;
```

### Add route registration

In the route builder function (where existing routes like `get.rs` and `list.rs` are registered), add the new route:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_advisory_summary))
```

This follows the existing pattern of `Router::new().route("/path", get(handler))` chaining seen in the sibling route registrations.

### Import additions

Add the import for the `get` method from Axum routing if not already present (it likely already is since the module registers other GET routes).

## Convention Compliance

- **Route registration**: Follows the `Router::new().route(...)` chaining pattern from sibling registrations
- **Path convention**: Uses `:id` parameter syntax consistent with Axum's path parameter format
- **Handler reference**: Uses `module::function` reference pattern (e.g., `severity_summary::get_advisory_summary`)
- **Scope**: Minimal change -- one module declaration and one route registration line
