# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new `m0002_drop_advisory_status` migration module so it is discovered
and executed by the SeaORM migration runner.

## Detailed Changes

### Change 1: Add module declaration

Add a `mod` declaration for the new migration module alongside the existing one:

```rust
// Before:
mod m0001_initial;

// After:
mod m0001_initial;
mod m0002_drop_advisory_status;
```

### Change 2: Register migration in the `migrations()` function

Add the new migration to the `vec![]` returned by the `migrations()` function,
following the pattern of the existing `m0001_initial` entry:

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

### Key Design Decisions

1. **Ordering**: The new migration is appended after `m0001_initial` to maintain chronological ordering. SeaORM executes migrations in the order they appear in the vec.

2. **Pattern conformance**: The registration follows the exact same `Box::new(<module>::Migration)` pattern used by the existing migration, as specified in the Implementation Notes.

3. **No other changes**: No other modifications to `lib.rs` are needed -- the file's structure (imports, struct definitions, trait implementations) remains unchanged.
