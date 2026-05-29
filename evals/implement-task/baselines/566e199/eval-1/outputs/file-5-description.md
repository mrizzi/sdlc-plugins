# File 5: modules/fundamental/src/advisory/model/mod.rs (MODIFY)

## Purpose
Register the new `severity_summary` model module so it is accessible to the rest of the crate.

## Detailed Changes

### Add module declaration

Add the following line alongside existing module declarations:

```rust
pub mod severity_summary;
```

This line should be placed alphabetically among the existing `pub mod` declarations (e.g., after `pub mod details;` and before or after `pub mod summary;` depending on alphabetical ordering in the existing file).

### Existing content (expected)

The file currently contains module declarations like:
```rust
pub mod details;
pub mod summary;
```

### After modification

```rust
pub mod details;
pub mod severity_summary;
pub mod summary;
```

### Conventions followed
- **Module declaration pattern**: `pub mod <name>;` matches the existing declarations for `summary` and `details`.
- **Alphabetical ordering**: if the existing file orders modules alphabetically, maintain that order. `severity_summary` sorts after `details` and before `summary`.
- **Public visibility**: `pub mod` makes the module accessible from outside the `model` module, consistent with siblings.
