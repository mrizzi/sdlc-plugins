# File 2: `migration/src/lib.rs` (MODIFY)

## Purpose

Register the new `m0002_drop_advisory_status` migration module so that SeaORM's migration runner discovers and executes it.

## Detailed Changes

### Change 1: Add module declaration

Add a `mod` statement for the new migration module, following the pattern of the existing `m0001_initial` declaration.

**Before:**
```rust
mod m0001_initial;
```

**After:**
```rust
mod m0001_initial;
mod m0002_drop_advisory_status;
```

### Change 2: Register migration in the `migrations()` function

Add the new migration to the `vec![]` returned by the `migrations()` function. The new migration must come after `m0001_initial` to maintain execution order.

**Before:**
```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
    ]
}
```

**After:**
```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),
    ]
}
```

## Conventions Applied

- **Module declaration pattern:** Follows the same `mod m<NNNN>_<name>;` pattern used by `m0001_initial`.
- **Registration pattern:** Adds `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]` in `migrations()`, following the exact same pattern as the existing `m0001_initial` entry.
- **Ordering:** The new migration is appended after all existing migrations to ensure correct execution order (migrations run in the order they appear in the vector).

## Scope

Only two small additions to this file:
1. One new `mod` line
2. One new `Box::new(...)` entry in the migrations vector

No other changes to this file are needed.
