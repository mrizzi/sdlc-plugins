# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new `m0002_drop_advisory_status` migration module so that SeaORM's migration runner discovers and executes it.

## Detailed Changes

### Change 1: Add module declaration

Add a `mod` declaration for the new migration module, alongside the existing one:

```rust
// Before:
mod m0001_initial;

// After:
mod m0001_initial;
mod m0002_drop_advisory_status;
```

### Change 2: Register migration in the migrations() function

Add the new migration to the `vec![]` returned by the `migrations()` function, following the pattern used for `m0001_initial`:

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

1. **Ordering**: The new migration is added after `m0001_initial` in the vec, preserving chronological ordering. Migrations run in the order they appear in this vector, so the initial schema must be created before columns can be dropped from it.

2. **Pattern adherence**: The registration follows exactly the same `Box::new(<module>::Migration)` pattern used by the existing migration entry, as specified in the Implementation Notes.

### Pre-modification Inspection

Before modifying this file, the following would be verified:
- Read the current contents of `migration/src/lib.rs` to understand the exact structure
- Confirm the `migrations()` function exists and uses the `vec![]` pattern
- Confirm `m0001_initial` is already registered to understand the exact registration syntax
- Check for any additional boilerplate (e.g., `Migrator` struct, trait implementations) that might need awareness
- Verify exact whitespace and formatting to match the existing code style
