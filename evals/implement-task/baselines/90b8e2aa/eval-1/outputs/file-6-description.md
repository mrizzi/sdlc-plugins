# File 6: modules/fundamental/src/advisory/model/mod.rs (MODIFY)

## Purpose

Register the new `severity_summary` model module by adding a `pub mod severity_summary;` declaration to the model's `mod.rs`.

## Pre-implementation Inspection

Before modifying this file, inspect it:

1. **Read current content**: Use `mcp__serena_backend__get_symbols_overview` on this file, or Read it directly, to see existing module declarations (`pub mod summary;`, `pub mod details;`)
2. **Confirm pattern**: Verify that sibling modules are declared as `pub mod <name>;`

## Planned Changes

Add one line to the existing module declarations:

```rust
pub mod severity_summary;
```

This is placed alongside the existing `pub mod summary;` and `pub mod details;` declarations, maintaining alphabetical order or appending after the last existing declaration (whichever pattern the file currently uses).

## Design Decisions

- **`pub` visibility**: The module is public so that the endpoint handler can import `SeveritySummary` from the model module
- **Module name**: `severity_summary` matches the filename `severity_summary.rs`, following Rust module naming conventions

## Notes

- This is a minimal one-line change
- No other modifications needed in this file

## Conventions Applied

- `pub mod <name>;` pattern matching existing declarations in the same file
- Module name matches the filename
