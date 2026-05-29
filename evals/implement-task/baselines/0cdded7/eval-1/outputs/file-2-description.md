# File 2: Modify `modules/fundamental/src/advisory/model/mod.rs`

## Action: MODIFY

## Purpose

Register the new `severity_summary` model module so it is accessible from the advisory model namespace.

## Detailed Changes

Add one line to the existing module declarations:

```rust
// Existing lines (not modified):
pub mod details;
pub mod summary;

// Add this line:
pub mod severity_summary;
```

The exact insertion point is after the existing `pub mod` declarations, following alphabetical ordering if that pattern is used, or at the end of the module list otherwise.

## Conventions Applied

- **Module registration pattern**: Each model file in the `model/` directory has a corresponding `pub mod` declaration in `mod.rs`, as observed in all sibling modules (`sbom/model/mod.rs`, `package/model/mod.rs`)
- **Public visibility**: `pub mod` ensures the struct is accessible from outside the model module
