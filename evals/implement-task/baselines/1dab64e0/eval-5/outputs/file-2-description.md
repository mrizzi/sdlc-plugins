# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new `m0002_drop_advisory_status` migration module so that SeaORM's migration runner discovers and executes it.

## Detailed Changes

### 1. Add module declaration

Add a `mod` declaration for the new migration module alongside the existing `m0001_initial`:

```rust
mod m0001_initial;
mod m0002_drop_advisory_status;  // ADD THIS LINE
```

### 2. Register in migrations() function

Add the new migration to the `vec![]` returned by the `migrations()` function, following the pattern of `m0001_initial`:

```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),  // ADD THIS LINE
    ]
}
```

### Key Implementation Decisions

1. **Ordering**: The new migration is added after `m0001_initial` in the vec, maintaining chronological order. SeaORM executes migrations in the order they appear in this list.

2. **Pattern conformance**: The registration follows the exact same pattern as `m0001_initial` -- `Box::new(<module>::Migration)` -- matching the established convention.

3. **Module declaration**: The `mod` statement is placed in alphabetical/numerical order after the existing module declarations, following Rust module organization conventions.
