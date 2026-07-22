# File 3: modules/fundamental/src/advisory/model/mod.rs

**Action**: Modify (existing file)
**Purpose**: Register the new severity_summary model module

## Pre-Implementation Inspection

Before modifying, would use Serena to inspect:
- `mcp__serena_backend__get_symbols_overview` on this file to see existing module declarations
- Also inspect sibling model `mod.rs` files:
  - `modules/fundamental/src/sbom/model/mod.rs` -- see how summary.rs and details.rs are declared
  - `modules/fundamental/src/package/model/mod.rs` -- see module declaration pattern

## Changes

Add a single line to register the new model module:

```rust
pub mod severity_summary;
```

This line is added alongside the existing `pub mod summary;` and `pub mod details;` declarations.

## Key Patterns Followed

- Uses `pub mod` declaration matching existing pattern (summary, details modules are already declared this way)
- Module name matches the file name (`severity_summary.rs` -> `pub mod severity_summary;`)
- Placed in alphabetical order relative to existing module declarations (after `details`, before or after `summary` depending on existing ordering)
