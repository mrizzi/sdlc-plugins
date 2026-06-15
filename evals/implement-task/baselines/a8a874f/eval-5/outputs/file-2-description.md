# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new `m0002_drop_advisory_status` migration module in the migration list so that SeaORM's migration runner discovers and executes it.

## Current State (Expected)

The file currently contains:
- A `mod m0001_initial;` declaration
- A `migrations()` function that returns a `Vec<Box<dyn MigrationTrait>>` containing `m0001_initial::Migration`

Example of expected current structure:

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

Add a new `mod` declaration for the migration module, placed after the existing `m0001_initial` declaration to maintain alphabetical/numerical order:

```rust
mod m0001_initial;
mod m0002_drop_advisory_status;
```

### Change 2: Register migration in the migrations vector

Add the new migration to the `vec![]` returned by the `migrations()` function, following the same `Box::new(...)` pattern used for `m0001_initial`:

```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),
    ]
}
```

The new migration is added **after** `m0001_initial` to maintain chronological execution order. Migrations run in the order they appear in this vector, and `m0002` must run after `m0001`.

## Convention Conformance

- Module declaration follows the same pattern as existing `mod m0001_initial;`
- Registration in the `vec![]` follows the same `Box::new(<module>::Migration)` pattern
- Ordering is chronological (m0001 before m0002)
- No other changes to this file -- the modification is minimal and scoped

## Verification

After modification, verify:
1. `cargo check` passes (module resolves correctly)
2. The migration vector contains both migrations in order
3. No other code in `lib.rs` is affected
