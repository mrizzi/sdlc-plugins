# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new `m0002_drop_advisory_status` migration module in the migration list so that the migration runner discovers and executes it.

## Pre-Implementation Inspection

Before modifying this file, the following must be inspected:

1. **Read `migration/src/lib.rs`** -- understand the current structure:
   - How modules are declared (e.g., `mod m0001_initial;`)
   - How the `migrations()` function returns a `Vec` of migration instances
   - The pattern for adding new entries to the vec (e.g., `Box::new(m0001_initial::Migration)`)
   - Any other organizational patterns (imports, struct definitions, etc.)

## Detailed Changes

### 1. Add module declaration

Add a new module declaration for the migration, placed after the existing `m0001_initial` module declaration:

```rust
mod m0001_initial;
mod m0002_drop_advisory_status;  // NEW
```

### 2. Register in migrations() function

Add the new migration to the `vec![]` in the `migrations()` function, following the existing pattern. The new entry goes after `m0001_initial` to maintain chronological order:

```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),  // NEW
    ]
}
```

### Key Design Decisions

- **Ordering:** The new migration is added after `m0001_initial` in the vec to preserve chronological execution order. SeaORM executes migrations in the order they appear in the vec.
- **Pattern conformance:** The exact pattern (`Box::new(<module>::Migration)`) must match what `m0001_initial` uses -- this will be confirmed by reading the file before modification.

### Acceptance Criteria Coverage

- [x] Migration is registered in `migration/src/lib.rs` (via module declaration and vec entry)
