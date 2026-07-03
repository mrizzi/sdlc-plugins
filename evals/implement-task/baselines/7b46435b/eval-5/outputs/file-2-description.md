# File 2: Modify `migration/src/lib.rs`

## Action: MODIFY

## Purpose

Register the new `m0002_drop_advisory_status` migration module so that SeaORM's migration runner includes it when running migrations.

## Detailed Changes

### Change 1: Add module declaration

Add a `mod` declaration for the new migration module, following the existing `m0001_initial` declaration:

```rust
// Existing:
mod m0001_initial;

// Add after:
mod m0002_drop_advisory_status;
```

### Change 2: Register migration in the migrations vec

Add the new migration to the `vec![]` returned by the `migrations()` function, after the existing `m0001_initial` entry:

```rust
// Existing pattern (approximate):
pub fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        // Add this line:
        Box::new(m0002_drop_advisory_status::Migration),
    ]
}
```

The ordering is important -- migrations run sequentially in the order listed, so `m0002` must come after `m0001`.

## Conventions followed

- Module declaration follows alphabetical/numerical ordering of migration modules
- Registration uses `Box::new(module::Migration)` pattern matching existing entries
- Migration ordering in the vec matches the numerical prefix ordering (m0001 before m0002)

## Acceptance criteria addressed

- Migration is registered in `migration/src/lib.rs`
