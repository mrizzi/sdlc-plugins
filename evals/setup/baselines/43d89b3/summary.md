## Eval Results: setup

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 6/7 | 1 | 86% |
| eval-2 | 6/6 | 0 | 100% |
| eval-3 | 6/6 | 0 | 100% |
| eval-4 | 6/6 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-1: 1 failing assertion</summary>

- **Assertion:** "outputs/changes-log.md indicates all sections were newly added (no preserved entries since this is a greenfield setup)"
  **Evidence:** "changes-log.md lines 3-9 show a '## Preserved (from existing CLAUDE.md)' section that lists 3 preserved items: '# my-project heading and project description', '## Documentation section', '## Getting Started section'. While no Project Configuration content existed previously, the changes log does not indicate a fully greenfield setup — it preserves existing CLAUDE.md content. However, lines 17-42 show all Project Configuration sections (Repository Registry, Jira Configuration, Code Intelligence) were newly added. The assertion states 'all sections were newly added (no preserved entries since this is a greenfield setup)' — the log contradicts this by explicitly listing preserved entries."

</details>

**Pass rate:** 96% · **Tokens:** 27,431 · **Duration:** 81s

