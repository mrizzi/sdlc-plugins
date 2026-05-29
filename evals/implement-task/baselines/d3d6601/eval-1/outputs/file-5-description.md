# File 5: modules/fundamental/src/advisory/endpoints/mod.rs (MODIFY)

## Purpose

Register the new `/api/v2/sbom/{id}/advisory-summary` route in the advisory endpoints module.

## Detailed Changes

### 1. Add module declaration for the new endpoint file

```rust
mod severity_summary;
```

### 2. Add route registration

In the router builder function, add a new `.route()` call:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_advisory_summary))
```

This should be added alongside existing route registrations following the `Router::new().route("/path", get(handler))` pattern.

## Before (expected pattern)

```rust
mod get;
mod list;

// ... router setup
Router::new()
    .route("/api/v2/advisory", get(list::list_advisories))
    .route("/api/v2/advisory/:id", get(get::get_advisory))
```

## After

```rust
mod get;
mod list;
mod severity_summary;

// ... router setup
Router::new()
    .route("/api/v2/advisory", get(list::list_advisories))
    .route("/api/v2/advisory/:id", get(get::get_advisory))
    .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_advisory_summary))
```

## Conventions Applied

- **Route registration**: follows existing `Router::new().route(...)` pattern
- **Module declaration**: `mod severity_summary;` matching `mod get;` and `mod list;`
- **Path parameter syntax**: `:id` (Axum path param syntax) -- would verify against existing routes
- **Handler reference**: `module::function` pattern matching existing registrations

## Inspection Required

Before modifying, would:
1. `mcp__serena_backend__get_symbols_overview` on this file to see exact current structure
2. Verify the Axum path parameter syntax used (`:id` vs `{id}`)
3. Verify the router builder function signature and how routes are chained
4. Check if there are any middleware or layer configurations applied to routes

## Note on Route Path

The endpoint is under `/api/v2/sbom/{id}/advisory-summary` per the task description, which is nested under the SBOM namespace even though the handler lives in the advisory endpoints module. This is by design -- the endpoint provides advisory data scoped to a specific SBOM.
