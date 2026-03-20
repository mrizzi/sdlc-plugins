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

## Template

Read the file `project-config.template.md` in this skill's directory. Use it as the structural reference for generating the `# Project Configuration` section. Replace the `{{placeholder}}` markers with actual values gathered during the steps below. Preserve the exact headings, table format, and section order from the template.

## Step 1 – Read Existing Configuration

Read the project's CLAUDE.md file. If it exists, parse it for:
- `# Project Configuration` heading
- `## Repository Registry` table — record each Repository name already listed
- `## Jira Configuration` list — record which fields already have values
- `## Code Intelligence` section — record which Serena instances are already documented

If the file doesn't exist, note that everything needs to be created.

## Step 2 – Discover Serena Instances

Examine the available MCP tools to identify Serena instances. Serena tools follow the naming pattern `mcp__<instance-name>__<tool>` where typical tool names include `find_symbol`, `get_symbols_overview`, `search_for_pattern`, `replace_symbol_body`.

Collect the set of unique `<instance-name>` values that correspond to Serena servers.

For each discovered Serena instance that is **not** already in the Repository Registry:
1. Use the instance's `get_diagnostics` tool (which returns the project root path) or ask the user for the repository's local path.
2. Ask the user for:
   - **Repository short name** (e.g., `trustify`, `trustify-ui`)
   - **Role** — language and purpose (e.g., "Rust backend", "TypeScript frontend")

If **all** discovered Serena instances are already in the Repository Registry, report "Repository Registry is up to date" and skip to Step 3.

If **no** Serena instances are discovered at all, inform the user that no Serena MCP servers were found and ask whether they want to continue without code intelligence or set up Serena first. If they choose to continue, create an empty Repository Registry table (headers only).

## Step 3 – Jira Configuration

If `## Jira Configuration` already exists with all three required fields (Project key, Cloud ID, Feature issue type ID) populated, report "Jira Configuration is up to date" and skip to Step 4.

Otherwise, determine which fields are missing and gather them:

1. Check for an Atlassian MCP server among available tools (tools prefixed with `mcp__atlassian__`).
2. If an Atlassian MCP is available:
   a. Use `getVisibleJiraProjects` to list available projects and ask the user which one to use (this provides the Project key).
   b. Use `getAccessibleAtlassianResources` to discover the Cloud ID.
   c. Use `getJiraProjectIssueTypesMetadata` with the chosen project key to list issue types and ask the user which one is the Feature type (this provides the Feature issue type ID).
   d. Ask the user if they have a Git Pull Request custom field ID (optional).
3. If no Atlassian MCP is available, ask the user to provide the missing fields directly:
   - Project key
   - Cloud ID (Jira instance URL or cloud UUID)
   - Feature issue type ID
   - Git Pull Request custom field (optional)

Only ask for fields that are not already configured.

## Step 4 – Code Intelligence

If `## Code Intelligence` already exists and covers all Serena instances from the Repository Registry, report "Code Intelligence is up to date" and skip to Step 5.

If the section doesn't exist, generate it with:
1. The standard tool naming convention explanation: tools are called as `mcp__<instance>__<tool>`.
2. A concrete example using the first Serena instance from the Repository Registry.
3. A `### Limitations` subheading — ask the user if any Serena instances have known limitations (e.g., language server features that don't work). If none, leave the subsection with a note that no limitations are known.

If the section exists but new Serena instances were added in Step 2, ask the user if the new instances have any known limitations and add them under `### Limitations`.

## Step 5 – Write Configuration

Compose the updated `# Project Configuration` section with its subsections.

**If CLAUDE.md doesn't exist**: Create the file with the Project Configuration section.

**If CLAUDE.md exists but has no `# Project Configuration`**: Append the section at the end of the file.

**If CLAUDE.md exists with `# Project Configuration`**: Update only the subsections that changed, preserving all other content in the file and within each subsection.

Present the planned changes to the user for review before writing. Clearly show what will be added or modified. If no changes are needed (everything is already configured), report "Project Configuration is up to date — no changes needed" and stop.

After the user approves, write the changes.

## Step 6 – Copy Constraints Template

Check if `docs/constraints.md` already exists in the target project.

- **If it does NOT exist**: Read `constraints.template.md` from this skill's directory and write its content to `docs/constraints.md` in the target project. Report "Created docs/constraints.md from template."
- **If it DOES exist**: Report "Constraints document already exists — skipping" and preserve the user's customized version.

## Step 7 – Scaffold CONVENTIONS.md

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
- **Dependencies** — dependency management policies

#### User review

Present the populated `CONVENTIONS.md` to the user for review before writing. Clearly show the content that will be written. Only write the file after the user approves.

## Step 8 – Validate

After writing, read the CLAUDE.md back and verify:
- `# Project Configuration` heading exists
- `## Repository Registry` contains a table with columns: Repository, Role, Serena Instance, Path
- `## Jira Configuration` contains at minimum: Project key, Cloud ID, Feature issue type ID
- `## Code Intelligence` documents the `mcp__<instance>__<tool>` naming convention
- `## Code Intelligence` has a `### Limitations` subheading
- `docs/constraints.md` exists in the target project

Report the validation results to the user.

## Important Rules

- **Never remove** existing configuration entries — only add new ones.
- **Never overwrite** user-customized values — if a field already has a value, preserve it.
- **Always present changes** to the user for review before writing to CLAUDE.md.
- **Ask only for what is missing** — do not re-ask for information that is already configured.
- If no changes are needed, report it clearly and stop.
