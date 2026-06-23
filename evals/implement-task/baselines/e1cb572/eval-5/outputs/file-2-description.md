# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new migration module `m0002_drop_advisory_status` in the migration registry so SeaORM's migrator executes it.

## Detailed Changes

### Change 1: Add module declaration

Add a `mod` declaration for the new migration module alongside the existing one.

**Before:**
```rust
mod m0001_initial;
```

**After:**
```rust
mod m0001_initial;
mod m0002_drop_advisory_status;
```

### Change 2: Register migration in the migrations() function

Add the new migration to the `vec![]` returned by the `migrations()` function, following the existing pattern of `m0001_initial`.

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

### Key Decisions

1. **Order matters**: The new migration is added after `m0001_initial` in the vector, maintaining chronological order. SeaORM executes migrations in the order they appear in this vector.
2. **Follows existing pattern**: The registration uses `Box::new(<module>::Migration)` exactly as the existing entry does.
3. **Module declaration placement**: The `mod` declaration is placed immediately after the existing `mod m0001_initial;` line, maintaining alphabetical/chronological ordering.

### Conventions Applied

- **Module registration pattern**: Follows the exact pattern of the existing `m0001_initial` entry -- `Box::new(module::Migration)` added to the `vec![]`.
- **Import organization**: Module declarations are grouped together at the top of the file.
