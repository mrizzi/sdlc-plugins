# File 4: modules/fundamental/src/advisory/model/mod.rs

**Action**: MODIFY

## Purpose

Register the new `severity_summary` model module so that the `SeveritySummary` struct is accessible from the advisory model namespace.

## Conventions Applied

- **Module registration**: Follows the existing pattern of `pub mod <name>;` declarations in `mod.rs` files
- **Sibling references**: `summary` and `details` modules are already registered here; `severity_summary` follows the same pattern

## Current State (expected)

```rust
pub mod summary;
pub mod details;
```

## Change Description

Add a single line to register the new `severity_summary` module:

```rust
pub mod summary;
pub mod details;
pub mod severity_summary;
```

## Scope

This is a minimal, single-line addition. No existing code is modified or removed. The change is explicitly listed in the task's "Files to Modify" section.
