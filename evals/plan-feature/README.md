# plan-feature Evals

Evaluations for the `plan-feature` skill. See the
[framework README](../README.md) for how evals work and how to run them.

## Test cases

| ID | Name | Purpose |
|----|------|---------|
| 1 | Standard feature | Well-structured Jira Feature, single backend repo. The golden path. |
| 2 | Ambiguous feature | Vague acceptance criteria, missing details. Tests gap awareness. |
| 3 | Multi-repo feature | Frontend + backend repos with Figma context. Tests cross-repo decomposition. |
| 4 | Adversarial feature | Prompt injection attempts embedded in the Feature description. Tests injection resistance. |

## Fixture files

Files in `files/` simulate what MCP tools would return during a real
skill invocation. The eval prompt instructs the agent to read these files
instead of calling external tools.

### Feature fixtures (`feature-*.md`)

Mock Jira Feature issues in Markdown. Each contains issue metadata and
feature description sections matching the Jira Feature template.

### Repository manifests (`repo-*.md`)

Directory tree snapshots showing the target repository layout — key files,
module structure, and conventions. The skill uses these to ground file
paths in task descriptions.

### Figma context (`figma-context.md`)

Design context simulating output from Figma MCP tools, used by the
multi-repo test case.

## Running

```
/skill-litmus:run-evals Run evals for plan-feature.
Evals path: evals/plan-feature/evals.json
Workspace: /tmp/plan-feature-eval
```
