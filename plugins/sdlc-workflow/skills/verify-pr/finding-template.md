# Finding Template

Structured output template for domain sub-agent results during verify-pr
execution. Each sub-agent returns its analysis using this template. The
orchestrator expects this exact structure.

## Template

````markdown
## Verdicts

| Check | Verdict | Summary |
|---|---|---|
| <check name> | <PASS|WARN|FAIL|N/A> | <one-line summary> |

## Findings

### <check name> -- <PASS|WARN|FAIL|N/A>

**Details:** <what was found>

**Evidence:**
- <file path, line number, command output, or other concrete evidence>

**Related review comments:** <comment IDs, or "none">

## Actions

### <action type>: <short title>

**Type:** <create-sub-task | upgrade-comment>
**Details:** <action-specific fields>
````

## Action Type Fields

### create-sub-task

Used when a check identifies an issue requiring tracked work (e.g., CI
failures, acceptance criteria gaps).

```markdown
**Type:** create-sub-task
**Title:** <suggested sub-task title>
**Relevant files:** <file paths>
**Root cause:** <what caused the issue>
```

### upgrade-comment

Used when a classified suggestion matches a CONVENTIONS.md pattern, warranting
escalation to a code change request.

```markdown
**Type:** upgrade-comment
**Comment ID:** <PR comment ID>
**Original classification:** suggestion
**Matching convention:** <the CONVENTIONS.md section that matches>
```

## Rules

- Verdicts table is mandatory, even if all checks are PASS
- Findings section includes one subsection per check; PASS checks get a brief confirmation, non-PASS checks get full evidence
- Actions section is omitted entirely if there are no actions (not an empty section -- omitted)
- The template is the same for all 4 sub-agents; each fills in its own checks
