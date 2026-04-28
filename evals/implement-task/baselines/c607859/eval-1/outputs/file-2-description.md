# File 2: modules/fundamental/src/advisory/endpoints/mod.rs

**Action**: MODIFY (register new route)

## Context

This file contains the route registration for the advisory module. Existing routes follow the pattern `Router::new().route("/path", get(handler))`. Currently registers routes for `GET /api/v2/advisory` (list) and `GET /api/v2/advisory/{id}` (get).

## Sibling Pattern Reference

Looking at `sbom/endpoints/mod.rs` and `package/endpoints/mod.rs`, route registration follows:
- Import the handler module with `mod <handler_name>;`
- Add `.route("/path", get(<handler_module>::<handler_fn>))` to the Router chain
- Route paths use kebab-case for multi-word segments

## Changes

1. Add module declaration for the new endpoint file:
```rust
mod severity_summary;
```

2. Add route registration to the existing Router chain:
```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

Note: The route path `/api/v2/sbom/{id}/advisory-summary` is registered in the advisory
module's endpoint registration because the feature is advisory-domain logic (aggregating
advisory severity). The path starts with `/api/v2/sbom/` because the query is scoped to
a specific SBOM, but the business logic and service method live in the advisory domain.

## Verification

After this change, the route tree will include:
- `GET /api/v2/advisory` -- list advisories (existing)
- `GET /api/v2/advisory/{id}` -- get advisory details (existing)
- `GET /api/v2/sbom/{id}/advisory-summary` -- severity summary (NEW)

The `server/src/main.rs` does not need modification because routes auto-mount via module registration.
