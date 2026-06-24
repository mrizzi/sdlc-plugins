# File 2: MODIFY `migration/src/lib.rs`

## Purpose

Register the new migration module `m0002_drop_advisory_status` in the migration runner so it is discovered and executed during database migrations.

## Detailed Changes

### 1. Add module declaration

Add a new `mod` declaration for the migration module, following the existing pattern:

```rust
// Existing:
mod m0001_initial;

// Add:
mod m0002_drop_advisory_status;
```

The module declaration should be placed after `m0001_initial` to maintain chronological ordering of migrations.

### 2. Register in `migrations()` function

Add the new migration to the `vec![]` in the `migrations()` function, following the pattern of `m0001_initial`:

```rust
// Existing pattern (to be discovered from inspection):
fn migrations(&self) -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        // Add:
        Box::new(m0002_drop_advisory_status::Migration),
    ]
}
```

The new entry is appended at the end of the vector to ensure migrations run in chronological order.

### Pre-implementation Verification

Before modifying this file, the following would be verified:

- Use `mcp__serena_backend__get_symbols_overview` on `migration/src/lib.rs` to see the current structure
- Use `mcp__serena_backend__find_symbol` with `include_body=true` on the `migrations()` function to see the exact registration pattern
- Confirm the registration uses `Box::new(module::Migration)` syntax (as opposed to some other pattern)
- Confirm `m0001_initial` is the last entry currently (so the new one goes after it)

### Conventions Applied

- Module declarations are ordered chronologically (matching migration execution order)
- Registration entries in `vec![]` follow the same chronological order
- Each migration is boxed using `Box::new(module_name::Migration)`
- No other changes to `lib.rs` -- the modification is minimal and scoped
