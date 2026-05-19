# File 6: modules/fundamental/src/advisory/model/mod.rs

## Action: MODIFY

## Purpose

Register the new `severity_summary` model module so that `SeveritySummary` is accessible from other modules (service, endpoints, tests).

## Detailed Changes

### Add Module Declaration

Add the following line alongside existing module declarations (`pub mod summary;`, `pub mod details;`):

```rust
pub mod severity_summary;
```

### Full Context of Change

The existing `mod.rs` likely has:

```rust
pub mod summary;
pub mod details;
pub mod severity_summary;  // NEW
```

### Design Decisions

- **`pub mod`**: The module is public so that the endpoint handler and service can import `SeveritySummary`. This matches the visibility pattern used by `summary` and `details` sibling modules.
- **Alphabetical or positional ordering**: Add the new module declaration after existing ones, maintaining the same ordering convention used in the file.

### Conventions Applied

- Module declaration follows the exact same pattern as sibling entries (`pub mod summary;`, `pub mod details;`)
- Minimal change -- single line addition
