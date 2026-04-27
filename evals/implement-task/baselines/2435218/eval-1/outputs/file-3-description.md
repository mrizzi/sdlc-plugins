# File 3 -- Modify: `modules/fundamental/src/advisory/model/mod.rs`

## Purpose

Register the new `severity_summary` model sub-module so that `SeveritySummary`
is accessible from the advisory model namespace.

## Pre-Implementation Inspection

Before modifying, read this file to see the existing module declarations. Expected
to find:

```rust
pub mod summary;
pub mod details;
```

## Changes

### Add module declaration

Add `pub mod severity_summary;` alongside the existing model module declarations:

```rust
pub mod details;
pub mod severity_summary;
pub mod summary;
```

This is a single-line addition. The ordering should be alphabetical to match
Rust conventions (details, severity_summary, summary), or match the existing
order if the file does not use alphabetical ordering.

## Conventions Applied

- Module declarations in `mod.rs` use `pub mod <name>;` format.
- New modules are registered in the parent `mod.rs` to be accessible within the crate.
