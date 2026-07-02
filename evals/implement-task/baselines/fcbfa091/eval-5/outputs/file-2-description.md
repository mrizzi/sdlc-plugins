# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new `m0002_drop_advisory_status` migration module so that the migration runner discovers and executes it.

## Detailed Changes

### Change 1: Add module declaration

Add a new `mod` declaration for the migration module, placed after the existing `m0001_initial` module declaration:

```rust
mod m0001_initial;
mod m0002_drop_advisory_status;  // <-- ADD THIS LINE
```

This follows the convention of declaring migration modules in sequence order at the top of `lib.rs`.

### Change 2: Register migration in the migrations vec

In the `migrations()` function, add the new migration to the `vec![]` after the existing `m0001_initial` entry:

```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),  // <-- ADD THIS LINE
    ]
}
```

The new entry is added at the end of the vec to ensure it runs after `m0001_initial` (which created the table and the column that is now being dropped). Migration ordering matters -- `m0002` depends on the `advisory` table and `status` column existing, which `m0001` creates.

## Conventions Applied

- Module declarations in sequence order matching the directory naming (`m0001_...`, `m0002_...`)
- Registration via `Box::new(<module>::Migration)` pattern matching the existing entry
- Trailing comma after the last vec entry (Rust formatting convention)
- No other changes to `lib.rs` -- scope is limited to registration only
