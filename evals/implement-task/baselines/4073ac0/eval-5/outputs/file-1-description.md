# File 1: `migration/src/lib.rs` (Modify)

## Purpose

Register the new `m0002_drop_advisory_status` migration module so that SeaORM's migration runner includes it when applying migrations.

## Pre-inspection

Before modifying, inspect the file to understand:
- How `m0001_initial` is declared as a module (`mod m0001_initial;`)
- How the `migrations()` function is structured (returns a `Vec<Box<dyn MigrationTrait>>`)
- The exact pattern for adding a migration to the vector (e.g., `Box::new(m0001_initial::Migration)`)

## Changes

### 1. Add module declaration

Add a new `mod` statement for the migration module, placed after the existing `m0001_initial` declaration:

```rust
mod m0001_initial;
mod m0002_drop_advisory_status;  // <-- ADD THIS LINE
```

### 2. Register the migration in the `migrations()` function

Add the new migration to the `vec![]` returned by the `migrations()` function, after the `m0001_initial` entry. The ordering matters -- migrations are applied in the order they appear in the vector:

```rust
pub fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),  // <-- ADD THIS LINE
    ]
}
```

## Convention Compliance

- Follows the exact same registration pattern as `m0001_initial` (discovered from sibling analysis).
- Module is placed in sequential order after existing migrations.
- Uses `Box::new()` wrapping consistent with the existing pattern.
