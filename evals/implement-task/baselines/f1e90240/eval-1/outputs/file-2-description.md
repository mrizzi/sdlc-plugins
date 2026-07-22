# File 2: modules/fundamental/src/advisory/endpoints/mod.rs

**Action**: Modify (existing file)
**Purpose**: Register the new severity summary route

## Pre-Implementation Inspection

Before modifying, would use Serena to inspect:
- `mcp__serena_backend__get_symbols_overview` on this file to see existing route registrations
- `mcp__serena_backend__find_symbol` on the route registration function with `include_body=true` to see the exact Router pattern
- Also inspect sibling endpoint `mod.rs` files:
  - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/sbom/endpoints/mod.rs`
  - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/package/endpoints/mod.rs`

## Changes

1. Add module declaration for the new endpoint file:
```rust
pub mod severity_summary;
```

2. Add the new route to the Router registration, following the existing pattern of `Router::new().route()`:
```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

## Key Patterns Followed

- Module declaration follows alphabetical ordering convention (if applicable from siblings)
- Route registration follows existing `Router::new().route("/path", get(handler))` pattern
- Handler function imported from its own module file (severity_summary.rs)
- Path parameter uses `:id` Axum syntax (or `{id}` if that's what siblings use -- would verify via code inspection)
