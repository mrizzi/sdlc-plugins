# File 4: `modules/fundamental/src/advisory/model/mod.rs` (MODIFY)

## Purpose

Register the new `severity_summary` model submodule so it is accessible from the rest of the crate.

## Detailed Changes

Add one line to the existing `mod.rs` file:

```diff
 pub mod details;
 pub mod summary;
+pub mod severity_summary;
```

The new `pub mod severity_summary;` declaration follows the same pattern as the existing `pub mod summary;` and `pub mod details;` lines. This makes `SeveritySummary` importable as `crate::advisory::model::severity_summary::SeveritySummary`.

## Conventions Applied

- Follows the established pattern where each model struct gets its own file and is re-exported through `mod.rs`.
- Alphabetical or logical ordering consistent with sibling declarations.
