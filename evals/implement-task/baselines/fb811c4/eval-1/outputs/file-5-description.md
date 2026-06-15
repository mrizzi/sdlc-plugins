# File 5: modules/fundamental/src/advisory/model/mod.rs (MODIFY)

## Purpose
Register the new `severity_summary` model module so that the `SeveritySummary` struct is accessible from other modules.

## Detailed Changes

### Add module declaration

Add the following line alongside existing module declarations (e.g., `pub mod summary;`, `pub mod details;`):

```rust
pub mod severity_summary;
```

## Conventions Applied
- **Module registration**: follows the existing pattern of `pub mod <name>;` declarations in `mod.rs` files
- **Naming**: module name matches the file name (`severity_summary.rs` -> `severity_summary`)
- **Position**: placed alongside existing model module declarations (`summary`, `details`)
