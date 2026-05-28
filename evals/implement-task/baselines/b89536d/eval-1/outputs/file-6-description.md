# File 6: modules/fundamental/src/advisory/model/mod.rs (MODIFY)

## Purpose

Register the new `severity_summary` model module so that the `SeveritySummary` struct
is accessible from other parts of the crate.

## Detailed Changes

Add the following line alongside existing module declarations (e.g., next to `pub mod summary;`
and `pub mod details;`):

```rust
pub mod severity_summary;
```

## Example of the change in context

Before:
```rust
pub mod details;
pub mod summary;
```

After:
```rust
pub mod details;
pub mod severity_summary;
pub mod summary;
```

(Alphabetical ordering maintained.)

## Conventions followed

- Uses `pub mod` to make the module publicly accessible (matches sibling declarations)
- Placed in alphabetical order among existing module declarations
- Single-line change, minimal diff
