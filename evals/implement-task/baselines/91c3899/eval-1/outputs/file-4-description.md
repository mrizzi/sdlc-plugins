# File 4: modules/fundamental/src/advisory/model/mod.rs

**Action**: MODIFY

## Purpose

Register the new `severity_summary` model module by adding a `pub mod` declaration, following the same pattern used for `summary` and `details` modules.

## Sibling Reference

The existing `mod.rs` already contains:
```rust
pub mod summary;
pub mod details;
```

Following this exact pattern for the new module.

## Detailed Changes

Add the following line after the existing module declarations:

```rust
pub mod severity_summary;
```

### Before (expected current state)

```rust
pub mod summary;
pub mod details;
```

### After

```rust
pub mod summary;
pub mod details;
pub mod severity_summary;
```

## Design Notes

- This is a one-line addition following the existing alphabetical or logical ordering of module declarations
- The `pub` visibility matches the sibling module declarations, making `SeveritySummary` accessible from outside the `model` module
- No other changes are needed in this file
