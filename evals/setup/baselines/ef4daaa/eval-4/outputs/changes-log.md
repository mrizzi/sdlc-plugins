# Changes Log

## Summary

Incremental update to Project Configuration. Existing entries preserved; new Serena instance added.

## Preserved (unchanged)

- **Repository Registry**: Existing entry for serena_backend preserved as-is (1 row)
- **Jira Configuration**: All fields preserved as-is (Project key, Cloud ID, Feature issue type ID, Git Pull Request custom field, GitHub Issue custom field)
- **Code Intelligence**: Existing tool naming convention text preserved as-is
- **Limitations**: Existing serena_backend limitation entries preserved as-is (2 entries)

## Added

- **Repository Registry**: New row for serena_ui instance
  - Repository: trustify-ui
  - Role: TypeScript frontend
  - Serena Instance: serena_ui
  - Path: /home/user/trustify-ui
- **Limitations**: New entry for serena_ui — "No known limitations"

## Not Modified

- No entries were removed or overwritten (idempotent behavior)
- No sanitization was performed on existing field values
- Documentation section above Project Configuration was not changed
