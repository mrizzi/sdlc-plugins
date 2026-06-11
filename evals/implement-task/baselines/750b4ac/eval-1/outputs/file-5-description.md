# File 5: `modules/fundamental/src/advisory/endpoints/mod.rs` (MODIFY)

## Purpose

Register the new severity summary route in the advisory endpoints module so it is
accessible via the HTTP API.

## Detailed Changes

### Add module declaration

Add a `mod` declaration for the new endpoint module:

```rust
mod severity_summary;
```

This should be placed alongside the existing `mod list;` and `mod get;` declarations.

### Add use import

Import the handler function from the new module:

```rust
use severity_summary::get_severity_summary;
```

### Register the route

Add the new route to the existing `Router` builder, following the pattern of existing
route registrations. Add this line within the `Router::new()` chain:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(get_severity_summary))
```

### Before (example of existing pattern):
```rust
mod get;
mod list;

use get::get_advisory;
use list::list_advisories;

pub fn router() -> Router<AppState> {
    Router::new()
        .route("/api/v2/advisory", get(list_advisories))
        .route("/api/v2/advisory/:id", get(get_advisory))
}
```

### After:
```rust
mod get;
mod list;
mod severity_summary;

use get::get_advisory;
use list::list_advisories;
use severity_summary::get_severity_summary;

pub fn router() -> Router<AppState> {
    Router::new()
        .route("/api/v2/advisory", get(list_advisories))
        .route("/api/v2/advisory/:id", get(get_advisory))
        .route("/api/v2/sbom/:id/advisory-summary", get(get_severity_summary))
}
```

**Note**: The exact route path format (`:id` vs `{id}`) and Router API would be confirmed
by reading the actual `endpoints/mod.rs` file. The API contract specifies
`/api/v2/sbom/{id}/advisory-summary` -- the Axum path parameter syntax may use `:id`
or `{id}` depending on the Axum version in use.

## Conventions Applied

- **Route registration**: follows the `Router::new().route()` chain pattern used by existing endpoints
- **Module declaration**: `mod severity_summary;` follows the existing `mod get;` / `mod list;` pattern
- **Import style**: `use severity_summary::get_severity_summary;` follows the existing import pattern
- **Route path**: placed under `/api/v2/sbom/:id/advisory-summary` as specified in the API Changes section
