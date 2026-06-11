# File 2: `modules/fundamental/src/advisory/model/mod.rs` (MODIFY)

## Purpose

Register the new `severity_summary` model module so it is accessible from the
advisory model module tree.

## Detailed Changes

Add one line to the existing module declarations in `model/mod.rs`:

```rust
pub mod severity_summary;
```

This line should be added alongside the existing `pub mod summary;` and `pub mod details;`
declarations, in alphabetical order or at the end of the module list, following the
existing ordering convention.

### Before (existing):
```rust
pub mod details;
pub mod summary;
```

### After:
```rust
pub mod details;
pub mod severity_summary;
pub mod summary;
```

## Conventions Applied

- **Module registration**: follows the existing pattern where each model file is registered as `pub mod <name>;` in `model/mod.rs`
- **Alphabetical ordering**: inserted in alphabetical position between `details` and `summary`
- **Minimal change**: only one line added, keeping the modification scoped
