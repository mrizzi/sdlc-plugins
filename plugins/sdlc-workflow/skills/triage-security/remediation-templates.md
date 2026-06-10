# Remediation Task Templates

These templates define the Jira Task descriptions created during CVE triage
(Step 7, Case A). Tasks follow `task-description-template.md` so that
`/implement-task` can parse them directly.

The number of tasks depends on the ecosystem type:

- **Source dependency ecosystems** (Cargo, npm, Go modules): create **two** tasks —
  an upstream backport task (fix in the source repo) and a downstream propagation
  subtask (update the reference in the Konflux release repo). The downstream subtask
  is blocked by the upstream task.
- **System package ecosystems** (RPM): create **one** task — the fix happens directly
  in the Konflux release repo (Dockerfiles, lock files). No upstream step needed.

## Upstream backport task (source dependency ecosystems)

```
## Repository

<source-repository-name from Ecosystem Mappings Repository column>

## Target Branch

<upstream-branch from Ecosystem Mappings Upstream Branch column>

## Description

Remediate CVE-YYYY-XXXXX: [library vulnerability description].
The vulnerable dependency ([library] [affected-range]) must be updated
to the fixed version ([fixed-version]+).

Affected versions: [list from version impact table]
Source commit(s): [commit hash(es) from supportability matrix]

Upstream fix: [upstream PR URL from remote links]
Advisory: [advisory URL from remote links]

## Implementation Notes

- Update [library] dependency to >= [fixed-version] in [lock-file-path]
- Target branch: [upstream-branch from Ecosystem Mappings]
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] [library] dependency is >= [fixed-version]
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: [Vulnerability issue key] (parent tracking issue)
```

## Downstream propagation subtask (source dependency ecosystems)

After the upstream backport task is created, create a second Task for the
downstream propagation. This task updates the source reference in the Konflux
release repo to pick up the upstream fix. It is blocked by the upstream task.

```
## Repository

<konflux-release-repo-name from Version Streams table>

## Target Branch

main

## Description

Update [source-repo] reference in [konflux-release-repo] to pick up the
CVE-YYYY-XXXXX fix from [upstream-task-key].

The upstream backport ([upstream-task-key]) bumps [library] to [fixed-version]
on [upstream-branch]. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: [from Source Pinning Method in security-matrix.md]
- Update the [source-repo] reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] [source-repo] reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: [upstream-task-key] (upstream backport must merge first)
- Depends on: [Vulnerability issue key] (parent tracking issue)
```

## System package task (RPM ecosystems)

For system package ecosystems, the fix happens directly in the Konflux release
repo. Create a single task with propagation steps inline. The propagation path
depends on the package origin identified in Step 2.3.5.

### Base image origin

```
## Repository

<konflux-release-repo-name from Version Streams table>

## Target Branch

main

## Description

Remediate CVE-YYYY-XXXXX: update base image to include patched [package-name].
Current base image: [image-reference]:[tag-or-digest] (from Dockerfile).

## Implementation Notes

- Check base image vendor for an updated version that includes
  the patched [package-name]
- Update the FROM reference in Dockerfile
- If using floating tag: verify a rebuild picks up the fix
- If lock file exists: regenerate rpms.lock.yaml

## Acceptance Criteria

- [ ] Base image reference updated to a version with patched [package-name]
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully

## Dependencies

- Depends on: [Vulnerability issue key] (parent tracking issue)
```

### Explicit install origin

```
## Repository

<konflux-release-repo-name from Version Streams table>

## Target Branch

main

## Description

Remediate CVE-YYYY-XXXXX: update [package-name] to [fixed-version].

## Implementation Notes

- Update the package version in Dockerfile (dnf install command or package spec)
- If lock file exists: regenerate rpms.lock.yaml

## Acceptance Criteria

- [ ] [package-name] is >= [fixed-version]
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully

## Dependencies

- Depends on: [Vulnerability issue key] (parent tracking issue)
```

**Omitted sections**: Files to Modify and Files to Create are intentionally omitted.
These depend on repository structure that the triage skill does not have context for —
`implement-task` discovers them via code analysis.

## Jira Issue Creation

### Source dependency ecosystems — create two tasks:

```
# 1. Upstream backport task
upstream_task = jira.create_issue(
  projectKey: "<project-key>",
  issueTypeName: "Task",
  summary: "Remediate CVE-YYYY-XXXXX: bump [library] to [fixed-version] ([stream])",
  description: <upstream-task-description>,
  labels: ["ai-generated-jira", "Security", "<CVE-ID>"]
)

# 2. Downstream propagation subtask
downstream_task = jira.create_issue(
  projectKey: "<project-key>",
  issueTypeName: "Task",
  summary: "Propagate CVE-YYYY-XXXXX fix: update [source-repo] ref in [konflux-repo] ([stream])",
  description: <downstream-task-description>,
  labels: ["ai-generated-jira", "Security", "<CVE-ID>"]
)
```

### System package ecosystems — create one task:

```
task = jira.create_issue(
  projectKey: "<project-key>",
  issueTypeName: "Task",
  summary: "Remediate CVE-YYYY-XXXXX: update [package-name] to [fixed-version] ([stream])",
  description: <system-package-task-description>,
  labels: ["ai-generated-jira", "Security", "<CVE-ID>"]
)
```

## Jira Linkage

After creating remediation tasks:

1. **Link** each task to the Vulnerability issue:
   ```
   jira.create_link(
     inwardIssue: <vulnerability-key>,
     outwardIssue: <task-key>,
     type: "Depend"
   )
   ```
2. **For source dependency ecosystems**, link the downstream subtask as blocked
   by the upstream task:
   ```
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   ```
3. **Transition** the Vulnerability to In Progress (if not already).
4. **Assign** the Vulnerability to the current user (if not already assigned).
5. **Add comment** to the Vulnerability listing all created tasks:
   - Source dependency: "Remediation tasks created: [upstream-task-key] (upstream
     backport), [downstream-task-key] (downstream propagation, blocked by
     [upstream-task-key])"
   - System package: "Remediation task created: [task-key]"
