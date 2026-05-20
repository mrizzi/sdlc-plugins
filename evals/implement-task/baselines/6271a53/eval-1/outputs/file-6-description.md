# File 6: `modules/fundamental/src/advisory/model/mod.rs` (MODIFY)

## Purpose

Register the new `severity_summary` model module so that the `SeveritySummary` struct is accessible from the advisory model namespace.

## Conventions Applied

- Follows the module registration pattern: each `mod.rs` declares sub-modules with `pub mod <name>;`
- Placement follows alphabetical ordering if the existing file maintains that convention

## Change Description

Add a single line to the existing `mod.rs` file:

### Before (existing content)

```rust
pub mod details;
pub mod summary;
```

### After (with addition)

```rust
pub mod details;
pub mod severity_summary;
pub mod summary;
```

## Diff

```diff
 pub mod details;
+pub mod severity_summary;
 pub mod summary;
```

## Design Decisions

1. **Alphabetical insertion**: The new module declaration is inserted alphabetically between `details` and `summary`, following Rust community conventions for module ordering. If the existing file does not use alphabetical order, the new line should be appended after the last existing `pub mod` declaration instead.
