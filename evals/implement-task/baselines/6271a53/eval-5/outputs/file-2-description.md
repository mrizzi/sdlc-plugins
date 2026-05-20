# File 2: migration/src/lib.rs

## Action: MODIFY

## Purpose

Register the new `m0002_drop_advisory_status` migration module so that SeaORM's migrator discovers and executes it.

## Pre-implementation Inspection

Read `migration/src/lib.rs` to identify:
- Where module declarations are placed (e.g., `mod m0001_initial;`)
- The exact structure of the `migrations()` function and the `vec![]` that lists migration instances
- Whether migrations are `Box::new(...)` wrapped or use a different pattern
- The struct implementing `MigratorTrait` and any other boilerplate

## Detailed Changes

### Change 1: Add module declaration

Add a new module declaration for the migration, placed after the existing `m0001_initial` declaration:

```rust
// BEFORE:
mod m0001_initial;

// AFTER:
mod m0001_initial;
mod m0002_drop_advisory_status;
```

### Change 2: Register migration in the migrations() function

Add the new migration to the `vec![]` inside the `migrations()` function, appended after the existing entry:

```rust
// BEFORE:
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
    ]
}

// AFTER:
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),
    ]
}
```

## Notes

- The new migration must appear **after** `m0001_initial` in the vec since migrations run in order and the initial migration creates the `advisory` table that this migration alters.
- The exact syntax (trailing commas, `Box::new` wrapping, struct path) should be adapted to match whatever pattern is observed in the existing file during inspection.
