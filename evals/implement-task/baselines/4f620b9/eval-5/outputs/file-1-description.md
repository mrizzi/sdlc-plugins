# File 1: migration/src/lib.rs (Modify)

## Purpose

Register the new `m0002_drop_advisory_status` migration module in the migration registry so that SeaORM's migration runner discovers and executes it.

## Changes

### 1. Add module declaration

Add a new `mod` declaration for the migration module, following the existing pattern of `m0001_initial`:

```rust
mod m0001_initial;
mod m0002_drop_advisory_status;  // <-- ADD THIS LINE
```

### 2. Register in the migrations() function

Add the new migration to the `vec![]` returned by the `migrations()` function, appending it after `m0001_initial` to maintain chronological order:

```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),  // <-- ADD THIS LINE
    ]
}
```

## Conventions Followed

- Migration modules are declared at the top of `lib.rs` in chronological order.
- Each migration is boxed and added to the `vec![]` in the `migrations()` function.
- The pattern follows the existing `m0001_initial` registration exactly.

## Rationale

The migration runner iterates over the `migrations()` vector to apply pending migrations. Without this registration, the new migration file would exist but never be executed.
