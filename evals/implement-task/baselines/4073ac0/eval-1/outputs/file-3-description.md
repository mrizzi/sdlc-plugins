# File 3: modules/fundamental/src/advisory/model/mod.rs

**Action**: Modify (add module registration)

## Current State

This file registers model sub-modules for the advisory domain:
```rust
pub mod details;
pub mod summary;
```

## Changes

Add `pub mod severity_summary;` to register the new model module:

```rust
pub mod details;
pub mod severity_summary;  // NEW
pub mod summary;
```

The new entry is inserted in alphabetical order to maintain consistency with existing module declarations.

## Rationale

- Follows the existing pattern of `pub mod <name>;` declarations
- Alphabetical ordering matches Rust convention for module declarations
- This registration makes `SeveritySummary` importable as `crate::advisory::model::severity_summary::SeveritySummary`
