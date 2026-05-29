# File 2: modules/fundamental/src/advisory/model/mod.rs (MODIFY)

## Purpose

Register the new `severity_summary` model sub-module so it is accessible from the advisory model namespace.

## Detailed Changes

Add a single line to the existing module declarations:

```rust
pub mod severity_summary;
```

This line should be added alongside the existing `pub mod summary;` and `pub mod details;` declarations, maintaining alphabetical ordering if the existing modules are ordered that way.

## Before (expected current state)

```rust
pub mod details;
pub mod summary;
```

## After

```rust
pub mod details;
pub mod severity_summary;
pub mod summary;
```

## Conventions Applied

- **Module registration pattern**: matches existing `pub mod summary;` and `pub mod details;` declarations
- **Alphabetical ordering**: inserted between `details` and `summary` to maintain alphabetical order (if that is the existing convention; otherwise placed at the end)
- **Scope**: minimal change -- single line addition

## Inspection Required

Before modifying, would use `mcp__serena_backend__get_symbols_overview` on this file to confirm the exact current content and ordering of module declarations.
