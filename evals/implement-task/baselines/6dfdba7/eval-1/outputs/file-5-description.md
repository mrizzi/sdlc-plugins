# File 5: modules/fundamental/src/advisory/endpoints/mod.rs

## Action: MODIFY

## Purpose

Register the new `GET /api/v2/sbom/{id}/advisory-summary` route in the advisory module's route configuration.

## Conventions Applied

- Follows the existing `Router::new().route("/path", get(handler))` registration pattern.
- New routes are added alongside existing route registrations in the same `mod.rs` file.
- The module for the new handler file is declared with `mod severity_summary;`.

## Detailed Changes

### 1. Add module declaration

Add at the top of the file, alongside existing module declarations (e.g., `mod get;`, `mod list;`):

```rust
mod severity_summary;
```

### 2. Add route registration

Add the new route to the existing router chain. Locate the section where routes are registered (e.g., `Router::new().route(...)`) and add:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::severity_summary))
```

The full router section would look something like:

```rust
Router::new()
    .route("/api/v2/advisory", get(list::list))
    .route("/api/v2/advisory/:id", get(get::get))
    .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::severity_summary))
```

## Notes

- The route path `/api/v2/sbom/:id/advisory-summary` is mounted in the advisory module's router because the logic is about advisories (aggregating advisory severities), even though the path includes `sbom`. This is consistent with the task specification which places the endpoint handler in `advisory/endpoints/`.
- Axum uses `:id` syntax for path parameters (or `{id}` depending on the version). The exact syntax should match what existing routes use in this file.
- If the project uses `utoipa` for OpenAPI, the endpoint may also need to be registered in the API documentation configuration, but this is typically handled at the server level.
