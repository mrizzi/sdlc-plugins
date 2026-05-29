# Changes Log

## Preserved (unchanged)

- **Repository Registry**: Existing `trustify-backend` row preserved with all original field values intact.
- **Jira Configuration**: All five fields preserved with their original values (Project key, Cloud ID, Feature issue type ID, Git Pull Request custom field, GitHub Issue custom field).
- **Code Intelligence**: Tool naming convention paragraph preserved. Existing `serena_backend` limitation entry about rust-analyzer indexing time preserved.
- **Document header**: Title and Documentation section preserved unchanged.

## Added

- **Repository Registry**: New row for `trustify-ui` (TypeScript frontend, Serena instance `serena_ui`, path `/home/user/trustify-ui`).
- **Code Intelligence > Limitations**: New entry for `serena_ui` noting no known limitations.

## Removed

- **Code Intelligence body text**: Removed two non-functional text blocks that were embedded between the tool naming convention paragraph and the Limitations subsection. These were not valid limitation entries and did not conform to the contract structure. The actual limitation entries under the `### Limitations` heading were preserved.

## Summary

This was an incremental update. One new Serena instance (`serena_ui`) was discovered via MCP tool scanning and added to the Repository Registry and Code Intelligence sections. All existing configuration entries were preserved without modification.
