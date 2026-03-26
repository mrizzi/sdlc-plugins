# AI-Assisted SDLC Metrics

This document defines the metrics for measuring the effectiveness of the
AI-assisted SDLC workflow. Use these metrics to quantify ROI and identify
areas for improvement.

---

## Metrics

### 1. Tasks Planned per Feature

**What it measures:** The number of implementation tasks created by
`plan-feature` in a single invocation.

**Data source:** Jira — issues with the label `ai-generated-jira` linked to
a parent feature.

**How to query:**

```jql
labels = "ai-generated-jira" AND parent = <FEATURE-KEY>
```

Count the results to get the number of tasks planned for that feature.
Track this over time to understand planning granularity and whether the
agent produces a reasonable number of tasks per feature.

---

### 2. Tasks Implemented per Session

**What it measures:** The number of `implement-task` completions in a single
working session (typically one developer sitting).

**Data source:** Jira — issues transitioned to "In Review" with the label
`ai-generated-jira`, filtered by the transition timestamp.

**How to query:**

```jql
labels = "ai-generated-jira" AND status changed to "In Review" during (<start-date>, <end-date>)
```

Replace `<start-date>` and `<end-date>` with the session's date range
(e.g., `"2026-03-19"`, `"2026-03-19"`). Count results per assignee for
per-developer throughput.

---

### 3. PR Merge Rate

**What it measures:** The percentage of agent-created pull requests that are
merged without requiring human code changes (i.e., merged as-is or with
only review comments, no additional commits by humans).

**Data source:** GitHub — PRs on branches matching the Jira issue key
pattern (e.g., `TC-1234`), cross-referenced with commit authors.

**How to query:**

1. List merged PRs with agent branches:
   ```
   gh pr list --state merged --search "head:TC-"
   ```
2. For each PR, check whether all commits are authored by the agent
   (trailer `Assisted-by: Claude Code`). If a human added fix-up commits
   after the agent's PR, the PR required rework.

**Calculation:** `(PRs merged without human commits / total agent PRs merged) * 100`

---

### 4. Time from Task Creation to PR

**What it measures:** The elapsed time between the Jira issue creation
timestamp and the pull request opened timestamp.

**Data source:**
- Jira — the `created` field on the issue
- GitHub — the PR `createdAt` timestamp

**How to query:**

1. Get the issue creation date:
   ```jql
   key = <ISSUE-KEY>
   ```
   The `created` field in the response contains the timestamp.

2. Get the PR creation date:
   ```
   gh pr list --search "head:<ISSUE-KEY>" --json createdAt
   ```

3. Compute the difference. Lower values indicate faster agent throughput.

---

### 5. Agent Failure Rate

**What it measures:** The percentage of tasks where the agent stopped
execution and asked the user for help instead of completing autonomously.

**Data source:** Jira — issues with label `ai-generated-jira` that were
transitioned to "In Progress" but never reached "In Review" within the
session, or issues where agent comments indicate a blocker.

**How to query:**

```jql
labels = "ai-generated-jira" AND status = "In Progress" AND status changed to "In Progress" before <end-date>
```

Issues matching this query that have not progressed to "In Review" likely
represent agent failures. Cross-reference with agent comments on the issue
for confirmation.

**Calculation:** `(tasks requiring human intervention / total tasks attempted) * 100`

---

### 6. Rework Rate

**What it measures:** The percentage of agent-submitted PRs that required
human code changes after submission (additional commits by non-agent
authors before merge).

**Data source:** GitHub — commit history on agent-created PRs.

**How to query:**

1. List agent PRs (merged and open):
   ```
   gh pr list --state all --search "head:TC-"
   ```
2. For each PR, inspect the commit log:
   ```
   gh pr view <PR-NUMBER> --json commits
   ```
3. Check for commits without the `Assisted-by: Claude Code` trailer — these
   are human rework commits.

**Calculation:** `(PRs with human rework commits / total agent PRs) * 100`

---

### 7. Review Feedback Sub-tasks per Task

**What it measures:** The number of review feedback sub-tasks created by
`verify-pr` for a given implementation task. This measures first-pass
implementation quality — fewer sub-tasks means the agent produced code that
better satisfied reviewer expectations on the first attempt.

**Data source:** Jira — issues with the label `review-feedback` that are
sub-tasks of an `ai-generated-jira` task.

**How to query:**

```jql
labels = "review-feedback" AND parent = <TASK-KEY>
```

Count the results to get the number of review feedback sub-tasks for that task.
Track this over time per task to measure whether first-pass quality is improving.
A declining trend indicates that upstream improvements (root-cause fixes) are
taking effect.

---

### 8. Root-Cause Improvements Created

**What it measures:** The number of root-cause improvement tasks created by
`verify-pr`'s root-cause investigation. This measures systemic improvement
opportunities identified — each root-cause task targets an upstream workflow
phase to prevent similar defects in future tasks.

**Data source:** Jira — issues with the label `root-cause` linked to
`ai-generated-jira` tasks.

**How to query:**

```jql
labels = "root-cause"
```

Count the results to get the total number of root-cause improvements created.
Group by the workflow phase targeted (define-feature, plan-feature,
implement-task, conventions) to understand where gaps most frequently originate.

---

## Data Sources Summary

| Source | What it provides |
|--------|-----------------|
| Jira issues | Task counts, timestamps (`created`), status transitions, labels (`ai-generated-jira`, `review-feedback`, `root-cause`) |
| Jira transitions | Status change history with timestamps |
| GitHub PRs | PR creation time, merge status, commit authors |
| Git trailers | `Assisted-by: Claude Code` identifies agent commits |

---

## Future Enhancement

A `/sdlc-workflow:metrics` skill could automate the collection and
reporting of these metrics by querying Jira and GitHub APIs directly,
producing a dashboard or summary report on demand.
