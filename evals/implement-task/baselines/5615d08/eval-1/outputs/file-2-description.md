# File 2: `modules/fundamental/src/advisory/endpoints/mod.rs`

**Action**: Modify (register new route)

## What Changes

Add a route registration for the new severity summary endpoint. Import the handler module and register the GET route.

## Detailed Changes

### Add module declaration

At the top of the file, alongside existing module declarations (e.g., `mod list;`, `mod get;`), add:

```rust
mod severity_summary;
```

### Add route registration

In the `Router` builder chain where existing routes are registered (following the pattern of `Router::new().route("/path", get(handler))` registrations), add:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

## Patterns Followed

- Same route registration pattern as existing endpoints in the module
- Route path follows the RESTful `/api/v2/` prefix convention
- Uses `get()` method handler binding consistent with other GET endpoints
- Module declaration follows alphabetical or grouped ordering of existing declarations
