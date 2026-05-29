# File 3: Modify `modules/fundamental/src/advisory/model/mod.rs`

## Purpose

Register the new `severity_summary` model module so it is accessible from the rest of the crate.

## Pre-Change Analysis

Before modifying, read this file to see the existing `pub mod` declarations (expected: `pub mod summary;` and `pub mod details;`).

## Detailed Changes

Add one line alongside the existing module declarations:

```rust
pub mod severity_summary;
```

This makes the `SeveritySummary` struct importable as `crate::advisory::model::severity_summary::SeveritySummary` from anywhere in the crate.
