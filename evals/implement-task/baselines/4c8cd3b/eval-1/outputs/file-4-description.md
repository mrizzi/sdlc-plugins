# File 4: modules/fundamental/src/advisory/model/mod.rs

**Action:** MODIFY

## Purpose

Register the new `severity_summary` model module so the `SeveritySummary` struct is accessible from the rest of the crate.

## Detailed Changes

Add a single line to the existing `mod.rs` file to declare the new module:

```rust
// Existing lines (preserved):
pub mod summary;
pub mod details;

// Add this line:
pub mod severity_summary;
```

The new `pub mod severity_summary;` declaration is added after the existing module declarations, following the alphabetical or logical ordering used by sibling entries.

## Conventions Applied

- **Module registration pattern:** Each model struct lives in its own file and is registered via `pub mod <name>;` in the parent `mod.rs`, consistent with how `summary` and `details` are registered.
- **Naming:** Module name matches the file name (`severity_summary`), following snake_case convention.
