# File 6: modules/fundamental/src/advisory/model/mod.rs

## Action: MODIFY

## Purpose

Register the new `severity_summary` model module so the `SeveritySummary` struct is accessible from the advisory model namespace.

## Detailed Changes

Add a single line to declare the new module alongside existing module declarations:

```rust
// Existing:
pub mod details;
pub mod summary;

// Add:
pub mod severity_summary;
```

## Notes

- This is a one-line change following the exact pattern of existing `pub mod` declarations in this file.
- The `pub mod` visibility ensures the struct is accessible from the endpoint handler and service code via `crate::advisory::model::severity_summary::SeveritySummary`.

## Conventions Applied

- **Module registration**: Follows the existing `pub mod <name>;` pattern in the same file
- **Alphabetical ordering**: Would place the new declaration in alphabetical order relative to existing declarations (after `pub mod details;`, before or after `pub mod summary;` depending on project convention -- would check via Serena before implementing)
