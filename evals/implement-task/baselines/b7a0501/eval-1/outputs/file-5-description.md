# File 5: Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

## Action: MODIFY

## Purpose

Register the new `GET /api/v2/sbom/{id}/advisory-summary` route by adding it to the
advisory module's route configuration.

## Sibling Reference

- This file already registers routes for `GET /api/v2/advisory` (list) and
  `GET /api/v2/advisory/{id}` (get).
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- registers SBOM routes similarly.
- Pattern: `Router::new().route("/path", get(handler))` chained together.

## Detailed Changes

### 1. Add module declaration for the new endpoint file

```rust
mod severity_summary;
```

### 2. Add the route registration

In the router builder function (the function that constructs and returns the `Router`
for advisory endpoints), add a new `.route()` call:

```rust
.route(
    "/api/v2/sbom/:id/advisory-summary",
    get(severity_summary::get_severity_summary),
)
```

This follows the existing pattern of chaining `.route()` calls on the `Router::new()` builder.

## Full Context of Change

The modification is minimal -- two additions to the existing file:

1. A `mod severity_summary;` declaration alongside existing `mod list;` and `mod get;`.
2. A `.route(...)` call in the router builder function, alongside existing route registrations.

## Conventions Applied

- **Module declaration**: `mod severity_summary;` follows the pattern of existing `mod list;`
  and `mod get;` declarations.
- **Route registration**: `.route("/api/v2/sbom/:id/advisory-summary", get(handler))` follows
  the existing `Router::new().route(...)` chaining pattern.
- **Path parameter syntax**: Uses `:id` (Axum path parameter syntax) consistent with existing
  routes like `/api/v2/advisory/:id`.
- **HTTP method**: `get()` function import from Axum, matching sibling GET endpoint registrations.

## Notes

- The route path `/api/v2/sbom/:id/advisory-summary` is a cross-domain endpoint -- it's
  conceptually about SBOM data but implemented in the advisory module because it aggregates
  advisory data. This is consistent with the task description. The route registration may
  alternatively belong in the SBOM endpoints module if the project convention is to organize
  routes by the resource in the URL path. This would be clarified by inspecting the actual
  `endpoints/mod.rs` files via Serena.
- Auto-mounting: `server/src/main.rs` mounts all module routers automatically, so no changes
  needed there.
