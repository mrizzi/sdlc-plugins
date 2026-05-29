# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new `m0002_drop_advisory_status` migration module so that SeaORM's
migration runner includes it when running migrations.

## Reference Files Inspected

- **`migration/src/lib.rs`** -- the current migration registry. Contains a `mod`
  declaration for `m0001_initial` and a `migrations()` function that returns a `Vec`
  of boxed migration instances. The new migration must be added in both places.

## Detailed Changes

### Change 1: Add module declaration

Add a new `mod` declaration for the migration module, following the existing pattern:

```rust
// Before:
mod m0001_initial;

// After:
mod m0001_initial;
mod m0002_drop_advisory_status;
```

This declares the new migration module so Rust can find it at compile time.

### Change 2: Register migration in the migrations() function

Add the new migration to the `vec![]` inside the `migrations()` function, following
the pattern of `m0001_initial`:

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

The new migration is appended after `m0001_initial` to ensure correct execution order
(migrations run in the order they appear in the vec).

### Key design decisions

1. **Ordering**: The new migration is placed after `m0001_initial` in both the `mod`
   declarations and the `vec![]`. Migration order matters -- `m0002` depends on the
   table created by `m0001`.

2. **Naming**: The module name `m0002_drop_advisory_status` follows the established
   numbering convention (`m0001_`, `m0002_`, ...) with a descriptive suffix.
