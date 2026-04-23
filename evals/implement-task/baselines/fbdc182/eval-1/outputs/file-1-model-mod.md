# File 1 — Modify: `modules/fundamental/src/advisory/model/mod.rs`

## Purpose

Register the new `severity_summary` sub-module so it is accessible from the rest of the crate. This is the only change to this file.

## Inspection Step

Read `modules/fundamental/src/advisory/model/mod.rs` to see the existing `pub mod` declarations. Based on the directory tree, the file currently contains at minimum:

```rust
pub mod summary;
pub mod details;
```

(Pattern confirmed from sibling `modules/fundamental/src/sbom/model/mod.rs` which contains `pub mod summary;` and `pub mod details;`.)

## Change

Add one line to register the new module, following the existing alphabetical or declaration-order convention:

```rust
pub mod details;
pub mod severity_summary;   // <-- ADD THIS LINE
pub mod summary;
```

If the existing order is `summary` then `details` (declaration order, not alpha), insert after the last existing `pub mod` line:

```rust
pub mod summary;
pub mod details;
pub mod severity_summary;   // <-- ADD THIS LINE
```

## Why only this change

The task description explicitly lists this file only for registering the new module. No other changes are needed here — the struct itself lives in `severity_summary.rs`.
