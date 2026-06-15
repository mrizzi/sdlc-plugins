# File 2: `migration/src/lib.rs` (MODIFY)

## Purpose

Register the new migration module `m0002_drop_advisory_status` in the migration list so SeaORM's migration runner discovers and executes it.

## Detailed Changes

### Change 1: Add module declaration

**Location:** At the top of the file, alongside the existing module declarations.

**Add** after the existing `mod m0001_initial;` line:

```rust
mod m0002_drop_advisory_status;
```

### Change 2: Register migration in the `migrations()` function

**Location:** Inside the `migrations()` function, within the `vec![]` macro.

**Add** the new migration entry after the existing `m0001_initial` entry, following the same pattern:

```rust
Box::new(m0002_drop_advisory_status::Migration),
```

### Example of the modified `migrations()` function

Before:
```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
    ]
}
```

After:
```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),
    ]
}
```

### Design Decisions

1. **Ordering:** The new migration is added after `m0001_initial` to maintain chronological ordering. Migrations are executed in the order they appear in the vector.
2. **Pattern matching:** The registration follows the exact same `Box::new(module::Migration)` pattern used by `m0001_initial`.
