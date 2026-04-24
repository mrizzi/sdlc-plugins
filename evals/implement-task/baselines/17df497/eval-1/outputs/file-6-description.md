# File 6: modules/fundamental/src/advisory/model/mod.rs

**Action:** MODIFY

## Purpose

Register the new `severity_summary` model module so that `SeveritySummary` is accessible from the advisory model namespace.

## Detailed Changes

### Add Module Declaration

Add the following line alongside existing module declarations (`pub mod summary;`, `pub mod details;`):

```rust
pub mod severity_summary;
```

### Before (Conceptual)

```rust
pub mod details;
pub mod summary;
```

### After (Conceptual)

```rust
pub mod details;
pub mod severity_summary;
pub mod summary;
```

### Design Notes

- The module declaration is placed in alphabetical order among siblings, following Rust convention for module listings.
- Using `pub mod` ensures the `SeveritySummary` struct is publicly accessible from `crate::advisory::model::severity_summary::SeveritySummary`.

### Conventions Applied

- **Module registration pattern**: `pub mod <name>;` matching existing entries in the same file
- **Alphabetical ordering**: placed between `details` and `summary` alphabetically
