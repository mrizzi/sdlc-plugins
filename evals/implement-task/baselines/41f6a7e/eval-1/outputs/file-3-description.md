# File 3: modules/fundamental/src/advisory/model/mod.rs (MODIFY)

## Purpose

Register the new `severity_summary` model module so it is accessible from the advisory module.

## Detailed Changes

Add a `pub mod severity_summary;` declaration to the existing `mod.rs`, following the pattern of existing module registrations (`pub mod summary;`, `pub mod details;`).

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

## Conventions followed

- **Alphabetical ordering**: Module declarations are kept in alphabetical order (details, severity_summary, summary), matching Rust conventions
- **Pattern**: Follows the existing `pub mod <name>;` pattern for registering model submodules
- **Minimal change**: Only adds one line -- no other modifications to the file

## Notes

- The exact current contents of `mod.rs` would be verified via `mcp__serena_backend__get_symbols_overview` or Read before editing
- If the file has additional content (re-exports, use statements), the new line would be inserted in the appropriate position among existing `pub mod` declarations
