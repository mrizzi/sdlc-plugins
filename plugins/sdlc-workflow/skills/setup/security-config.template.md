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
     - Upstream Affected Component custom field: the Jira custom field ID that stores
       the upstream library name on Vulnerability issues (e.g., "customfield_10632").
       Used by Step 4.3 for cross-CVE overlap detection. Leave blank to skip overlap
       detection.
     - PS Component custom field: the Jira custom field ID that stores the PS Component
       identifier on Vulnerability issues (e.g., "customfield_10669"). Used together
       with the Upstream Affected Component field for cross-CVE overlap filtering.
     - Stream custom field: the Jira custom field ID that stores the stream identifier
       on Vulnerability issues (e.g., "customfield_10832"). Used together with the
       Upstream Affected Component field for cross-CVE overlap filtering.

     Optional fields for security team notification:
     - ProdSec contact email: the email address of the Product Security contact for
       this project (e.g., "prodsec@example.com"). Used for informational reference
       in CVE triage notifications. Leave blank if your project does not have a
       dedicated security team.
     - ProdSec Jira account ID: the Jira account ID of the ProdSec contact (e.g.,
       "557058:abc123"). Used for @mentions in triage comments (Affects Versions
       corrections, cross-CVE overlap notifications). Leave blank to skip @mentions.

     Optional field for coordinated vulnerability disclosure:
     - Embargo policy URL: link to the organization's coordinated vulnerability
       disclosure or embargo policy (e.g., "https://example.com/security/embargo-policy").
       When configured and a CVE has Critical or Important severity, triage-security
       presents a warning gate before proceeding. Leave blank to skip the embargo check.

     Example:
       Product pages URL: https://lifecycle.example.com/products/myproduct
       Jira version prefix: MYPRODUCT
       Vulnerability issue type ID: 10001
       Component label pattern: pscomponent:
       VEX Justification custom field: customfield_00000
       Upstream Affected Component custom field: customfield_10632
       PS Component custom field: customfield_10669
       Stream custom field: customfield_10832
       Embargo policy URL: https://example.com/security/embargo-policy -->

- Product pages URL: {{product-pages-url}}
- Jira version prefix: {{jira-version-prefix}}
- Vulnerability issue type ID: {{vulnerability-issue-type-id}}
- Component label pattern: {{component-label-pattern}}
- VEX Justification custom field: {{vex-justification-field-id}}
- Upstream Affected Component custom field: {{upstream-affected-component-field-id}}
- PS Component custom field: {{ps-component-field-id}}
- Stream custom field: {{stream-field-id}}
- ProdSec contact email: {{prodsec-email}}
- ProdSec Jira account ID: {{prodsec-jira-account-id}}
- Embargo policy URL: {{embargo-policy-url}}

### Version Streams

<!-- TODO: Add one row per version stream. Each stream maps to a Konflux release
     repo and a local security-matrix.md file. The skill reads these entries to
     discover all supported versions.
     - Konflux Release Repo: the git repository URL (used by git show for lock file
       inspection and fallback matrix reads)
     - Local Path: the user's local clone path to the Konflux release repo
     - Security Matrix Path: the path to security-matrix.md relative to the project
       working directory

     Example:
       | 2.1.x | git.downstream.example.com/my-org/product-release.0.3.z | /path/to/product-release.0.3.z | docs/security-matrix-2.1.x.md |
       | 2.2.x | git.downstream.example.com/my-org/product-release.0.4.z | /path/to/product-release.0.4.z | docs/security-matrix-2.2.x.md | -->

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
