# File 6: Modify `modules/fundamental/src/advisory/model/mod.rs`

## Action: MODIFY

## Purpose

Register the new `severity_summary` model module so the `SeveritySummary` struct is accessible from other parts of the codebase.

## Detailed Changes

### Add Module Declaration

Add the following line to the existing module declarations in `model/mod.rs`:

```rust
pub mod severity_summary;
```

### Complete Change Context

The existing `mod.rs` likely contains:

```rust
pub mod summary;
pub mod details;
```

After modification:

```rust
pub mod summary;
pub mod details;
pub mod severity_summary;
```

### Placement

The new module declaration should be placed after the existing `pub mod` declarations, maintaining alphabetical or logical ordering (whichever the existing file uses). Based on sibling patterns, the existing modules appear in definition order rather than alphabetical, so appending at the end is appropriate.

## Conventions Applied

- **Module registration**: Uses `pub mod <name>;` pattern matching siblings (`pub mod summary;`, `pub mod details;`)
- **Public visibility**: `pub` ensures the struct is accessible from the service and endpoint layers
- **Naming**: Module name matches the file name (`severity_summary` matches `severity_summary.rs`)
