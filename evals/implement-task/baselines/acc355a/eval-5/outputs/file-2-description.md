# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new `m0002_drop_advisory_status` migration module in the migration list so it is executed as part of the migration pipeline.

## Pre-implementation Inspection

Before modifying this file, inspect:
- **`migration/src/lib.rs`** — Read the full file to understand:
  - How existing migration modules are imported (e.g., `mod m0001_initial;`)
  - The structure of the `migrations()` function and its return type
  - The pattern for adding entries to the `vec![]` (e.g., `Box::new(m0001_initial::Migration)`)
  - Any ordering conventions or comments about migration sequence

## Detailed Changes

### Change 1: Add module import

Add a new `mod` declaration for the migration module, placed after the existing migration module imports:

```rust
mod m0001_initial;
mod m0002_drop_advisory_status;  // ADD THIS LINE
```

The module declaration follows alphabetical/numerical ordering consistent with the migration naming convention (`m0001_`, `m0002_`, etc.).

### Change 2: Register migration in the migrations() function

Add the new migration to the `vec![]` returned by the `migrations()` function, after the existing `m0001_initial` entry:

```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),  // ADD THIS LINE
    ]
}
```

The new entry follows the exact same pattern as the existing entry: `Box::new(<module>::Migration)`.

## Conventions Applied

- Migration modules are declared in numerical order matching their `m{NNNN}_` prefix
- Each migration is registered as `Box::new(<module>::Migration)` in the `vec![]`
- The order in the `vec![]` determines execution order — `m0002` must come after `m0001`
