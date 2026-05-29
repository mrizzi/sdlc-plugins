# File 1: migration/src/lib.rs (Modify)

## Purpose

Register the new migration module `m0002_drop_advisory_status` in the migration registry so SeaORM discovers and runs it.

## Pre-Implementation Inspection

Before modifying this file, inspect it using Serena:

1. `mcp__serena_backend__get_symbols_overview` on `migration/src/lib.rs` to see current structure
2. `mcp__serena_backend__find_symbol` on the `migrations()` function with `include_body=true` to see how `m0001_initial` is registered

This tells us the exact pattern for module declaration and registration.

## Changes

### 1. Add module declaration

Add a new `mod` statement for the migration module, following the existing pattern:

```rust
// Existing:
mod m0001_initial;

// Add:
mod m0002_drop_advisory_status;
```

### 2. Register migration in `migrations()` function

Add the new migration to the `vec![]` returned by the `migrations()` function, following the pattern used for `m0001_initial`:

```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),  // Add this line
    ]
}
```

The new migration is appended after `m0001_initial` to maintain chronological ordering.

## Convention Adherence

- Module naming follows the `m<NNNN>_<descriptive_name>` pattern established by `m0001_initial`
- Registration follows the `Box::new(<module>::Migration)` pattern
- Ordering is sequential (m0002 after m0001)
