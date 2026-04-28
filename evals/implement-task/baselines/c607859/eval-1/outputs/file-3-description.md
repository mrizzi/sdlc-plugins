# File 3: modules/fundamental/src/advisory/model/mod.rs

**Action**: MODIFY (add module declaration)

## Context

This file re-exports the model sub-modules for the advisory domain. Currently contains:
```rust
pub mod summary;
pub mod details;
```

## Sibling Pattern Reference

Looking at `sbom/model/mod.rs` and `package/model/mod.rs`, each model sub-module is declared with a `pub mod` statement in alphabetical order (convention inferred from the consistent module layout across domains).

## Changes

Add a single line to register the new severity_summary model module:

```rust
pub mod severity_summary;
```

This makes the `SeveritySummary` struct accessible as `crate::advisory::model::severity_summary::SeveritySummary` from other parts of the codebase.

## Final State

After modification:
```rust
pub mod details;
pub mod severity_summary;
pub mod summary;
```

(Maintaining alphabetical ordering consistent with Rust module conventions.)
