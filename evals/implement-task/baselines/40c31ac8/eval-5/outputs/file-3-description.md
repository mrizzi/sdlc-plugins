# File 3: Tests for the migration

## Action: Would add tests (specific file location depends on project test infrastructure)

## Purpose

Verify that the migration runs successfully, the rollback works, and existing advisory queries are unaffected.

## Test Location

Tests would be added in the integration test suite. Based on the repo structure, migration tests could be placed in:
- `tests/api/advisory.rs` (extend existing advisory tests), or
- A new `tests/migration/` directory if migration tests are kept separate

The exact location would be determined by inspecting existing test infrastructure during Step 4. Given the repo structure shows `tests/api/` for integration tests, and migrations are infrastructure rather than API tests, would check if a migration test pattern already exists.

## Test Implementations

### Test 1: Migration up runs successfully

```rust
/// Verifies that the m0002 migration drops the `status` column from the `advisory` table.
#[tokio::test]
async fn test_m0002_drop_advisory_status_up() {
    // Given a test database with the initial schema (m0001 applied)
    let db = setup_test_database().await;

    // When running the m0002 migration
    let migration = m0002_drop_advisory_status::Migration;
    let manager = SchemaManager::new(&db);
    migration.up(&manager).await.expect("migration up should succeed");

    // Then the `status` column should no longer exist on the `advisory` table
    let result = db
        .query_one(Statement::from_string(
            DatabaseBackend::Postgres,
            "SELECT column_name FROM information_schema.columns WHERE table_name = 'advisory' AND column_name = 'status'".to_string(),
        ))
        .await
        .expect("query should succeed");
    assert!(result.is_none(), "status column should not exist after migration");
}
```

### Test 2: Migration down (rollback) re-adds the column

```rust
/// Verifies that the m0002 rollback re-adds the `status` column as a nullable string.
#[tokio::test]
async fn test_m0002_drop_advisory_status_down() {
    // Given a test database with m0002 applied (status column dropped)
    let db = setup_test_database().await;
    let migration = m0002_drop_advisory_status::Migration;
    let manager = SchemaManager::new(&db);
    migration.up(&manager).await.expect("migration up should succeed");

    // When rolling back the migration
    migration.down(&manager).await.expect("migration down should succeed");

    // Then the `status` column should exist again as a nullable string
    let result = db
        .query_one(Statement::from_string(
            DatabaseBackend::Postgres,
            "SELECT column_name, is_nullable, data_type FROM information_schema.columns WHERE table_name = 'advisory' AND column_name = 'status'".to_string(),
        ))
        .await
        .expect("query should succeed");
    let row = result.expect("status column should exist after rollback");
    let is_nullable: String = row.try_get("", "is_nullable").expect("should have is_nullable");
    let data_type: String = row.try_get("", "data_type").expect("should have data_type");
    assert_eq!(is_nullable, "YES", "status column should be nullable");
    assert_eq!(data_type, "character varying", "status column should be a string type");
}
```

### Test 3: Existing advisory queries work after migration

```rust
/// Verifies that existing advisory queries continue to work after the status column is dropped.
#[tokio::test]
async fn test_advisory_queries_work_after_m0002() {
    // Given a test database with m0002 applied and test data inserted
    let db = setup_test_database().await;
    let migration = m0002_drop_advisory_status::Migration;
    let manager = SchemaManager::new(&db);
    migration.up(&manager).await.expect("migration up should succeed");
    insert_test_advisory(&db).await;

    // When querying advisories using the standard service patterns
    let advisories = Advisory::find().all(&db).await.expect("query should succeed");

    // Then the query should return results without errors
    assert!(!advisories.is_empty(), "should return at least one advisory");
}
```

## Conventions Applied

- Test naming follows `test_<migration_name>_<scenario>` pattern
- Each test has a documentation comment explaining what it verifies
- Tests use given-when-then section comments for structure clarity
- Tests run against a real PostgreSQL test database (integration test pattern)
- Assertions verify specific values, not just counts
- Both success and rollback paths are covered
