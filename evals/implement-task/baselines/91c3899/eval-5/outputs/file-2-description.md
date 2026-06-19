# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new `m0002_drop_advisory_status` migration module in the migration runner so it is discovered and executed during database migrations.

## Current State (Before Changes)

The file currently:
1. Declares the `m0001_initial` module
2. Implements a `Migrator` struct with a `migrations()` function
3. The `migrations()` function returns a `vec![]` containing only `m0001_initial::Migration`

Expected current structure:

```rust
mod m0001_initial;

pub struct Migrator;

#[async_trait::async_trait]
impl MigratorTrait for Migrator {
    fn migrations() -> Vec<Box<dyn MigrationTrait>> {
        vec![
            Box::new(m0001_initial::Migration),
        ]
    }
}
```

## Changes

### Change 1: Add module declaration

Add a new module declaration for `m0002_drop_advisory_status` after the existing `m0001_initial` declaration:

```rust
mod m0001_initial;
mod m0002_drop_advisory_status;
```

### Change 2: Register migration in vec![]

Add the new migration to the `vec![]` in the `migrations()` function, after `m0001_initial::Migration`:

```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),
    ]
}
```

## Conventions Applied

- **Module ordering**: New module declaration is added in sequential order after existing modules (m0001 before m0002), following the chronological ordering convention
- **Registration ordering**: Migration is appended to the end of the `vec![]` to maintain execution order (migrations run in the order listed)
- **Pattern matching**: Uses the same `Box::new(<module>::Migration)` pattern as the existing entry
- **No other changes**: The modification is strictly scoped to adding the module declaration and registration -- no other lines in `lib.rs` are touched

## Verification

After this change:
- `cargo check` should compile without errors (the module exists and implements `MigrationTrait`)
- `cargo test` should run the migration against the test database
- The migration runner will discover and execute `m0002_drop_advisory_status` after `m0001_initial`
