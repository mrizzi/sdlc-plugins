# File 5: `modules/fundamental/src/advisory/endpoints/mod.rs` (MODIFY)

## Purpose

Register the new severity summary route so it is served by the Axum router.

## Detailed Changes

Two changes to the existing `mod.rs`:

### 1. Add module declaration

```diff
 mod get;
 mod list;
+mod severity_summary;
```

### 2. Add route registration

Within the `Router::new()` builder chain, add the new route:

```diff
 Router::new()
     .route("/api/v2/advisory", get(list::handler))
     .route("/api/v2/advisory/:id", get(get::handler))
+    .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::handler))
```

## Conventions Applied

- **Module declaration**: Follows the same `mod <name>;` pattern as `mod get;` and `mod list;`.
- **Route registration**: Uses the `Router::new().route(path, get(handler))` builder pattern established by sibling routes.
- **Path parameter**: Uses `:id` syntax for Axum path parameters, matching existing routes like `/api/v2/advisory/:id`.
- **Route path**: The endpoint path `/api/v2/sbom/:id/advisory-summary` is registered here in the advisory module's router because the business logic is advisory-related, even though the path is scoped under SBOMs. This is consistent with how the task specifies the route.
