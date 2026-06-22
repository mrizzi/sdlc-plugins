# File 1: `migration/src/lib.rs` (Modify)

## Purpose

Register the new migration module `m0002_drop_advisory_status` in the migration runner so it is executed as part of the migration sequence.

## Pre-Implementation Inspection

Before modifying this file:
1. Use `mcp__serena_backend__get_symbols_overview` on `migration/src/lib.rs` to see the current structure
2. Use `mcp__serena_backend__find_symbol` with `include_body=true` on the `migrations()` function to see how `m0001_initial` is registered
3. Understand the exact pattern for module declarations and the `vec![]` registration

## Changes

### 1. Add module declaration

Add a new `mod` statement for the migration module, placed after the existing `m0001_initial` declaration:

```rust
mod m0001_initial;
mod m0002_drop_advisory_status;  // <-- add this line
```

### 2. Register migration in `migrations()` function

Add the new migration to the `vec![]` returned by the `migrations()` function, after the `m0001_initial` entry:

```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),  // <-- add this line
    ]
}
```

## Rationale

The migration runner iterates over the vector returned by `migrations()` in order. The new migration must be appended after all existing migrations to ensure correct execution order. This follows the exact same pattern used by `m0001_initial`.
