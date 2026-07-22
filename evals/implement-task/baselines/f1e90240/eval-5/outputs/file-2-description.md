# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new `m0002_drop_advisory_status` migration module so that SeaORM's migration runner discovers and executes it.

## Detailed Changes

### Change 1: Add module declaration

Add a `mod` declaration for the new migration module alongside the existing `m0001_initial` declaration.

**Before:**
```rust
mod m0001_initial;
```

**After:**
```rust
mod m0001_initial;
mod m0002_drop_advisory_status;
```

### Change 2: Register migration in the `migrations()` function

Add the new migration to the `vec![]` returned by the `migrations()` function, following the same pattern used for `m0001_initial`.

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

### Key Design Decisions

1. **Ordering**: The new migration is appended after `m0001_initial` in the vec, maintaining chronological order. SeaORM executes migrations in the order they appear in this list.

2. **Module naming**: Uses the `m0002_` prefix with a descriptive suffix (`drop_advisory_status`), following the naming convention established by `m0001_initial`.

3. **Registration pattern**: Uses `Box::new(module::Migration)` to wrap the migration struct, matching the existing pattern for `m0001_initial`.

### Scope

This is a minimal, surgical change -- only two lines added (one `mod` declaration and one `vec!` entry). No other modifications to this file are needed.
