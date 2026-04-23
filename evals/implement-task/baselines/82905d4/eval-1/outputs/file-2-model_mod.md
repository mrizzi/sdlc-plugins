# File 2: `modules/fundamental/src/advisory/model/mod.rs` (MODIFY)

## Purpose

Register the new `severity_summary` sub-module so the `SeveritySummary` struct is accessible from the model layer.

## Change

Add one line to the existing module declarations:

```rust
// Existing declarations (example):
pub mod details;
pub mod summary;

// ADD this line:
pub mod severity_summary;
```

## Placement

The new `pub mod severity_summary;` line should be inserted alphabetically among the existing module declarations, or immediately after `pub mod summary;` since they are related.

## Impact

This is a one-line addition. No existing code is modified. The new module becomes importable as `crate::advisory::model::severity_summary::SeveritySummary`.
