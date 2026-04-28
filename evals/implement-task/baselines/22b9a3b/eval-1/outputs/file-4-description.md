# File 4: modules/fundamental/src/advisory/endpoints/mod.rs

## Action: MODIFY

## Purpose

Register the new severity summary endpoint route in the advisory module's endpoint registration file. This adds both the module declaration and the route to the router.

## Sibling Reference

The existing `mod.rs` already registers routes for `list.rs` and `get.rs` using the `Router::new().route("/path", get(handler))` pattern. The new route follows the same registration approach.

## Detailed Changes

### Add module declaration

Add near the top of the file alongside the existing module declarations:

```rust
mod severity_summary;
```

### Add route registration

Add the new route to the existing `Router::new()` chain:

```rust
use severity_summary::get_severity_summary;

// Inside the router construction function/block, add:
.route("/api/v2/sbom/:id/advisory-summary", get(get_severity_summary))
```

### Full context of the change

The existing file likely looks like:

```rust
mod list;
mod get;

use axum::{routing::get, Router};
// ... other imports ...

pub fn router() -> Router<AppState> {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
}
```

After modification:

```rust
mod list;
mod get;
mod severity_summary;

use axum::{routing::get, Router};
// ... other imports ...

pub fn router() -> Router<AppState> {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
        .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
}
```

## Design Notes

- **Route path**: The route is `/api/v2/sbom/:id/advisory-summary` (nested under SBOM) even though it is registered in the advisory module's router. This is because the endpoint returns advisory data scoped to a specific SBOM. The advisory module is the natural owner of the aggregation logic.
- **Axum path parameter syntax**: Uses `:id` (Axum's syntax) in the route definition, which corresponds to `Path<String>` extraction in the handler.
- **No changes to `server/main.rs`**: The task description confirms routes auto-mount via module registration, so no changes are needed there.
