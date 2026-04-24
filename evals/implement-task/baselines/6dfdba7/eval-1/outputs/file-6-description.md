# File 6: modules/fundamental/src/advisory/model/mod.rs

## Action: MODIFY

## Purpose

Register the new `severity_summary` model module so the `SeveritySummary` struct is accessible from other parts of the codebase.

## Conventions Applied

- Follows the existing pattern where each model sub-module is declared with `pub mod <name>;`.
- Existing declarations: `pub mod summary;` and `pub mod details;`.

## Detailed Changes

Add the following line alongside the existing module declarations:

```rust
pub mod severity_summary;
```

The full `mod.rs` would look like:

```rust
pub mod details;
pub mod summary;
pub mod severity_summary;
```

## Notes

- This is a single-line addition. The `pub` visibility modifier ensures the struct is accessible from the service and endpoint layers.
- The alphabetical ordering of module declarations follows Rust convention, but the exact position should match whatever ordering pattern the existing file uses (alphabetical or logical grouping).
