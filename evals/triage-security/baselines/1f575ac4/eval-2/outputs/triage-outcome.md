# Triage Outcome -- TC-8002 (CVE-2026-28940)

## Triage Decision: Close as Not a Bug (not affected)

**Case C -- No supported versions affected.**

The version impact analysis shows that **no supported product version ships a vulnerable version of serde_json**. All versions across both the 2.1.x and 2.2.x streams ship serde_json >= 1.0.135, which is at or above the fix threshold. The vulnerability (CVE-2026-28940: stack overflow on deeply nested JSON input) was fixed in serde_json 1.0.135, and the earliest version shipped by any product release is 1.0.137.

## Evidence Summary

| Stream | Versions | serde_json shipped | Fix threshold | Affected? |
|--------|----------|--------------------|---------------|-----------|
| 2.1.x | 2.1.0, 2.1.1 | 1.0.137 | 1.0.135 | NO |
| 2.2.x | 2.2.0--2.2.4 | 1.0.138--1.0.139 | 1.0.135 | NO |

## VEX Justification

Since the VEX Justification custom field is configured (`customfield_12345`), the field should be set to:

**Component not Present** -- specifically, the *vulnerable version* of serde_json (< 1.0.135) is not present in any shipped product version. All versions ship a patched version of the library.

Note: While the serde_json package itself is present, the vulnerable code (versions before 1.0.135 which lacked the recursion limit) is not present in any shipped version. The appropriate VEX justification is "Vulnerable Code not Present" since the patched version includes the fix (configurable recursion limit defaulting to 128 levels). However, given that the lock file analysis shows the *version* shipped is above the fix threshold, "Component not Present" (referring to the vulnerable component version) is the standard default per skill guidelines.

## Proposed Jira Actions

The following Jira mutations would be proposed to the engineer for confirmation:

### 1. Affects Versions Correction (Step 3)

Since no versions in the scoped stream (2.2.x) are affected, the Affects Versions field should be cleared or the issue should proceed directly to closure:

- **Current**: RHTPA 2.2.0
- **Proposed**: Remove RHTPA 2.2.0 (not actually affected based on lock file evidence)

### 2. Post Triage Comment

Add a comment to TC-8002:

> No supported versions ship a vulnerable version of serde_json.
> Version impact analysis:
>
> | Version | serde_json | Affected? |
> |---------|------------|-----------|
> | 2.1.0 | 1.0.137 | NO |
> | 2.1.1 | 1.0.137 | NO |
> | 2.2.0 | 1.0.138 | NO |
> | 2.2.1 | 1.0.138 | NO |
> | 2.2.2 | 1.0.138 | NO (retag of 2.2.1) |
> | 2.2.3 | 1.0.139 | NO |
> | 2.2.4 | 1.0.139 | NO |
>
> All supported versions ship serde_json >= 1.0.135, which is outside the affected range (< 1.0.135).
> Closing as Not a Bug -- the vulnerable version of serde_json is not present in any supported release.

### 3. Close Issue

- **Transition**: Close TC-8002
- **Resolution**: Not a Bug
- **VEX Justification** (`customfield_12345`): Component not Present
- **Assignee**: Set to current user

### 4. Add Label

Add `ai-cve-triaged` label to TC-8002 to mark it as triaged and prevent re-triage.

### 5. Post-Triage Summary Comment

A final summary comment would be posted to TC-8002 documenting:
1. The version impact table (all versions NOT affected)
2. No Affects Versions corrections needed (issue is being closed)
3. Triage outcome: Closed as Not a Bug
4. No remediation tasks created (none needed)
5. @mention of the issue reporter (PSIRT analyst) via ADF mention node

The comment would include the Comment Footnote per `shared/comment-footnote.md` with skill name `triage-security`.

## Steps Not Applicable

- **Step 4 (Duplicate/Sibling Check)**: Would still be performed via JQL search, but results do not change the close decision since no versions are affected.
- **Step 5 (Version Lifecycle Check)**: Moot -- no affected versions to check lifecycle status for.
- **Step 6 (Already Fixed Check)**: Not applicable -- the library was never vulnerable in any shipped version, so this is a "not affected" scenario rather than an "already fixed" scenario.
- **Step 7 (Remediation)**: No remediation tasks needed. No versions are affected.
