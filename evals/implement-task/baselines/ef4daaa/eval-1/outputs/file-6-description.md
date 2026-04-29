# File 6: modules/fundamental/src/advisory/model/mod.rs

**Action**: MODIFY

## Purpose

Register the new `severity_summary` model module so that `SeveritySummary` is accessible from the advisory model namespace.

## Files inspected before writing

Before modifying this file, the following would be inspected:

- `modules/fundamental/src/advisory/model/mod.rs` -- PRIMARY: Read the full file to see existing `pub mod` declarations and any re-exports. Expected to contain `pub mod summary;` and `pub mod details;`.
- `modules/fundamental/src/sbom/model/mod.rs` -- SIBLING: to confirm the same pattern of `pub mod` declarations

## Conventions applied

- Module declaration: `pub mod severity_summary;` following the alphabetical or logical ordering used by existing declarations
- Re-export pattern: if existing modules use `pub use summary::AdvisorySummary;` style re-exports, add `pub use severity_summary::SeveritySummary;` for convenience

## Detailed changes

Add the new module declaration. Would use Edit to insert after the existing `pub mod` declarations:

```rust
// Existing declarations:
pub mod details;
pub mod summary;

// Add:
pub mod severity_summary;
```

If the existing `mod.rs` also re-exports the primary structs from sub-modules (e.g., `pub use summary::AdvisorySummary;`), add a corresponding re-export:

```rust
pub use severity_summary::SeveritySummary;
```

## Key design decisions

1. **Alphabetical ordering**: `severity_summary` is placed after `summary` alphabetically. If the existing file uses a different ordering convention (e.g., by creation date or logical grouping), the new entry would follow that convention instead.
2. **Re-export**: Adding a `pub use` re-export is conditional on whether sibling modules have them. If `mod.rs` only has `pub mod` declarations without re-exports, only the `pub mod` line is added.

## Integration points

- Makes `SeveritySummary` (file 1) importable as `crate::advisory::model::severity_summary::SeveritySummary` (or `crate::advisory::model::SeveritySummary` if re-exported)
- Used by the endpoint handler (file 2) and the service method (file 4) to import the response struct
