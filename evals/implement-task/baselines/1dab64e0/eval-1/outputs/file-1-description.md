# File 1: modules/fundamental/src/advisory/model/mod.rs (MODIFY)

## Purpose

Register the new `severity_summary` model submodule so the `SeveritySummary` struct is accessible to the rest of the crate.

## Pre-change Inspection

Before modifying, inspect the file using:
```
mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/model/mod.rs")
```

Expect to see existing module declarations:
```rust
pub mod summary;
pub mod details;
```

## Changes

Add a single line to declare the new submodule:

```rust
pub mod severity_summary;
```

This should be added after the existing `pub mod` declarations, maintaining alphabetical or logical ordering consistent with the existing declarations.

## Full Expected State After Change

```rust
pub mod details;
pub mod severity_summary;
pub mod summary;
```

(Exact ordering depends on existing convention -- alphabetical shown above.)

## Rationale

The Rust module system requires explicit `pub mod` declarations in the parent `mod.rs` for submodules to be compiled and accessible. Without this line, the new `severity_summary.rs` file would be ignored by the compiler.
