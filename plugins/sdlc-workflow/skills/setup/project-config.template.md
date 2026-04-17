# Project Configuration

## Repository Registry

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| {{repository-name}} | {{language}} {{purpose}} | {{serena-instance-name}} | {{absolute-path}} |

## Jira Configuration

- Project key: {{project-key}}  # Your Jira project key (e.g., TC, PROJ)
- Cloud ID: {{cloud-id}}  # Jira cloud instance ID (from get_user_info)
- Feature issue type ID: {{feature-issue-type-id}}  # Discovered via get_project_metadata
- Git Pull Request custom field: {{custom-field-id}}  # Optional - from get_project_metadata
- GitHub Issue custom field: {{custom-field-id}}  # Optional - from get_project_metadata

## Code Intelligence

Tools are prefixed by Serena instance name: `mcp__<instance>__<tool>`.

For example, to search for a symbol in a repository whose Serena instance
is `{{serena-instance-name}}`:

    mcp__{{serena-instance-name}}__find_symbol(
      name_path_pattern="MyService",
      substring_matching=true,
      include_body=false
    )

### Limitations

- `{{serena-instance-name}}`: {{limitation-description}}
