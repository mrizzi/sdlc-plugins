# File 4: modules/fundamental/src/advisory/model/mod.rs

## Action: MODIFY

## Purpose
Register the new `severity_summary` model module so it is accessible to the service and endpoint layers.

## Detailed Changes

Add a single line to the existing module declarations:

```rust
// Existing lines (unchanged):
pub mod summary;
pub mod details;

// Add this line:
pub mod severity_summary;
```

The new `pub mod severity_summary;` line registers `severity_summary.rs` in the module tree, making `SeveritySummary` importable as `crate::advisory::model::severity_summary::SeveritySummary`.

## Conventions Applied
- **Module registration**: Follows the exact pattern of existing `pub mod summary;` and `pub mod details;` declarations in the same file.
- **Alphabetical or logical ordering**: Place after `details` to maintain consistency with the existing declaration order (which groups related models together).
