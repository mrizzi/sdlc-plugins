# File 2: `migration/src/lib.rs` (MODIFY)

## Purpose

Register the new `m0002_drop_advisory_status` migration module so that SeaORM's migrator knows to run it.

## Pre-implementation inspection

Read `migration/src/lib.rs` before modifying to understand:
- How `m0001_initial` is declared as a module
- How the `Migrator` struct and its `MigratorTrait` implementation are structured
- The exact syntax of the `migrations()` function and its `vec![]` contents
- The ordering convention (migrations should be listed in sequential order)

## Detailed Changes

### Change 1: Add module declaration

Add the new module declaration alongside the existing one:

```rust
// Before:
mod m0001_initial;

// After:
mod m0001_initial;
mod m0002_drop_advisory_status;
```

### Change 2: Register migration in the migrations list

Add the new migration to the `vec![]` in the `migrations()` function:

```rust
// Before:
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
    ]
}

// After:
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),
    ]
}
```

## Key Design Decisions

1. **Ordering**: The new migration is appended after `m0001_initial` to maintain sequential order. SeaORM executes migrations in the order they appear in this vector.

2. **Module declaration**: The `mod` statement is placed alphabetically/sequentially after `m0001_initial`, following the existing convention.

3. **No other changes**: The `Migrator` struct and `MigratorTrait` implementation remain unchanged. Only the module declaration and migration list entry are added.
