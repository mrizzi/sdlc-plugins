# Remediation Task Templates

These templates define the Jira Task descriptions created during CVE triage
(Step 8, Case A). Tasks follow `task-description-template.md` so that
`/implement-task` can parse them directly.

The number of tasks depends on the ecosystem type:

- **Source dependency ecosystems** (Cargo, npm): create **two** tasks —
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

- Target branch: [upstream-branch from Ecosystem Mappings]
- **Dependency type**: [direct | transitive (chain: [dependency-chain])]
- If the vulnerable dependency is dev-only or build-only (identified
  in Step 2.3.5), the remediation priority is Normal regardless of CVE
  severity. Add `dev-dependency` label to the task.

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update [library] dependency to >= [fixed-version] in [lock-file-path]
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

When the vulnerable package is a **transitive** dependency (pulled in
through intermediate packages), use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in [library] (see dependency
  chain above)
- Bump the direct dependency to a version whose transitive closure
  includes [library] >= [fixed-version]
- Verify the bump does not introduce breaking API changes to the
  direct dependency

**Fallback: pin the transitive dependency directly**
If bumping the direct dependency is not viable (breaking API changes,
no release available with the fix):
- Cargo: `cargo add [library]@[fixed-version]` to add as a direct
  dependency, overriding the transitive resolution
- npm: add `"[library]": ">=[fixed-version]"` to `overrides` (npm)
  or `resolutions` (yarn/pnpm) in `package.json`
- Document why the direct dep bump was not viable in the PR description

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
- **Dependency type**: [direct | transitive] — carried forward from upstream task
- Update the [source-repo] reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly (fallback
  approach), verify the pinning is reflected in the downstream build's
  lock file after the source reference update
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

## Coordination Guidance

When the affected repository has a deployment context configured in Security Configuration
(see Step 0), append a `### Coordination Guidance` subsection to the Implementation Notes
of each remediation task description. The content varies by deployment context:

- **internal**: "This component is deployed internally. Develop and merge the fix within
  the repository. No public advisory or upstream coordination required."
- **upstream**: "This component is public upstream. Coordinate fix with upstream maintainers
  if the vulnerability is not yet public. Follow your organization's embargo policy before
  discussing in public channels or PRs."
- **customer-shipped**: "This component is shipped to customers. Coordinate with Product
  Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be
  released via a security advisory with explicit CVE-to-component mapping."

When the Deployment Context column is absent from the Source Repositories table (backward
compatibility), omit the coordination guidance entirely — do not add the subsection.

## Jira Issue Creation

After creating each remediation task, post a description digest comment per
`shared/description-digest-protocol.md`. The digest comment MUST be posted
before creating issue links or other comments on the task.

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

# 1a. Post description digest comment (before links or other comments)
upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
# Write description to temp file and compute digest
python3 scripts/sha256-digest.py /tmp/task-desc.md  # → sha256-md:<hex> or sha256-adf:<hex>
jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")

# 2. Downstream propagation subtask
downstream_task = jira.create_issue(
  projectKey: "<project-key>",
  issueTypeName: "Task",
  summary: "Propagate CVE-YYYY-XXXXX fix: update [source-repo] ref in [konflux-repo] ([stream])",
  description: <downstream-task-description>,
  labels: ["ai-generated-jira", "Security", "<CVE-ID>"]
)

# 2a. Post description digest comment (before links or other comments)
downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
python3 scripts/sha256-digest.py /tmp/task-desc.md
jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
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

# Post description digest comment (before links or other comments)
task_desc = jira.get_issue(<task-key>, fields=["description"])
python3 scripts/sha256-digest.py /tmp/task-desc.md
jira.add_comment(<task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
```

## Preemptive Task Variant

When Step 8 Case B identifies affected streams that lack their own CVE Jira,
create proactive remediation tasks using the same templates as Case A but with
these differences:

### Labels

Add `security-preemptive` to the labels array to distinguish proactive tasks
from standard remediation:

```
labels: ["ai-generated-jira", "Security", "<CVE-ID>", "security-preemptive"]
```

### Description prefix

Prepend a note to the Description section of the task template:

```
> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of [originating-CVE-Jira-key] (stream [originating-stream]).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.
```

### Link type

Link preemptive tasks to the originating CVE Jira with "Related" (not "Depend"),
because the originating CVE belongs to a different stream:

```
jira.create_link(
  inwardIssue: <originating-cve-jira-key>,
  outwardIssue: <preemptive-task-key>,
  type: "Related"
)
```

### Creation pseudocode

```
# Source dependency ecosystems — preemptive variant
upstream_task = jira.create_issue(
  projectKey: "<project-key>",
  issueTypeName: "Task",
  summary: "Remediate CVE-YYYY-XXXXX: bump [library] to [fixed-version] ([stream])",
  description: <upstream-task-description-with-preemptive-prefix>,
  labels: ["ai-generated-jira", "Security", "<CVE-ID>", "security-preemptive"]
)

# Post description digest comment (before links or other comments)
upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
python3 scripts/sha256-digest.py /tmp/task-desc.md
jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")

# System package ecosystems — preemptive variant
task = jira.create_issue(
  projectKey: "<project-key>",
  issueTypeName: "Task",
  summary: "Remediate CVE-YYYY-XXXXX: update [package-name] to [fixed-version] ([stream])",
  description: <system-package-task-description-with-preemptive-prefix>,
  labels: ["ai-generated-jira", "Security", "<CVE-ID>", "security-preemptive"]
)

# Post description digest comment (before links or other comments)
task_desc = jira.get_issue(<task-key>, fields=["description"])
python3 scripts/sha256-digest.py /tmp/task-desc.md
jira.add_comment(<task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
```

Downstream propagation subtasks (for source dependency ecosystems) also receive
the `security-preemptive` label, the description digest comment, and use the
same "Related" link to the originating CVE Jira.

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
