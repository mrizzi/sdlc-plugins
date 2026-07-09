# File 2: Modify `migration/src/lib.rs`

## Action: MODIFY

## Purpose

Register the new `m0002_drop_advisory_status` migration module in the migration library so it is discovered and executed by the migration runner.

## Pre-implementation inspection

Before modifying this file, the following inspections would be performed:

1. **`migration/src/lib.rs`** -- Read via `mcp__serena_backend__get_symbols_overview` and then `mcp__serena_backend__find_symbol` with `include_body=true` on the `migrations()` function to understand:
   - How `m0001_initial` is declared as a module (`mod m0001_initial;`)
   - The exact structure of the `migrations()` function
   - How migrations are collected in the `vec![]` (e.g., `Box::new(m0001_initial::Migration)`)
   - The trait or struct that `migrations()` belongs to (likely `MigratorTrait`)
   - Import statements at the top of the file

2. **Existing migration registration pattern** -- Confirm the exact syntax used for `m0001_initial` so the new entry matches precisely.

## Changes

### Change 1: Add module declaration

**Location**: Near the top of the file, after the existing `mod m0001_initial;` declaration.

**Before**:
```rust
mod m0001_initial;
```

**After**:
```rust
mod m0001_initial;
mod m0002_drop_advisory_status;
```

**Rationale**: Module declarations are listed in order. The new module follows the sequential numbering convention.

### Change 2: Register migration in the `migrations()` function

**Location**: Inside the `migrations()` function body, in the `vec![]` macro.

**Before**:
```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
    ]
}
```

**After**:
```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),
    ]
}
```

**Rationale**: Migrations are registered in sequential order in the `vec![]`. The new migration is appended after `m0001_initial`, following the same `Box::new(<module>::Migration)` pattern.

## Conventions followed

- Module declarations ordered sequentially by migration number
- Each migration entry uses `Box::new(<module>::Migration)` syntax
- Trailing comma after last entry in `vec![]` (Rust convention)
- No additional imports needed -- `MigrationTrait` is already imported
