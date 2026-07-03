# Triage Outcome -- TC-8002 (CVE-2026-28940)

## Decision: Case C -- Close as Not a Bug (Not Affected)

The version impact analysis conclusively shows that **no supported version** of the product ships a vulnerable version of serde_json. All versions across both the 2.1.x and 2.2.x streams include serde_json >= 1.0.137, which is above the fix threshold of 1.0.135.

This is a **Case C** outcome per the triage-security skill: no supported versions affected, so the issue should be closed as Not a Bug.

## Rationale

- **CVE-2026-28940** affects serde_json versions **before 1.0.135**.
- The earliest serde_json version shipped in any supported product version is **1.0.137** (in stream 2.1.x, versions 2.1.0 and 2.1.1).
- The latest serde_json version shipped is **1.0.139** (in stream 2.2.x, versions 2.2.3 and 2.2.4).
- The PSIRT-claimed Affects Version of "RHTPA 2.2.0" is **incorrect** -- version 2.2.0 ships serde_json 1.0.138, which is not vulnerable.

## Proposed Jira Actions

The following Jira mutations would be performed (each requiring engineer confirmation):

### 1. Correct Affects Versions

Remove the incorrect Affects Version:

- **Current**: `[RHTPA 2.2.0]`
- **Proposed**: `[]` (empty -- no versions are affected)

```
jira.edit_issue("TC-8002", fields={
  "versions": []
})
```

Add a comment documenting the correction:

> Corrected Affects Versions: [RHTPA 2.2.0] -> [] (none affected).
> Based on lock file analysis at pinned commits from security-matrix.md.
> Scoped to stream 2.2.x per issue suffix [rhtpa-2.2], but cross-stream analysis
> confirms no versions in any stream are affected.

### 2. Add Triage Summary Comment

Post a summary comment to TC-8002:

> No supported versions ship a vulnerable version of serde_json.
> Version impact analysis:
>
> | Version | serde_json | Affected? |
> |---------|------------|-----------|
> | 2.1.0   | 1.0.137    | NO        |
> | 2.1.1   | 1.0.137    | NO        |
> | 2.2.0   | 1.0.138    | NO        |
> | 2.2.1   | 1.0.138    | NO        |
> | 2.2.2   | 1.0.138    | NO (retag of 2.2.1) |
> | 2.2.3   | 1.0.139    | NO        |
> | 2.2.4   | 1.0.139    | NO        |
>
> All supported versions ship serde_json >= 1.0.137, which is outside
> the affected range (< 1.0.135).

### 3. Set VEX Justification

Since the VEX Justification custom field (`customfield_12345`) is configured, set it to indicate the component is not present in a vulnerable form:

- **Value**: `Component not Present`

Rationale: The vulnerable version of serde_json (< 1.0.135) is not shipped in any supported product version. All shipped versions include the fixed code.

```
jira.edit_issue("TC-8002", fields={
  "customfield_12345": "Component not Present"
})
```

### 4. Close the Issue

Transition TC-8002 to **Closed** with resolution **Not a Bug**:

```
jira.get_transitions("TC-8002")
# Select transition whose target status is "Closed"
jira.transition_issue("TC-8002", <closed-transition-id>, resolution="Not a Bug")
```

### 5. Add Triage Label

Add the `ai-cve-triaged` label to mark the issue as triaged:

```
jira.edit_issue("TC-8002", fields={
  "labels": ["CVE-2026-28940", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

## Remediation Tasks

**None required.** No supported versions are affected, so no remediation tasks need to be created. This is purely a close-as-not-affected outcome.

## Cross-Stream Impact

No cross-stream impact exists because no versions in any stream are affected:

- Stream 2.1.x: NOT affected (serde_json 1.0.137 in all versions)
- Stream 2.2.x: NOT affected (serde_json 1.0.138-1.0.139 in all versions)

No cross-stream remediation comments or preemptive tasks are needed.
