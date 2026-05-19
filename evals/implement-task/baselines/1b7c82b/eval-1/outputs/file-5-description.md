# File 5: modules/fundamental/src/advisory/endpoints/mod.rs

## Action: MODIFY

## Purpose

Register the new `GET /api/v2/sbom/{id}/advisory-summary` route by adding the `severity_summary` handler module and wiring it into the existing router.

## Detailed Changes

### Add Module Declaration

Add at the top of the file alongside existing module declarations:

```rust
pub mod severity_summary;
```

### Add Route Registration

Within the existing router builder (where other routes like `get.rs` and `list.rs` are registered), add the new route:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

### Placement

The new `.route(...)` call is added after the existing advisory route registrations, following the pattern of `Router::new().route("/path", get(handler))` chains observed in the sibling modules.

### Full Context of Change

The existing `mod.rs` likely has a structure similar to:

```rust
mod get;
mod list;
pub mod severity_summary;  // NEW

use axum::{routing::get, Router};

pub fn router() -> Router {
    Router::new()
        .route("/api/v2/advisory", get(list::list_advisories))
        .route("/api/v2/advisory/:id", get(get::get_advisory))
        .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))  // NEW
}
```

### Design Decisions

- **Route path**: Uses `/api/v2/sbom/{id}/advisory-summary` as specified in the task's API Changes section. The route is nested under the SBOM resource because the advisory summary is scoped to a specific SBOM.
- **Route registration location**: Registered in the advisory module's `endpoints/mod.rs` because the feature aggregates advisory data. Even though the URL is under `/sbom/`, the implementation logic belongs to the advisory domain.
- **No changes to `server/src/main.rs`**: Routes auto-mount via module registration, as confirmed by the task description.

### Conventions Applied

- Module declaration uses `pub mod` consistent with sibling module declarations
- Route registration follows `Router::new().route(...)` chain pattern
- Handler function reference uses `module::function` pattern
