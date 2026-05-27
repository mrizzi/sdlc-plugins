# File 4: `modules/fundamental/src/advisory/model/mod.rs` (MODIFY)

## Purpose

Register the new `severity_summary` model submodule so it is accessible from the rest of the crate.

## Detailed Changes

### Current State (inferred from repository structure)

The file currently contains module declarations for existing model submodules:

```rust
pub mod summary;
pub mod details;
```

### Change

Add one line to register the new `severity_summary` module:

```rust
pub mod summary;
pub mod details;
pub mod severity_summary;
```

### What This Does

- Makes `SeveritySummary` accessible as `crate::advisory::model::severity_summary::SeveritySummary`
- Follows the established pattern of one `pub mod` line per model submodule
- The ordering places it after existing modules alphabetically or logically

## Conventions Applied

- One `pub mod` declaration per model file, matching the existing pattern in `model/mod.rs`
- Module name matches the file name (`severity_summary.rs` -> `pub mod severity_summary;`)
