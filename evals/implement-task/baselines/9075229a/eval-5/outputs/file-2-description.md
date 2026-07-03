# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new `m0002_drop_advisory_status` migration module so it is executed by the migration runner.

## Detailed Changes

### Change 1: Add module declaration

Add a `mod` declaration for the new migration module alongside the existing one:

```rust
// BEFORE:
mod m0001_initial;

// AFTER:
mod m0001_initial;
mod m0002_drop_advisory_status;
```

### Change 2: Register migration in the migrations() function

Add the new migration to the `vec![]` returned by the `migrations()` function, after the existing `m0001_initial` entry:

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

### Key Points

- The new migration is added **after** `m0001_initial` to maintain chronological ordering
- The pattern matches exactly how `m0001_initial` is registered: `Box::new(<module>::Migration)`
- No other changes to `lib.rs` are needed
