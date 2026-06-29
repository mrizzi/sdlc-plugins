# File 3: Modify `modules/fundamental/src/advisory/model/mod.rs`

## Purpose

Register the new `severity_summary` model sub-module so it is visible to the rest of the crate.

## Detailed Changes

### Add module declaration

Add a single line to the existing module declarations:

```rust
pub mod severity_summary;
```

This follows the existing pattern where each model sub-module (e.g., `summary`, `details`) is registered with a `pub mod` line in `mod.rs`.

## Convention Compliance

- **Module registration**: Matches the pattern used for existing sibling modules (`pub mod summary;`, `pub mod details;`)
- **Ordering**: Insert alphabetically among the existing module declarations, or at the end if no alphabetical ordering is observed in siblings
- **Scope**: Minimal change -- single line addition
