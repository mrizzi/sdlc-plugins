# File 6: modules/fundamental/src/advisory/model/mod.rs

**Action**: MODIFY

## Purpose

Register the new `severity_summary` model module so the `SeveritySummary` struct is
accessible from the advisory model namespace.

## Detailed Changes

Add a `pub mod severity_summary;` declaration alongside the existing module declarations:

```rust
pub mod details;
pub mod summary;
pub mod severity_summary;  // NEW
```

## Conventions Applied

- **Module declaration pattern**: Uses `pub mod <name>;` to register sub-modules, matching the existing `pub mod summary;` and `pub mod details;` declarations.
- **Public visibility**: Uses `pub mod` so the struct is accessible from outside the model module (needed by the endpoint handler and service method).
- **File naming**: The module name `severity_summary` matches the file name `severity_summary.rs`, following Rust module conventions.

## Notes

- This is a minimal one-line change that makes the new model struct available through the module hierarchy.
- After this change, the struct is accessible as `crate::advisory::model::severity_summary::SeveritySummary` from within the fundamental module.
