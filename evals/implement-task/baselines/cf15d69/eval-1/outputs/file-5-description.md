# File 5: modules/fundamental/src/advisory/endpoints/mod.rs (MODIFY)

## Purpose

Register the new advisory severity summary route in the advisory module's route configuration.

## Detailed Changes

Two modifications to the existing `mod.rs`:

### 1. Add module declaration

Add at the top with the other module declarations:

```rust
mod severity_summary;
```

### 2. Register the route

Add the new route to the existing `Router::new()` chain:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_advisory_summary))
```

This line would be added after the existing `.route(...)` registrations in the router builder, following the same pattern as the existing `get.rs` and `list.rs` route registrations.

## Convention Conformance

- **Route registration pattern**: Follows the existing `Router::new().route("/path", get(handler))` pattern described in the repository conventions.
- **Module declaration**: Matches the existing `mod get;` and `mod list;` declarations at the top of the file.
- **Route path**: Uses the `:id` parameter syntax (Axum convention) matching existing routes like `/api/v2/advisory/:id`.
- **Handler reference**: Uses `severity_summary::get_advisory_summary` -- module-qualified function name, consistent with how other handlers are referenced.

## Notes

The exact router construction pattern (whether routes are chained with `.route()` or use `.merge()`) would be confirmed by reading the file during Step 4. The path parameter syntax (`:id` vs `{id}`) would also be verified -- the task description uses `{id}` in the API spec but Axum uses `:id` in route definitions. The actual implementation would match whatever syntax the existing routes use.
