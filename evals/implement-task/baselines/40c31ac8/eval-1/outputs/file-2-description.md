# File 2: modules/fundamental/src/advisory/model/mod.rs

**Action**: MODIFY

## Purpose

Register the new `severity_summary` model module so it is accessible from other parts of the codebase.

## Sibling Reference

The existing `mod.rs` already contains:
```rust
pub mod summary;
pub mod details;
```

## Detailed Changes

Add one line to register the new module:

```rust
pub mod severity_summary;
```

This line is added alongside the existing `pub mod summary;` and `pub mod details;` declarations, maintaining alphabetical ordering if that is the existing convention, or appended at the end of the module declarations.

## Convention Conformance

- Follows the same `pub mod <name>;` pattern used for `summary` and `details`
- Module name matches the file name (`severity_summary.rs`)
- Maintains the existing ordering convention of module declarations
