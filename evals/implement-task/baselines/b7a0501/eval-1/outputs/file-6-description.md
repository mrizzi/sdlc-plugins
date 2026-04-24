# File 6: Modify `modules/fundamental/src/advisory/model/mod.rs`

## Action: MODIFY

## Purpose

Register the new `severity_summary` model module so that the `SeveritySummary` struct
is accessible from the advisory model namespace.

## Sibling Reference

- This file already contains `pub mod summary;` and `pub mod details;` declarations
  for the existing `AdvisorySummary` and `AdvisoryDetails` model structs.

## Detailed Changes

Add a single line to register the new module:

```rust
pub mod severity_summary;
```

This line should be placed alongside the existing `pub mod summary;` and `pub mod details;`
declarations, in alphabetical order or following the existing ordering convention.

## Full Context of Change

**Before:**
```rust
pub mod details;
pub mod summary;
```

**After:**
```rust
pub mod details;
pub mod severity_summary;
pub mod summary;
```

## Conventions Applied

- **Module declaration pattern**: `pub mod <name>;` matches the pattern used for existing
  model sub-modules (`summary`, `details`).
- **Visibility**: `pub` to make the struct accessible from the service and endpoint layers.
- **Ordering**: Alphabetical order (if the project follows that convention) -- `details`,
  `severity_summary`, `summary`.

## Notes

- This is the smallest change in the implementation -- a single line addition. But it is
  essential for the Rust module system to recognize the new `severity_summary.rs` file.
- Without this line, the `use crate::advisory::model::severity_summary::SeveritySummary`
  import in the service and endpoint files would fail to compile.
