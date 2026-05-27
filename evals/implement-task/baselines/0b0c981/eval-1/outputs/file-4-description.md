# File 4: `modules/fundamental/src/advisory/model/mod.rs` (MODIFY)

## Purpose
Register the new `severity_summary` model module so it is accessible from the rest of the crate.

## Detailed Changes

Add a single line to the existing `mod.rs` file:

```rust
pub mod severity_summary;
```

This line should be added alongside the existing module declarations (e.g., next to `pub mod summary;` and `pub mod details;`), maintaining alphabetical order if the existing declarations follow that convention.

### Before (expected current state)
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

## Rationale
- Follows the existing pattern in `mod.rs` where each model submodule is registered with `pub mod`.
- Alphabetical ordering is maintained for consistency.
- This is the minimal change needed to make the new `SeveritySummary` struct importable from other modules.
