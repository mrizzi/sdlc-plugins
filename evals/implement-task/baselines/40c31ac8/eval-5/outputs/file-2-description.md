# File 2: Modify `migration/src/lib.rs`

## Action: MODIFY

## Purpose

Register the new `m0002_drop_advisory_status` migration module so it is executed by the SeaORM migrator.

## Changes

### Change 1: Add module declaration

**Location**: Near the top of the file, after the existing `mod m0001_initial;` declaration.

**Add**:
```rust
mod m0002_drop_advisory_status;
```

### Change 2: Register migration in the migrations vec

**Location**: Inside the `migrations()` method of the `MigratorTrait` implementation, within the `vec![]` macro.

**Before** (existing code):
```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
    ]
}
```

**After** (with new migration appended):
```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),
    ]
}
```

## Conventions Applied

- Module declaration follows alphabetical/chronological ordering (m0001 before m0002)
- Registration follows the same `Box::new(<module>::Migration)` pattern as existing entries
- New migration is appended at the end of the vec to maintain chronological execution order
- No other changes to the file -- scope is strictly limited to registration
