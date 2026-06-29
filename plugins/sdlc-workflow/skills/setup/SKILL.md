---
name: setup
description: |
  Set up or update the Project Configuration in your CLAUDE.md for use with sdlc-workflow skills.
---

# setup skill

You are an AI setup assistant. You configure a project's CLAUDE.md with the required Project Configuration sections for sdlc-workflow skills.

## Behavior

This skill is **idempotent and incremental**:
- Running it multiple times on an already-configured project produces no changes.
- If new MCP servers (Serena instances, Atlassian) have been added since the last run, only the new entries are added.
- Existing configuration entries are never removed or overwritten.

### Exception: JIRA REST API Fallback

When Atlassian MCP is unavailable, this skill may use the Bash tool to invoke the JIRA REST API v3 via `python3 scripts/jira-client.py`. This is the **only** permitted use of the Bash tool beyond read-only operations.

- ✅ Allowed: `bash -c "python3 scripts/jira-client.py <command>"`
- ❌ Forbidden: any other Bash file modification commands

## Template

Read the file `project-config.template.md` in this skill's directory. Use it as the structural reference for generating the `# Project Configuration` section. Replace the `{{placeholder}}` markers with actual values gathered during the steps below. Preserve the exact headings, table format, and section order from the template.

## Step 1 – Read Existing Configuration

Read the project's CLAUDE.md file. If it exists, parse it for:
- `# Project Configuration` heading
- `## Repository Registry` table — record each Repository name already listed
- `## Jira Configuration` list — record which fields already have values
- `### Jira Field Defaults` subsection under Jira Configuration — record whether it exists and which fields are populated
- `## Code Intelligence` section — record which Serena instances are already documented
- `## Bug Configuration` section — record whether it exists and which fields are populated
- `## Security Configuration` section — record whether it exists and which fields are populated
- `## Hierarchy Configuration` section — record whether it exists and which fields are populated

If the file doesn't exist, note that everything needs to be created.

## Step 2 – Discover Serena Instances

Examine the available MCP tools to identify Serena instances. Serena tools follow the naming pattern `mcp__<instance-name>__<tool>` where typical tool names include `find_symbol`, `get_symbols_overview`, `search_for_pattern`, `replace_symbol_body`.

Collect the set of unique `<instance-name>` values that correspond to Serena servers.

For each discovered Serena instance that is **not** already in the Repository Registry:
1. Use the instance's `get_diagnostics` tool (which returns the project root path) or ask the user for the repository's local path.
2. Ask the user for:
   - **Repository short name** (e.g., `backend`, `frontend-ui`)
   - **Role** — language and purpose (e.g., "Rust backend", "TypeScript frontend")

If **all** discovered Serena instances are already in the Repository Registry, report "Repository Registry is up to date" and skip to Step 3.

If **no** Serena instances are discovered at all, inform the user that no Serena MCP servers were found and ask whether they want to continue without code intelligence or set up Serena first. If they choose to continue, create an empty Repository Registry table (headers only).

## Step 3 – Jira Configuration

If `## Jira Configuration` already exists with all three required fields (Project key, Cloud ID, Feature issue type ID) populated, report "Jira Configuration is up to date" and skip to Step 3.5.

Otherwise, determine which fields are missing and gather them:

### Step 3.1 – Attempt MCP First

1. Check for an Atlassian MCP server among available tools (tools prefixed with `mcp__atlassian__`).
2. If an Atlassian MCP is available, **try** to use it:
   a. Try `getVisibleJiraProjects` to list available projects
   b. Try `getAccessibleAtlassianResources` to discover the Cloud ID
   c. Try `getJiraProjectIssueTypesMetadata` to list issue types

### Step 3.2 – Handle MCP Failure (REST API Fallback)

If any MCP operation fails, **always prompt the user** (even if REST API credentials exist in CLAUDE.md):

```
❌ Atlassian MCP failed: {error_message}

Would you like to use JIRA REST API v3 fallback?

Options:
1. Yes - Use REST API (requires credentials)
2. No - Skip auto-discovery, I'll provide fields manually
3. Retry - I'll fix MCP configuration and retry

Choose (1/2/3):
```

**If user chooses "1. Yes - Use REST API":**

1. Check `CLAUDE.md` for existing REST API credentials under `### REST API Credentials (MCP Fallback)`
2. If credentials exist:
   - Read Server URL, Email, and API Token (or `$JIRA_API_TOKEN` env var reference)
   - Set environment variables: `JIRA_SERVER_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`
   - Proceed to Step 3.3 (use REST API)
3. If credentials do not exist:
   - Follow credential collection flow (see `shared/jira-rest-fallback.md`)
   - Collect: Server URL, Email, API Token
   - Validate with: `python3 scripts/jira-client.py get_user_info`
   - On success: Display "✅ Authentication successful! Logged in as: {displayName}"
   - Ask storage preference (all in CLAUDE.md / URL+email with env var / don't store)
   - Store if requested under `### REST API Credentials (MCP Fallback)` in `## Jira Configuration`
   - Proceed to Step 3.3 (use REST API)

**If user chooses "2. No - Skip auto-discovery":**
- Proceed to Step 3.4 (manual entry)

**If user chooses "3. Retry":**
- Retry MCP operations once
- If still fails, return to this prompt

### Step 3.3 – Use REST API for Discovery

Use the Python client to gather Jira configuration:

1. **Get project metadata:**
   ```bash
   python3 scripts/jira-client.py get_project_metadata <project-key>
   ```
   Ask user which project key to use if not already known. The response provides:
   - Project key
   - Available issue types with IDs and names

2. **Get user info:**
   ```bash
   python3 scripts/jira-client.py get_user_info
   ```
   Extract Cloud ID from the response (if present in user metadata).
   If Cloud ID is not available via API, ask user to provide it manually.

3. From the project metadata, list issue types and ask user which one is the Feature type (this provides the Feature issue type ID).

4. Ask the user if they have a Git Pull Request custom field ID (optional).

5. Ask the user if they have a GitHub Issue custom field ID (optional).

Proceed to Step 3.5 with the gathered fields.

### Step 3.4 – Manual Entry (Fallback)

If MCP is not available and user chooses not to use REST API, ask the user to provide the missing fields directly:
- Project key
- Cloud ID (Jira cloud site URL, e.g., `mycompany.atlassian.net`)
- Feature issue type ID
- Git Pull Request custom field (optional)
- GitHub Issue custom field (optional)

Only ask for fields that are not already configured.

Proceed to Step 3.5 with the provided fields.

## Step 3.5 – Hierarchy Preferences

Check if `## Hierarchy Configuration` already exists in CLAUDE.md with all fields
populated (no `{{placeholder}}` markers).

- **If it exists and is fully populated**: Report "Hierarchy Configuration is up to date"
  and skip to Step 4.
- **If it exists but contains `{{placeholder}}` markers**: Treat it as not yet populated
  and proceed to the discovery steps below (skip scaffolding the section heading since
  it already exists).
- **If it does NOT exist**: Proceed to discover hierarchy and scaffold the section below.

### Step 3.5.1 – Discover Issue Type Hierarchy

Use the same MCP-first-with-REST-fallback pattern from Step 3:

1. Try `getJiraProjectIssueTypesMetadata` via MCP to list issue types for the project.
2. Group the returned issue types by their `hierarchyLevel` field.
3. If MCP fails, follow the REST API fallback flow from Step 3.2.
4. If auto-discovery fails entirely, ask the user for hierarchy information manually.

Display the discovered hierarchy to the user in a structured format, grouped by
hierarchy level and sorted descending. Include the type name and ID for each.
Mark the configured Feature issue type with "← currently configured":

```
Discovered Jira hierarchy for project <key>:
- Level 3: Outcome (id: 10130)
- Level 2: Feature (id: 10142) ← currently configured
- Level 1: Epic (id: 10000)
- Level 0: Task (id: 10014), Story (id: 10009), Bug (id: 10016), ...
```

### Step 3.5.2 – Ask for Grouping Strategy

If a level-1 type (Epic) exists in the discovered hierarchy, ask:

```
Default Epic grouping strategy for plan-feature?

1. by-repository — one Epic per repository (recommended for multi-repo projects)
2. by-sub-feature — group by logical sub-features
3. trivial — single Epic wrapping all tasks
4. none — ask each time (no default)

Choose (1/2/3/4):
```

If no level-1 type exists in the project, skip the grouping strategy question
entirely and note: "No Epic-level type found in project — Epic grouping is not
available. Hierarchy Configuration will not be created." Then skip to Step 4.

### Step 3.5.3 – Write Hierarchy Configuration

Write the `## Hierarchy Configuration` section to CLAUDE.md with the gathered
values. Follow the template structure from `project-config.template.md`. Present
the planned changes to the user for review before writing.

If the section already exists but has placeholder markers, replace only the
placeholder content, preserving any surrounding text.

## Step 4 – Jira Field Defaults

If `### Jira Field Defaults` already exists under `## Jira Configuration` with all four
fields populated (Default priority, fixVersion scope, Prompt for priority, Prompt for
fixVersion) and none contain `{{placeholder}}` markers, report "Jira Field Defaults is
up to date" and skip to Step 5.

If `## Jira Configuration` does not exist yet (Step 3 was skipped or not completed),
skip to Step 5 — this subsection depends on Jira Configuration being present.

Otherwise, proceed to discover available values and configure the defaults.

### Step 4.1 – Discover Available Priorities and fixVersions

Use `getJiraIssueTypeMetaWithFields` to fetch the available field values for the
Feature issue type:

```
jira.getJiraIssueTypeMetaWithFields(cloudId, projectIdOrKey, issueTypeId)
```

Where:
- `cloudId` is from the Jira Configuration
- `projectIdOrKey` is the Project key from the Jira Configuration
- `issueTypeId` is the Feature issue type ID from the Jira Configuration

From the response, extract:
- **Available priorities** from `priority.allowedValues` — list each priority name
- **Available fixVersions** from `fixVersions.allowedValues` — list each version name

If MCP fails, follow the same REST API fallback pattern from Step 3.2. If REST API
is also unavailable, ask the user to provide the values manually.

### Step 4.2 – Ask User for Defaults

Present the discovered values and ask the user to configure each field:

1. **Default priority**: Show the list of available priorities and ask which one to
   use as the default pre-selection. The user may also choose "none" (no default).

2. **fixVersion scope**: Ask whether fixVersion should apply at the "feature" level
   only, "task" level only, or "both". Default: "both".

3. **Prompt for priority**: Ask whether define-feature should prompt users for
   priority. Default: true.

4. **Prompt for fixVersion**: Ask whether define-feature should prompt users for
   fixVersion. Default: true.

### Step 4.3 – Write Jira Field Defaults

If `### Jira Field Defaults` already exists but has placeholder markers or incomplete
values, replace only the changed fields, preserving any surrounding text. This follows
the setup skill's existing idempotency pattern.

If `### Jira Field Defaults` does not exist, add the subsection under
`## Jira Configuration`, before any other subsections (such as
`### REST API Credentials`).

Use the template format from `project-config.template.md`:

```markdown
### Jira Field Defaults
- Default priority: <selected-priority>
- fixVersion scope: <selected-scope>
- Prompt for priority: <true|false>
- Prompt for fixVersion: <true|false>
```

Present the planned changes to the user for review before writing.

## Step 5 – Code Intelligence

If `## Code Intelligence` already exists and covers all Serena instances from the Repository Registry, report "Code Intelligence is up to date" and skip to Step 6.

If the section doesn't exist, generate it with:
1. The standard tool naming convention explanation: tools are called as `mcp__<instance>__<tool>`.
2. A concrete example using the first Serena instance from the Repository Registry.
3. A `### Limitations` subheading — ask the user if any Serena instances have known limitations (e.g., language server features that don't work). If none, leave the subsection with a note that no limitations are known.

If the section exists but new Serena instances were added in Step 2, ask the user if the new instances have any known limitations and add them under `### Limitations`.

## Step 6 – Write Configuration

Compose the updated `# Project Configuration` section with its subsections.

**If CLAUDE.md doesn't exist**: Create the file with the Project Configuration section.

**If CLAUDE.md exists but has no `# Project Configuration`**: Append the section at the end of the file.

**If CLAUDE.md exists with `# Project Configuration`**: Update only the subsections that changed, preserving all other content in the file and within each subsection.

Present the planned changes to the user for review before writing. Clearly show what will be added or modified. If no changes are needed (everything is already configured), report "Project Configuration is up to date — no changes needed" and stop.

After the user approves, write the changes.

## Step 7 – Copy Constraints Template

Check if `docs/constraints.md` already exists in the target project.

- **If it does NOT exist**: Read `constraints.template.md` from this skill's directory and write its content to `docs/constraints.md` in the target project. Report "Created docs/constraints.md from template."
- **If it DOES exist**: Report "Constraints document already exists — skipping" and preserve the user's customized version.

## Step 8 – Scaffold CONVENTIONS.md

For each repository in the **Repository Registry**, check if a `CONVENTIONS.md` file exists at the repository root (using the **Path** column from the Registry table).

- **If it exists with real content** (no `{{placeholder}}` markers): Report "CONVENTIONS.md already exists in <repository> — skipping" and move to the next repository.
- **If it exists but still contains `{{placeholder}}` markers**: Treat it as not yet populated and proceed to the fill-in prompt below (skip scaffolding since the file already exists).
- **If it does NOT exist**: Ask the user whether they want to scaffold a `CONVENTIONS.md` for that repository. If yes, read `conventions.template.md` from this skill's directory and write its content to `CONVENTIONS.md` at the repository root. Report "Created CONVENTIONS.md in <repository> from template."

This step is optional and does not block the rest of the setup. If the user declines scaffolding for any repository, continue to the next one.

### Fill-in Prompt

After scaffolding a new `CONVENTIONS.md` (or finding an existing one with `{{placeholder}}` markers), ask the user:

> "Would you like me to fill in the CONVENTIONS.md for **<repository-name>** now? I can use code intelligence to analyze the codebase and populate the conventions automatically."

- **If the user declines**: Continue to the next repository without changes.
- **If the user accepts**: Analyze the codebase and populate the conventions as described below.

#### Analyzing the codebase

**For repositories with a Serena instance** (check the **Serena Instance** column in the Repository Registry):
1. Use `get_symbols_overview` on key source files to discover languages, frameworks, and code structure.
2. Use `search_for_pattern` to find naming patterns, error handling idioms, test patterns, and commit message conventions.
3. Use `find_symbol` to inspect representative examples of each convention category.

**For repositories without a Serena instance**:
1. Use Explore agents with Glob, Grep, and Read to analyze the codebase.
2. Glob for source files to identify languages and frameworks.
3. Grep for patterns like error handling, test structures, and naming conventions.
4. Read representative files to confirm discovered patterns.

#### Populating the template

For each section in the `CONVENTIONS.md` template, replace the `{{placeholder}}` marker with the discovered conventions:
- **Language and Framework** — primary languages, frameworks, and build tools
- **Code Style** — formatting tools, linters, style rules
- **Naming Conventions** — casing patterns for types, functions, files, endpoints
- **File Organization** — directory structure and where new files should go
- **Error Handling** — error types, patterns, and idioms
- **Testing Conventions** — test frameworks, patterns, coverage expectations
- **Commit Messages** — commit format and conventions
- **Shared Modules and Reuse** — utility directories, shared helpers, common abstractions, and any reusable code that should be preferred over writing new implementations. Search for directories named `utils/`, `common/`, `shared/`, `helpers/`, or `lib/`, and for widely-imported modules. List the key modules with their paths and purpose.
- **Documentation** — documentation file locations (README, API docs, architecture docs), what kinds of changes trigger a doc update, and documentation formats used. Search for `README.md`, `docs/` directories, API doc files, and architecture documents.
- **Dependencies** — dependency management policies

#### User review

Present the populated `CONVENTIONS.md` to the user for review before writing. Clearly show the content that will be written. Only write the file after the user approves.

## Step 9 – Scaffold Bug Configuration

Check if `## Bug Configuration` already exists in CLAUDE.md with all three required
fields populated (Bug issue type ID, Bug template, Bug-to-Task link type) and none
contain `{{placeholder}}` markers.

- **If it exists and is fully populated**: Report "Bug Configuration is up to date"
  and skip to Step 10.
- **If it exists but contains `{{placeholder}}` markers**: Treat it as not yet populated
  and proceed to the discovery steps below (skip scaffolding the section heading since
  it already exists).
- **If it does NOT exist**: Proceed to discover and scaffold all three fields below.

### Step 9.1 – Discover Bug Issue Type ID

Use the same MCP-first-with-REST-fallback pattern from Step 3:

1. Try `getJiraProjectIssueTypesMetadata` via MCP to list issue types for the project.
2. Look for an issue type named "Bug" in the results and extract its ID.
3. If MCP fails, follow the REST API fallback flow from Step 3.2.
4. If auto-discovery fails entirely, ask the user for the Bug issue type ID manually.

### Step 9.2 – Ask for Bug Template Path

Ask the user for the path where the bug template file should be placed in the target
project. Offer a default:

> "Where should the bug template file be placed? (default: `docs/bug-template.md`)"

### Step 9.3 – Ask for Bug-to-Task Link Type

Retrieve available issue link types:

1. Try `getIssueLinkTypes` via MCP (or `python3 scripts/jira-client.py get_link_types`
   as REST fallback).
2. Display the available link types to the user.
3. Ask the user which link type to use for linking Bugs to Tasks. Offer a default:

> "Which link type should be used to link Bug issues to their remediation Tasks?
> (default: Blocks)"

### Step 9.4 – Copy Bug Template

Check if the bug template file already exists at the user-specified path in the
target project.

- **If it does NOT exist**: Read `docs/templates/bug-template.md` from the plugin's
  templates directory and write its content to the user-specified path in the target
  project. Report "Created <path> from template."
- **If it DOES exist**: Report "Bug template already exists at <path> — skipping"
  and preserve the user's customized version.

### Step 9.5 – Write Bug Configuration

Write the `## Bug Configuration` section to CLAUDE.md with the gathered values.
Follow the template structure from `project-config.template.md`. Present the planned
changes to the user for review before writing.

If the section already exists but has placeholder markers, replace only the placeholder
content, preserving any surrounding text.

## Step 10 – Security Configuration (Optional)

Check if `## Security Configuration` already exists in CLAUDE.md with all required
fields populated (no `{{placeholder}}` markers remaining).

- **If it exists and is fully populated**: Report "Security Configuration is up to date"
  and skip to Step 11.
- **If it exists but contains `{{placeholder}}` markers**: Treat it as not yet populated
  and proceed to the fill-in prompt below (skip scaffolding since the section already exists).
- **If it does NOT exist**: Ask the user whether they want to enable security triage
  for this project:

> "Would you like to enable security triage for this project? This configures the
> triage-security skill to perform CVE impact analysis across supported product versions."

If the user declines, skip to Step 11. If the user accepts, proceed below.

### Step 10.1 – Collect Product Lifecycle fields

Ask the user for the following fields:

1. **Product pages URL** — the product lifecycle page for EOL/support status checks
2. **Jira version prefix** — filters Jira versions to this product (e.g., `MYPRODUCT`)
3. **Vulnerability issue type ID** — the Jira issue type ID for Vulnerability issues.
   If an Atlassian MCP server is available, offer to discover this by listing issue types
   via `getJiraProjectIssueTypesMetadata` and letting the user select the Vulnerability type.
4. **Component label pattern** — the label prefix used by PSIRT on Vulnerability issues
   to identify the affected component (e.g., `pscomponent:`)
5. **VEX Justification custom field** _(optional)_ — the custom field ID used to record
   VEX justification when closing a Vulnerability as "Not a Bug" (e.g., `customfield_00000`).
   This field cannot be auto-discovered via Jira metadata. Ask the user:

   > "Do you have a VEX Justification custom field? If you're unsure, provide a link to
   > a closed Vulnerability issue that has it set (e.g., https://mycompany.atlassian.net/browse/PROJ-456)
   > and I'll extract the field ID from it. Otherwise, leave blank — you can add it later."

   If the user provides an issue link, fetch that issue with all fields and search for
   a field whose value matches a known VEX justification (e.g., "Component not Present",
   "Vulnerable Code not Present"). Extract the field ID.

   If the user skips, leave the placeholder empty in the template.

6. **Upstream Affected Component custom field** _(optional)_ — the custom field ID that
   stores the upstream library name on Vulnerability issues (e.g., `customfield_10632`).
   Used by Step 4.3 for cross-CVE overlap detection. Ask the user:

   > "Do you have an Upstream Affected Component custom field on Vulnerability issues?
   > This field stores the upstream library name (e.g., 'axios', 'webpack') and enables
   > cross-CVE overlap detection. Provide the custom field ID, or leave blank to skip
   > overlap detection."

   If the user skips, leave the placeholder empty in the template.

7. **PS Component custom field** _(optional)_ — the custom field ID that stores the
   PS Component identifier on Vulnerability issues (e.g., `customfield_10669`).
   Used together with the Upstream Affected Component field for cross-CVE overlap
   filtering. Ask the user:

   > "Do you have a PS Component custom field on Vulnerability issues? This field
   > stores the product component identifier (e.g., 'pscomponent:org/image-name')
   > and is used to filter cross-CVE overlap results. Provide the custom field ID,
   > or leave blank."

   If the user skips, leave the placeholder empty in the template.

8. **Stream custom field** _(optional)_ — the custom field ID that stores the stream
   identifier on Vulnerability issues (e.g., `customfield_10832`). Used together with
   the Upstream Affected Component field for cross-CVE overlap filtering. Ask the user:

   > "Do you have a Stream custom field on Vulnerability issues? This field stores
   > the stream identifier (e.g., 'rhtpa-2.2') and is used to filter cross-CVE
   > overlap results. Provide the custom field ID, or leave blank."

   If the user skips, leave the placeholder empty in the template.

9. **ProdSec contact email** _(optional)_ — the email address of the Product Security
   contact for this project. Used for informational reference in CVE triage
   notifications. Ask the user:

   > "ProdSec contact email (optional, for CVE triage notifications)?"

   If the user skips, leave the placeholder empty in the template.

10. **ProdSec Jira account ID** _(optional)_ — the Jira account ID of the ProdSec
    contact. Used for @mentions in triage comments (Affects Versions corrections,
    cross-CVE overlap notifications). Ask the user:

    > "ProdSec Jira account ID (optional, for @mentions in triage comments)?"

    If the user skips, leave the placeholder empty in the template.

11. **Embargo policy URL** _(optional)_ — link to the organization's coordinated
    vulnerability disclosure or embargo policy. When configured, triage-security
    presents a warning gate before proceeding with triage on Critical or Important
    severity CVEs. Ask the user:

    > "Embargo policy URL (optional, for coordinated vulnerability disclosure guidance)?"

    If the user skips, leave the placeholder empty in the template.

### Step 10.2 – Collect Version Streams

Ask the user for one or more version streams. For each stream, collect:

1. **Stream name** — the version range label (e.g., `2.1.x`, `2.2.x`)
2. **Konflux release repo URL** — the git repository URL (e.g.,
   `git.downstream.example.com/my-org/product-release.0.4.z`)
3. **Local path** — the user's local clone path to the Konflux release repo
4. **Security matrix path** — the path to security-matrix.md relative to the project
   working directory (e.g., `docs/security-matrix-2.2.x.md`)

### Step 10.3 – Collect Source Repositories

Ask the user for one or more source repositories whose dependencies are tracked
for CVE analysis. For each repository, collect:

1. **Repository name** — short name (e.g., `backend`, `frontend-ui`)
2. **URL** — the repository URL

### Step 10.4 – Scaffold Security Configuration

Read `security-config.template.md` from this skill's directory and replace the
`{{placeholder}}` markers with the values gathered above.

If the `## Security Configuration` section does not yet exist in CLAUDE.md, append it
after the `## Code Intelligence` section. If the section exists but has placeholders,
replace only the placeholder content, preserving any surrounding text.

Present the planned Security Configuration section to the user for review before writing.

### Step 10.5 – Scaffold security-matrix.md

For each Version Stream configured above, check if a `security-matrix.md` file exists
at the specified path within the project working directory.

- **If it does NOT exist**: Read `security-matrix.md` from `docs/templates/` and offer
  to write it to the configured path in the project directory. The user must confirm each file.
- **If it DOES exist**: Report "security-matrix.md already exists at <path> — skipping."

### Step 10.6 – Populate supportability matrix (Optional)

After scaffolding or confirming security-matrix.md files exist, ask the user:

> "Would you like me to populate the supportability matrix now? I'll query the Konflux
> release repo's git history to discover versions, image digests, build dates, and
> source commits."

If the user declines, skip to Step 11. The matrix can be populated later on demand
by `/triage-security` during CVE investigation.

If the user accepts, for each Version Stream:

1. Read the Konflux release repo's git log or tag history to discover released versions
2. For each version, extract:
   - **Image digest** — from the container image reference in the repo
   - **Build date** — from image metadata or build-date labels
   - **Source commits** — one per source repository, from the pinned references in the repo
   - **Retag status** — whether this version shares the same source commits as another
3. Write the discovered rows into the Supportability Matrix table in the stream's
   `security-matrix.md`
4. Present the populated matrix to the user for review before writing

## Step 11 – Validate

After writing, read the CLAUDE.md back and verify:
- `# Project Configuration` heading exists
- `## Repository Registry` contains a table with columns: Repository, Role, Serena Instance, Path
- `## Jira Configuration` contains at minimum: Project key, Cloud ID, Feature issue type ID
- (If configured) `### Jira Field Defaults` subsection contains valid field values
- `## Code Intelligence` documents the `mcp__<instance>__<tool>` naming convention
- `## Code Intelligence` has a `### Limitations` subheading
- `docs/constraints.md` exists in the target project
- (If scaffolded) `## Bug Configuration` contains: Bug issue type ID, Bug template path, Bug-to-Task link type
- (If scaffolded) The bug template file exists at the configured Bug template path
- (If scaffolded) `## Hierarchy Configuration` contains Default epic grouping strategy
- (If scaffolded) `## Security Configuration` contains `### Product Lifecycle` with all four required fields (VEX Justification is optional)
- (If scaffolded) `## Security Configuration` contains `### Version Streams` with at least one row
- (If scaffolded) `## Security Configuration` contains `### Source Repositories` with at least one row

Report the validation results to the user.

## Important Rules

- **Never remove** existing configuration entries — only add new ones.
- **Never overwrite** user-customized values — if a field already has a value, preserve it.
- **Always present changes** to the user for review before writing to CLAUDE.md.
- **Ask only for what is missing** — do not re-ask for information that is already configured.
- If no changes are needed, report it clearly and stop.
