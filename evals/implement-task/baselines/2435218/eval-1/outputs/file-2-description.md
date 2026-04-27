# File 2 -- Modify: `modules/fundamental/src/advisory/endpoints/mod.rs`

## Purpose

Register the new GET `/api/v2/sbom/{id}/advisory-summary` route in the advisory
module's route configuration.

## Pre-Implementation Inspection

Before modifying, inspect this file using Serena (`mcp__serena_backend__get_symbols_overview`)
to understand the existing route registration pattern. Specifically:
- Identify how `Router::new().route(...)` calls are structured.
- Confirm the import style for handler functions from sub-modules.
- Check whether routes are grouped or chained.

Also inspect `modules/fundamental/src/sbom/endpoints/mod.rs` as a sibling to confirm
the route registration pattern is consistent across modules.

## Changes

### Add module declaration

Add a `pub mod severity_summary;` declaration at the top of the file alongside the
existing `pub mod get;` and `pub mod list;` declarations:

```rust
pub mod get;
pub mod list;
pub mod severity_summary;
```

### Add route registration

In the router builder function (likely a `pub fn router()` or similar), add the new
route following the existing pattern:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::handler))
```

The exact path parameter syntax depends on the Axum version used (`:id` vs `{id}`).
Inspect the existing route definitions to match the correct syntax.

### Add import (if needed)

If handler functions are imported explicitly rather than referenced via module path,
add:

```rust
use severity_summary::handler as severity_summary_handler;
```

and reference it in the route registration accordingly.

## Conventions Applied

- Route registration follows `Router::new().route("/path", get(handler))` pattern.
- Handler is imported from its own sub-module file.
- Module declaration added alphabetically or in the same order as existing declarations.
