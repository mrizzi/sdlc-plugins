# File 6: modules/fundamental/src/advisory/model/mod.rs (MODIFY)

## Purpose

Register the new `severity_summary` model module so the `SeveritySummary` struct is accessible from the advisory module.

## Pre-Implementation Inspection

Before modifying, inspect this file using:
- Read the file to see the existing `pub mod` declarations (e.g., `pub mod summary;`, `pub mod details;`)
- Confirm the pattern for module registration in model directories

## Detailed Changes

### Add module declaration

Add the following line alongside the existing module declarations:

```rust
pub mod severity_summary;
```

This registers the new `severity_summary.rs` file as a public sub-module of `advisory::model`, making `SeveritySummary` accessible as `crate::advisory::model::severity_summary::SeveritySummary`.

### Existing file context (expected)

The file currently contains something like:

```rust
pub mod details;
pub mod summary;
```

After modification:

```rust
pub mod details;
pub mod severity_summary;
pub mod summary;
```

(Alphabetical ordering follows Rust convention for module declarations.)

### Design Decisions

- **Public visibility**: Uses `pub mod` to make the struct accessible from the service and endpoint modules, matching the pattern of `pub mod summary;` and `pub mod details;`.
- **Alphabetical ordering**: Placed alphabetically between existing module declarations, following Rust community convention.

### Convention Conformance

- Follows the exact same `pub mod <name>;` pattern as existing entries in the file.
- Matches the one-module-per-model-type pattern seen across all domain modules.
