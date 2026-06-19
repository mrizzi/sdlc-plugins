# File 3: modules/fundamental/src/advisory/model/mod.rs (MODIFY)

## Purpose

Register the new `severity_summary` model module so it is accessible from the advisory module.

## Detailed Changes

### Inspect before modifying

- Read `modules/fundamental/src/advisory/model/mod.rs` to see existing `pub mod` declarations (should have `pub mod summary;` and `pub mod details;`)

### Change

Add a new `pub mod` declaration for the severity_summary module, following the existing pattern:

```rust
// Existing:
pub mod details;
pub mod summary;

// Add:
pub mod severity_summary;
```

### Notes

- Place the new `pub mod severity_summary;` in alphabetical order with existing declarations, following the convention observed in the file
- This is a single-line addition — no other changes to this file
