# File 3: modules/fundamental/src/advisory/model/mod.rs

## Change Type: Modify

## Purpose

Register the new `severity_summary` model sub-module so that the `SeveritySummary` struct is accessible from the advisory model module.

## Detailed Changes

### 1. Add module declaration

Add the following line alongside existing `pub mod` declarations (e.g., `pub mod summary;`, `pub mod details;`):

```rust
pub mod severity_summary;
```

This makes `SeveritySummary` accessible as `crate::advisory::model::severity_summary::SeveritySummary`.

## Conventions Applied

- Uses `pub mod` declaration consistent with existing entries (`pub mod summary;`, `pub mod details;`)
- Module name matches the file name (`severity_summary.rs` -> `severity_summary`)
- Placed alongside sibling module declarations in alphabetical or logical order
