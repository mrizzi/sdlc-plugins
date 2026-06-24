# File 2: modules/fundamental/src/advisory/model/mod.rs (MODIFY)

## Purpose

Register the new `severity_summary` module so the `SeveritySummary` struct is accessible from the `advisory::model` namespace.

## Detailed Changes

Add one line to the existing module declarations:

```rust
pub mod severity_summary;
```

This follows the existing pattern where `mod.rs` re-exports submodules (e.g., `pub mod summary;` and `pub mod details;` are already present).

## Convention Conformance

- **Module registration**: Follows the exact pattern of existing `pub mod summary;` and `pub mod details;` declarations in this file.
- **Alphabetical ordering**: Insert after `pub mod details;` to maintain alphabetical order if that convention is followed, or at the end of the module list if ordering is by addition date. The actual position would be determined by reading the file in Step 4.
