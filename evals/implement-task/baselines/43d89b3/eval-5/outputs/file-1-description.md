# File 1: migration/src/lib.rs (Modify)

## Purpose

Register the new migration module `m0002_drop_advisory_status` in the application's migration list so that SeaORM's migration runner includes it when running migrations.

## Pre-implementation Inspection

Before modifying this file, use Serena (`mcp__serena_backend__get_symbols_overview`) to inspect:
- The existing module declarations (e.g., `mod m0001_initial;`)
- The `migrations()` function structure and how it returns a `Vec<Box<dyn MigrationTrait>>`
- The pattern used to register `m0001_initial` in the vector

## Changes

### 1. Add module declaration

Add a new module declaration for the migration, placed after the existing `m0001_initial` declaration:

```rust
mod m0001_initial;
mod m0002_drop_advisory_status;  // <-- ADD THIS LINE
```

### 2. Register migration in the `migrations()` function

Add the new migration to the `vec![]` returned by the `migrations()` function. Place it after the `m0001_initial` entry, following the same `Box::new(...)` pattern:

```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),  // <-- ADD THIS LINE
    ]
}
```

The ordering matters -- migrations must be listed in chronological order so they run sequentially. `m0002` comes after `m0001`.

## Conventions Followed

- Same `Box::new(<module>::Migration)` pattern as `m0001_initial`
- Module declared at the top of the file alongside other migration modules
- Chronological ordering in the migrations vector
