# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new `m0002_drop_advisory_status` migration module in the migration library so it is discovered and executed by the SeaORM migration runner.

## Detailed Changes

### Change 1: Add module declaration

Add a `mod` statement to declare the new migration module, placed after the existing `m0001_initial` module declaration.

**Before:**
```rust
mod m0001_initial;
```

**After:**
```rust
mod m0001_initial;
mod m0002_drop_advisory_status;
```

### Change 2: Register the migration in the `migrations()` function

Add the new migration to the `vec![]` returned by the `migrations()` function, following the pattern of the existing `m0001_initial` entry.

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

### Conventions Followed

- Module declaration follows alphabetical/sequential ordering (m0001 before m0002)
- Migration registration in `vec![]` follows the same `Box::new(<module>::Migration)` pattern as the existing entry
- New migration is appended at the end of the vec (migrations must run in order)
- No other changes to `lib.rs` — keeping modifications scoped to what the task describes

### Verification

After this change, running the migration runner (e.g., `cargo run --bin migration`) would execute `m0002_drop_advisory_status` after `m0001_initial`, dropping the `status` column from the `advisory` table.
