# File 3: Test Implementation Plan

## Purpose

Implement tests as described in the Test Requirements section of the task.

## Pre-Implementation Inspection

Before writing tests, inspect sibling test files to understand test conventions:

1. **Read `tests/api/advisory.rs`** -- Understand existing advisory endpoint integration tests: assertion patterns, test setup, database fixture creation, and naming conventions.
2. **Read `tests/api/sbom.rs`** -- Additional sibling test file to confirm patterns are consistent across the test suite.

## Test Requirements from Task

1. Test that the migration runs successfully against a test database
2. Test that the rollback (down) re-adds the column
3. Verify that existing advisory queries still work after the column is dropped

## Detailed Test Plan

### Test Location

Tests would be added to the existing integration test infrastructure. Based on the repository structure, migration tests could be placed in either:
- `tests/api/advisory.rs` (if migration tests are co-located with endpoint tests)
- A new test file `tests/migration/m0002_drop_advisory_status.rs` (if migration tests have their own directory)

The choice depends on what sibling test analysis reveals about the project's test organization.

### Test 1: Migration runs successfully

```rust
/// Verifies that the m0002 migration successfully drops the status column from the advisory table.
#[tokio::test]
async fn test_m0002_migration_up() {
    // Given a test database with the initial schema (m0001 applied)
    let db = setup_test_database().await;

    // When applying the m0002 migration
    let result = Migrator::up(&db, Some(2)).await;

    // Then the migration should succeed
    assert!(result.is_ok());

    // And the status column should no longer exist on the advisory table
    let columns = get_table_columns(&db, "advisory").await;
    assert!(!columns.contains(&"status".to_string()));
}
```

### Test 2: Rollback re-adds the column

```rust
/// Verifies that rolling back m0002 re-adds the status column as a nullable string.
#[tokio::test]
async fn test_m0002_migration_down() {
    // Given a test database with m0002 applied (status column dropped)
    let db = setup_test_database().await;
    Migrator::up(&db, Some(2)).await.unwrap();

    // When rolling back the m0002 migration
    let result = Migrator::down(&db, Some(1)).await;

    // Then the rollback should succeed
    assert!(result.is_ok());

    // And the status column should exist again on the advisory table
    let columns = get_table_columns(&db, "advisory").await;
    assert!(columns.contains(&"status".to_string()));
}
```

### Test 3: Advisory queries work after migration

```rust
/// Verifies that existing advisory queries continue to work after the status column is dropped.
#[tokio::test]
async fn test_advisory_queries_after_m0002() {
    // Given a test database with m0002 applied and test advisory data
    let db = setup_test_database().await;
    Migrator::up(&db, None).await.unwrap();
    seed_test_advisories(&db).await;

    // When querying advisories through the service layer
    let advisories = AdvisoryService::list(&db, Default::default()).await;

    // Then the query should succeed and return results
    assert!(advisories.is_ok());
    let results = advisories.unwrap();
    assert!(!results.items.is_empty());
}
```

## Test Conventions Applied

Based on the repository structure and Key Conventions:
- **Framework**: Integration tests hit a real PostgreSQL test database
- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` pattern for endpoint tests; direct `assert!()` for migration success checks
- **Test naming**: `test_<subject>_<scenario>` pattern (e.g., `test_m0002_migration_up`)
- **Documentation**: Every test function has a `///` doc comment explaining what it verifies
- **Structure**: Given-When-Then section comments for non-trivial tests
- **Async**: Tests use `#[tokio::test]` for async database operations

## Acceptance Criteria Coverage

- [x] Test that the migration runs successfully against a test database
- [x] Test that the rollback (down) re-adds the column
- [x] Verify that existing advisory queries still work after the column is dropped
