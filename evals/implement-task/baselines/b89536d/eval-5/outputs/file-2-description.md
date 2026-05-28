# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new migration module `m0002_drop_advisory_status` in the migration runner so it is discovered and executed during database migration.

## Detailed Changes

### Change 1: Add module declaration

Add a `mod` declaration for the new migration module, following the existing `m0001_initial` declaration:

```rust
// Before:
mod m0001_initial;

// After:
mod m0001_initial;
mod m0002_drop_advisory_status;
```

### Change 2: Register migration in the migrations() function

Add the new migration to the `vec![]` returned by the `migrations()` function, after the existing `m0001_initial` entry:

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

## Conventions Followed

- Module declaration follows alphabetical/sequential ordering (m0001 before m0002)
- Registration in `migrations()` follows chronological order (m0001 before m0002), which is critical for migration execution order
- Uses the same `Box::new(<module>::Migration)` pattern as the existing entry
- No other changes to this file -- strictly scoped to registering the new migration
