# File 5: modules/fundamental/src/advisory/model/mod.rs

## Action: MODIFY

## Purpose

Register the new `severity_summary` model module so that the `SeveritySummary` struct is accessible from `crate::advisory::model::severity_summary::SeveritySummary`.

## Sibling Reference

The existing `mod.rs` already registers `summary` and `details` modules with `pub mod` declarations:

```rust
pub mod summary;
pub mod details;
```

## Detailed Changes

Add the following line alongside the existing module declarations:

```rust
pub mod severity_summary;
```

### Full context of the change

Before:
```rust
pub mod summary;
pub mod details;
```

After:
```rust
pub mod summary;
pub mod details;
pub mod severity_summary;
```

## Design Notes

- Uses `pub mod` to make the module publicly accessible, consistent with the sibling `summary` and `details` modules.
- The module name `severity_summary` matches the file name `severity_summary.rs` per Rust module conventions.
