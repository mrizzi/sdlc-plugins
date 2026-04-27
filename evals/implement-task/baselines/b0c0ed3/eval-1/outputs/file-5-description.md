# File 5: `modules/fundamental/src/advisory/endpoints/mod.rs` (MODIFY)

## Purpose

Register the new `GET /api/v2/sbom/{id}/advisory-summary` route in the advisory module's route table.

## Detailed Changes

### Add module declaration

```rust
mod severity_summary;
```

alongside existing `mod get;` and `mod list;` declarations.

### Add route registration

In the function that builds the advisory `Router`, add a new `.route()` call:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_advisory_summary))
```

### Before (expected existing content)

```rust
mod get;
mod list;

// ... (possibly other imports)

pub fn router() -> Router<AppState> {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
}
```

### After

```rust
mod get;
mod list;
mod severity_summary;

// ... (possibly other imports)

pub fn router() -> Router<AppState> {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
        .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_advisory_summary))
}
```

## Design Decisions

- **Route path**: `/api/v2/sbom/:id/advisory-summary` -- the route is conceptually under the SBOM resource (it answers "what advisories affect this SBOM?") but is implemented in the advisory module because it uses `AdvisoryService`. This is consistent with the task specification.
- **Axum path syntax**: Uses `:id` (Axum's path parameter syntax) rather than `{id}` (OpenAPI notation). The task description uses `{id}` for documentation purposes, but actual Axum routes use `:id`.

## Convention Conformance

- Route registration follows the `Router::new().route(...)` chaining pattern.
- Module declaration uses `mod` (private) consistent with endpoint sub-modules being internal.
- Handler reference uses `module::function` pattern matching existing routes.
