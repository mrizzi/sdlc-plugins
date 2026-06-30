# File 6: `modules/fundamental/src/advisory/model/mod.rs` (MODIFY)

## Purpose

Register the new `severity_summary` model module so the `SeveritySummary` struct is accessible from the advisory model namespace.

## Detailed Changes

### Add module declaration

Add the following line alongside the existing `pub mod summary;` and `pub mod details;` declarations:

```rust
pub mod severity_summary;
```

### Full context of the change

The modified `mod.rs` would contain:

```rust
pub mod summary;
pub mod details;
pub mod severity_summary;
```

### Design decisions

- **Follows sibling convention**: The module declaration uses `pub mod` with the file name, matching the existing pattern for `summary` and `details` modules.
- **Public visibility**: The module is declared `pub` so that the `SeveritySummary` struct can be imported by the service and endpoint modules, consistent with how `AdvisorySummary` and `AdvisoryDetails` are exposed.
