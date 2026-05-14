# File 6: modules/fundamental/src/advisory/model/mod.rs

**Action**: MODIFY

## Purpose

Register the new `severity_summary` model module so it is accessible from the rest of the crate.

## Detailed Changes

Add a single line to the existing `mod.rs` file:

```diff
 pub mod summary;
 pub mod details;
+pub mod severity_summary;
```

The `pub mod severity_summary;` declaration should be placed alphabetically or at the end of the existing module declarations, following the file's current ordering convention.

## Conventions Applied

- **Module registration pattern**: Every `.rs` file in the `model/` directory has a corresponding `pub mod <name>;` line in `model/mod.rs`. This is consistent across all domain modules (`sbom/model/mod.rs`, `advisory/model/mod.rs`, `package/model/mod.rs`).
- **Visibility**: Uses `pub mod` to make the struct importable from outside the module, matching sibling declarations.

## Minimal Change

This is a single-line addition. No other changes to this file are needed.
