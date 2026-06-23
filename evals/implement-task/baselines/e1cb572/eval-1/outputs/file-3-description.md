# File 3: modules/fundamental/src/advisory/model/mod.rs

**Action:** MODIFY

## Purpose

Register the new `severity_summary` sub-module so the `SeveritySummary` struct is accessible from the `advisory::model` module.

## Detailed Changes

Add the following line alongside the existing `pub mod` declarations:

```rust
pub mod severity_summary;
```

### Before (expected current state):

```rust
pub mod summary;
pub mod details;
```

### After:

```rust
pub mod details;
pub mod severity_summary;
pub mod summary;
```

## Conventions Applied

- **Module registration:** Follows the existing pattern of `pub mod <name>;` declarations in `mod.rs` files
- **Alphabetical ordering:** Module declarations are sorted alphabetically, matching Rust convention (would verify against actual file ordering during implementation)
- **Minimal change:** Only one line added, keeping the modification scoped
