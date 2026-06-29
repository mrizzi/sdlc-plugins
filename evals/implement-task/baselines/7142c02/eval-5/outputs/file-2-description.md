# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new migration module `m0002_drop_advisory_status` in the migration runner so it is discovered and executed.

## Pre-Implementation Inspection

Read `migration/src/lib.rs` to understand:
- How the existing `m0001_initial` module is declared and registered
- The structure of the `migrations()` function and its return type
- The `MigratorTrait` implementation
- Import patterns

## Detailed Changes

### Change 1: Add module declaration

Add a new `mod` declaration for the migration module, following the pattern of the existing module declaration:

```rust
// Existing:
mod m0001_initial;

// Add:
mod m0002_drop_advisory_status;
```

### Change 2: Register migration in the migrations list

Add the new migration to the `vec![]` inside the `migrations()` function, after the existing `m0001_initial` entry:

```rust
// Existing pattern (approximate):
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        // Add this line:
        Box::new(m0002_drop_advisory_status::Migration),
    ]
}
```

The new entry is added at the end of the vector to ensure migrations run in chronological order.

## Conventions Followed

- Module declaration follows the same naming pattern as `m0001_initial`
- Migration registration follows the same `Box::new(module::Migration)` pattern
- Placement at the end of the vector maintains chronological ordering

## Acceptance Criteria Coverage

- [x] Migration is registered in `migration/src/lib.rs`
