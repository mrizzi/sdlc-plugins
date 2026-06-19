# File 2: Modify `migration/src/lib.rs`

## Action: MODIFY

## Purpose

Register the new `m0002_drop_advisory_status` migration module in the migration list so that SeaORM's migrator discovers and executes it.

## Detailed Changes

### Change 1: Add module declaration

Add a `mod` declaration for the new migration module alongside the existing one:

```rust
// Before:
mod m0001_initial;

// After:
mod m0001_initial;
mod m0002_drop_advisory_status;
```

### Change 2: Register migration in the `migrations()` function

Add the new migration to the `vec![]` returned by the `migrations()` function, following the existing pattern:

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

## Conventions Applied

- **Module registration pattern:** Follows the same pattern as `m0001_initial` -- declare the module at the top of the file, then add `Box::new(<module>::Migration)` to the migrations vec
- **Ordering:** The new migration is added after `m0001_initial` in the vec, maintaining chronological order
- **No other changes:** Only the module declaration and vec entry are added -- no other modifications to `lib.rs`

## Verification

After this change:
- `cargo build` should compile successfully with the new migration module
- The SeaORM migrator should discover both `m0001_initial` and `m0002_drop_advisory_status` migrations
- Running `cargo test` should pass if migration tests are present
