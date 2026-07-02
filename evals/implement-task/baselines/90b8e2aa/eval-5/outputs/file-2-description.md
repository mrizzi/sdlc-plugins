# File 2: Modify `migration/src/lib.rs`

## Action: MODIFY

## Purpose

Register the new `m0002_drop_advisory_status` migration module so it is executed as part of the migration sequence.

## Detailed Changes

### Change 1: Add module declaration

**Location**: Near the top of the file, after the existing `mod m0001_initial;` declaration.

**Add**:
```rust
mod m0002_drop_advisory_status;
```

**Before**:
```rust
mod m0001_initial;
```

**After**:
```rust
mod m0001_initial;
mod m0002_drop_advisory_status;
```

### Change 2: Register migration in the `migrations()` function

**Location**: Inside the `migrations()` function, in the `vec![]` that lists all migrations.

**Add** a new entry after the existing `m0001_initial` entry:

**Before**:
```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
    ]
}
```

**After**:
```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),
    ]
}
```

### Design decisions

1. **Module ordering**: The new module declaration is placed immediately after `m0001_initial` to maintain sequential ordering by migration number.

2. **Vec ordering**: The new migration is appended at the end of the `vec![]` to ensure it runs after `m0001_initial`. Migration order is critical -- `m0002` must run after `m0001` since `m0001` created the table that `m0002` alters.

3. **No other changes**: The file requires no other modifications. The migration framework handles discovery and execution based on the `migrations()` return value.

### Conventions applied

- Follows the exact same `mod` declaration pattern as `m0001_initial`
- Follows the exact same `Box::new()` registration pattern in the migrations vec
- Maintains sequential ordering of modules and vec entries
