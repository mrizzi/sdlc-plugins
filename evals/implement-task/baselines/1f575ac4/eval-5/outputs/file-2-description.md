# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new migration module so it is discovered and executed by the SeaORM migration runner.

## Detailed Changes

### 1. Add module declaration

Add the module declaration for the new migration directory, placed after the existing m0001_initial declaration:

```rust
mod m0001_initial;
mod m0002_drop_advisory_status;  // <-- ADD THIS LINE
```

### 2. Register in migrations() function

Add the new migration to the `vec![]` returned by the `migrations()` function, following the existing pattern for `m0001_initial`:

```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),  // <-- ADD THIS LINE
    ]
}
```

## Pre-Modification Inspection

Before modifying this file, read `migration/src/lib.rs` to:
- Confirm the exact function signature and return type of `migrations()`
- Confirm the exact pattern used for boxing migration structs (e.g., `Box::new(...)` vs other patterns)
- Confirm the module declaration style and ordering
- Identify any other registrations or patterns that need to be followed

## Conventions Applied

- New migration is appended after existing migrations (chronological ordering)
- Same boxing pattern as existing entries
- Module declaration follows alphabetical/numerical ordering convention
