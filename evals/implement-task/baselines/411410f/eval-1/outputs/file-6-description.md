# File 6: modules/fundamental/src/advisory/model/mod.rs

## Action: MODIFY

## Purpose
Register the new `severity_summary` model module so the `SeveritySummary` struct
is accessible from other modules.

## Sibling Reference
Follows the existing module declarations in the same file -- `pub mod summary;`
and `pub mod details;` are already declared here.

## Detailed Changes

Add the following line alongside the existing module declarations:

```rust
pub mod severity_summary;
```

Place it in alphabetical order with the existing declarations (after `pub mod details;`
and before or after `pub mod summary;`, depending on alphabetical position -- `severity_summary`
comes after `summary` alphabetically but this is a minor style choice).

## Notes
- This is a single-line addition.
- The `pub` visibility ensures `SeveritySummary` is accessible from the endpoint handler and service.
- The existing declarations (`pub mod summary;`, `pub mod details;`) confirm this is the correct pattern.
