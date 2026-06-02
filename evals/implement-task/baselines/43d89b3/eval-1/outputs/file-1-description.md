# File 1: modules/fundamental/src/advisory/model/mod.rs (MODIFY)

## Purpose
Register the new `severity_summary` model module so it is accessible from the rest of the crate.

## Current State (expected)
The file currently declares submodules for existing model types:
```rust
pub mod summary;
pub mod details;
```

## Changes
Add a single line to register the new module:
```rust
pub mod severity_summary;
```

This follows the existing pattern of one `pub mod` declaration per model submodule file.

## Detailed Diff
```diff
 pub mod summary;
 pub mod details;
+pub mod severity_summary;
```

## Conventions Applied
- Module registration pattern: one `pub mod` per submodule, matching sibling declarations.
