# File 3: `modules/fundamental/src/advisory/model/mod.rs` (MODIFY)

## Pre-modification inspection

Before modifying this file, inspect it using:
- Read the file directly (it is likely small) to see existing `pub mod` declarations.
- Confirm the existing declarations: `pub mod summary;` and `pub mod details;` should be present.

## Changes

### Add module declaration

Add a single line to register the new severity summary model module:

```rust
pub mod severity_summary;
```

This should be placed alongside the existing module declarations (`pub mod summary;`, `pub mod details;`), following the existing ordering convention (alphabetical or by addition order).

### Full expected content of mod.rs after change

```rust
pub mod details;
pub mod severity_summary;
pub mod summary;
```

(Sorted alphabetically, matching convention if that is the existing order.)

### Conventions followed

- **Module registration**: Matches the existing `pub mod summary;` and `pub mod details;` pattern exactly.
- **Ordering**: Alphabetical order (confirm against existing file -- if existing file uses a different order, follow that).

### Backward compatibility

No existing declarations are modified. This is a purely additive change that makes the new `severity_summary` module accessible from the parent module.
