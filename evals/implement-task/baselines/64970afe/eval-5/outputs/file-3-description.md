# File 3: Tests for the migration

## Action: WOULD WRITE / VERIFY

## Purpose

Implement the test requirements specified in the task:
1. Test that the migration runs successfully against a test database
2. Test that the rollback (down) re-adds the column
3. Verify that existing advisory queries still work after the column is dropped

## Pre-implementation inspection

Before writing tests, the following inspections would be performed:

1. **`tests/api/advisory.rs`** -- Read via `mcp__serena_backend__get_symbols_overview` to understand:
   - Existing test structure and naming conventions
   - Test setup patterns (database initialization, fixtures)
   - Assertion patterns (`assert_eq!` with `StatusCode`, body deserialization)
   - How test databases are provisioned and torn down

2. **`tests/Cargo.toml`** -- Check test dependencies for migration testing support (e.g., `sea-orm-migration` test utilities).

3. **Sibling test files** (`tests/api/sbom.rs`, `tests/api/search.rs`) -- Examine 2-3 sibling test files to discover test conventions:
   - Test naming: `test_<action>_<scenario>` pattern
   - Setup patterns: how test databases are configured
   - Assertion style: `assert_eq!(resp.status(), StatusCode::OK)` pattern

## Test implementation approach

Migration tests would likely be integrated into the existing test infrastructure rather than creating a separate test file, depending on how the project handles migration testing. Two approaches:

### Approach A: Migration-specific test (if migration test infrastructure exists)

```rust
/// Verifies that m0002_drop_advisory_status successfully drops the status column.
#[tokio::test]
async fn test_m0002_drop_advisory_status_up() {
    // Given a database with the status column present
    let db = setup_test_database().await;
    run_migrations_up_to(&db, "m0001_initial").await;

    // When running the m0002 migration
    let result = run_migration(&db, "m0002_drop_advisory_status").await;

    // Then the migration succeeds and the status column no longer exists
    assert!(result.is_ok());
    let columns = get_table_columns(&db, "advisory").await;
    assert!(!columns.contains(&"status".to_string()));
}

/// Verifies that m0002_drop_advisory_status rollback re-adds the status column as nullable.
#[tokio::test]
async fn test_m0002_drop_advisory_status_down() {
    // Given a database with m0002 applied (status column dropped)
    let db = setup_test_database().await;
    run_migrations_up_to(&db, "m0002_drop_advisory_status").await;

    // When rolling back the m0002 migration
    let result = rollback_migration(&db, "m0002_drop_advisory_status").await;

    // Then the status column is re-added as a nullable string
    assert!(result.is_ok());
    let columns = get_table_columns(&db, "advisory").await;
    assert!(columns.contains(&"status".to_string()));
    let col_info = get_column_info(&db, "advisory", "status").await;
    assert!(col_info.is_nullable);
    assert_eq!(col_info.data_type, "varchar");
}

/// Verifies that existing advisory queries work after the status column is dropped.
#[tokio::test]
async fn test_advisory_queries_after_status_drop() {
    // Given a database with all migrations applied (including m0002)
    let db = setup_test_database().await;
    run_all_migrations(&db).await;
    seed_test_advisories(&db).await;

    // When querying advisories through the service
    let advisories = AdvisoryService::list(&db, Default::default()).await;

    // Then queries succeed and return expected data
    assert!(advisories.is_ok());
    let results = advisories.unwrap();
    assert!(!results.items.is_empty());
}
```

### Approach B: Verification via existing integration tests

If the project runs all migrations as part of test database setup, the existing integration tests in `tests/api/advisory.rs` would implicitly verify that queries work after the migration. In this case, running `cargo test` would serve as the verification step.

## Test conventions followed

- Doc comments on every test function explaining what it verifies
- Given-When-Then section comments for non-trivial tests
- `assert_eq!` / `assert!` assertion style matching sibling tests
- `test_<action>_<scenario>` naming convention
- `#[tokio::test]` for async test functions (Rust async test convention)
- Value-based assertions (checking column names and properties, not just counts)
