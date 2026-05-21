## Security Configuration

<!-- TODO: This section configures project-specific security triage settings.
     It is consumed by the triage-security skill and scaffolded by the setup skill.
     Run /setup to populate interactively, or fill in manually using the
     placeholders below. -->

### Product Lifecycle

<!-- TODO: Configure product lifecycle metadata.
     Required fields:
     - Product pages URL: the product lifecycle page for EOL/support status checks
     - Jira version prefix: filters Jira versions to this product (e.g., "MYPRODUCT")
     - Vulnerability issue type ID: the Jira issue type for Vulnerability issues
     - Component label pattern: the label prefix used by PSIRT on Vulnerability issues
       to identify the affected component (e.g., "pscomponent:")

     Optional fields:
     - VEX Justification custom field: the Jira custom field ID for VEX Justification
       on Vulnerability issues (e.g., "customfield_00000"). Used when closing
       not-affected issues to record the justification per VEX standard. This field
       cannot be auto-discovered via Jira metadata. To find it, inspect a closed
       Vulnerability issue that has it set and look for the custom field. Leave blank
       if your project does not use VEX Justification.

     Example:
       Product pages URL: https://lifecycle.example.com/products/myproduct
       Jira version prefix: MYPRODUCT
       Vulnerability issue type ID: 10001
       Component label pattern: pscomponent:
       VEX Justification custom field: customfield_00000 -->

- Product pages URL: {{product-pages-url}}
- Jira version prefix: {{jira-version-prefix}}
- Vulnerability issue type ID: {{vulnerability-issue-type-id}}
- Component label pattern: {{component-label-pattern}}
- VEX Justification custom field: {{vex-justification-field-id}}

### Version Streams

<!-- TODO: Add one row per version stream. Each stream maps to a Konflux release
     repo that contains a security-matrix.md file. The skill follows these entries
     to discover all supported versions.
     - Konflux Release Repo: the git repository URL (shared across users, used in
       security-matrix.md Forward Pointers)
     - Local Path: the user's local clone path (used by git show for lock file inspection)
     - Security Matrix Path: the path to security-matrix.md within the repo

     Example:
       | 2.1.x | git.downstream.example.com/my-org/product-release.0.3.z | /path/to/product-release.0.3.z | security-matrix.md |
       | 2.2.x | git.downstream.example.com/my-org/product-release.0.4.z | /path/to/product-release.0.4.z | security-matrix.md | -->

| Stream | Konflux Release Repo | Local Path | Security Matrix Path |
|---|---|---|---|
| {{stream-name}} | {{konflux-release-repo-url}} | {{local-path}} | {{security-matrix-path}} |

### Source Repositories

<!-- TODO: Add one row per source repository whose dependencies are tracked for CVEs.
     These repos are inspected via git show for lock file analysis.

     Example:
       | backend | https://github.com/my-org/backend |
       | frontend-ui | https://github.com/my-org/frontend-ui | -->

| Repository | URL |
|---|---|
| {{source-repo-name}} | {{source-repo-url}} |
