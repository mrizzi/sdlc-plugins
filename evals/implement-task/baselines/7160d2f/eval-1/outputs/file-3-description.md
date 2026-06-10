# File 3: modules/fundamental/src/advisory/model/mod.rs

**Action**: MODIFY

**Purpose**: Register the new `severity_summary` model module so it is accessible from the `advisory::model` namespace.

## Detailed Changes

Add a single line to the existing `mod.rs` file:

```rust
pub mod severity_summary;
```

This follows the existing pattern in the file where `pub mod summary;` and `pub mod details;` are already declared. The new line would be added adjacent to the other `pub mod` declarations, maintaining alphabetical order or following the existing ordering convention (whichever is used in the file).

## Conventions Followed

- **Module registration pattern**: follows the same `pub mod <name>;` pattern used for `summary` and `details` in the same file.
- **Ordering**: would inspect the existing file to determine whether modules are listed alphabetically or in declaration order, and follow the same convention.
- **Scope**: minimal change -- single line addition.

## Serena Usage

Would use `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/mod.rs` to see existing module declarations, then use `mcp__serena_backend__insert_after_symbol` to add the new module declaration after the last existing `pub mod` statement.
