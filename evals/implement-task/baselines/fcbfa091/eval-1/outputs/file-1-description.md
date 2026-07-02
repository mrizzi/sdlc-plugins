# File 1: modules/fundamental/src/advisory/model/mod.rs (MODIFY)

## Purpose

Register the new `severity_summary` sub-module so that the `SeveritySummary` struct is accessible to the service and endpoint layers.

## Current state (inspected via Serena)

The file currently declares modules for existing model types:

```rust
pub mod details;
pub mod summary;
```

These re-export `AdvisoryDetails` and `AdvisorySummary` respectively.

## Changes

Add a single line to register the new module:

```rust
pub mod details;
pub mod severity_summary;
pub mod summary;
```

The new `pub mod severity_summary;` line is inserted in alphabetical order among the existing module declarations, following the naming convention observed in sibling `mod.rs` files (e.g., `sbom/model/mod.rs` lists modules alphabetically).

## Rationale

Without this module declaration, `severity_summary.rs` would not be compiled or accessible from other parts of the crate. This is the standard Rust module registration pattern used throughout the codebase.

## Conventions applied

- Module declarations in alphabetical order (observed in sibling `mod.rs` files)
- `pub mod` for public visibility (matching `details` and `summary` declarations)
