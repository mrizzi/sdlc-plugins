# File 2: modules/fundamental/src/advisory/model/mod.rs

**Action**: MODIFY

**Purpose**: Register the new `severity_summary` module so the `SeveritySummary` struct is accessible from within the advisory model.

## Detailed Changes

Add a `pub mod severity_summary;` declaration to the existing `mod.rs` file. This follows the pattern already present for `summary` and `details` modules.

### Before (existing content, representative)

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

### Conventions Applied

- **Alphabetical ordering**: module declarations are kept in alphabetical order (matching Rust convention and likely existing ordering: `details`, `severity_summary`, `summary`)
- **Public re-export**: `pub mod` makes the submodule publicly accessible, consistent with how `summary` and `details` are declared
