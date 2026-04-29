# File 3: `modules/fundamental/src/advisory/model/mod.rs`

**Action**: Modify (register new model module)

## What Changes

Add a `pub mod severity_summary;` declaration to register the new model module so it is accessible from the rest of the crate.

## Detailed Changes

Alongside existing module declarations (e.g., `pub mod summary;`, `pub mod details;`), add:

```rust
pub mod severity_summary;
```

## Patterns Followed

- Same `pub mod` declaration pattern as `summary` and `details` modules
- Alphabetical or grouped ordering consistent with existing declarations
