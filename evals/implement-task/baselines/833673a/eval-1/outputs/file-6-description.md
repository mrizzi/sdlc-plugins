# File 6: modules/fundamental/src/advisory/model/mod.rs (MODIFY)

## Purpose

Register the new `severity_summary` model module so the `SeveritySummary` struct is accessible from within the advisory module and from external consumers (endpoints, service).

## Detailed Changes

### Change: Add public module declaration

**Location**: Alongside existing module declarations (`pub mod summary;`, `pub mod details;`).

**Add**:
```rust
pub mod severity_summary;
```

**Placement**: After the existing model module declarations, maintaining alphabetical or logical ordering consistent with existing declarations.

## Conventions Applied

- **Module registration**: Uses `pub mod <name>;` matching the pattern of existing `pub mod summary;` and `pub mod details;` declarations in the same file.
- **Public visibility**: Uses `pub` to allow the model to be imported from sibling modules (endpoints, service), matching the visibility pattern of sibling model modules.
