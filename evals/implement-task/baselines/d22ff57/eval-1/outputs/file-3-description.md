# File 3: modules/fundamental/src/advisory/model/mod.rs

## Action: MODIFY

## Summary

Register the new `severity_summary` model module so the `SeveritySummary` struct is
accessible from the advisory model namespace.

## Detailed Changes

### Add module declaration

Add the following line alongside existing module declarations (`pub mod summary;`,
`pub mod details;`):

```rust
pub mod severity_summary;
```

This makes `crate::advisory::model::severity_summary::SeveritySummary` available for
import by the service and endpoint handlers.

## Conventions Applied

- **Module registration:** Follows the existing pattern where each model struct lives in its own file and is registered via `pub mod` in `model/mod.rs`.
- **Naming:** Module file name matches the struct concept (`severity_summary.rs` for `SeveritySummary`), consistent with `summary.rs` for `AdvisorySummary` and `details.rs` for `AdvisoryDetails`.
