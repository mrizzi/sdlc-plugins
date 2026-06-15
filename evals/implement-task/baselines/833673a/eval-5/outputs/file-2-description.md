# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new `m0002_drop_advisory_status` migration module so that it is included
when migrations are run.

## Detailed Changes

### Change 1: Add module declaration

Add a new `mod` declaration for the migration module, after the existing `m0001_initial`
module declaration:

```rust
mod m0001_initial;
mod m0002_drop_advisory_status;  // <-- ADD THIS LINE
```

### Change 2: Register migration in the migrations() function

Add the new migration to the `vec![]` inside the `migrations()` function, following the
pattern of `m0001_initial`:

**Before:**
```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
    ]
}
```

**After:**
```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),  // <-- ADD THIS LINE
    ]
}
```

## Conventions Applied

- **Module declaration order:** Module declarations are listed in numerical order matching
  the migration prefix (`m0001_`, `m0002_`, etc.).
- **Registration order:** Migrations are added to the `vec![]` in chronological order,
  matching the module declaration order.
- **Boxing pattern:** Each migration is wrapped in `Box::new()` to satisfy the
  `Vec<Box<dyn MigrationTrait>>` return type, consistent with the existing `m0001_initial` entry.

## Verification

- Confirm the module declaration compiles (the `m0002_drop_advisory_status` directory
  and `mod.rs` must exist).
- Confirm the `migrations()` function returns both migrations in order.
- Run `cargo check` to verify compilation.
