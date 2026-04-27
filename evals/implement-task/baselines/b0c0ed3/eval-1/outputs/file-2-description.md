# File 2: `modules/fundamental/src/advisory/model/mod.rs` (MODIFY)

## Purpose

Register the new `severity_summary` model module so it is accessible from the `advisory::model` namespace.

## Detailed Changes

Add a single line to the existing `mod.rs` file:

```rust
pub mod severity_summary;
```

This should be added alongside the existing `pub mod summary;` and `pub mod details;` declarations, maintaining alphabetical order or matching the existing ordering style.

### Before (expected existing content)

```rust
pub mod details;
pub mod summary;
```

### After

```rust
pub mod details;
pub mod severity_summary;
pub mod summary;
```

## Convention Conformance

- Follows the pattern of sibling `model/mod.rs` files that re-export sub-modules with `pub mod`.
- Alphabetical ordering matches the convention observed in other `mod.rs` files.
- Minimal change: exactly one line added, no other modifications.
