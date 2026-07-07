# Contributing to sdlc-plugins

Thank you for your interest in contributing! This document describes our
contributors ladder, governance policies, and workflows for issues and pull
requests.

## Contributors Ladder

This project uses a four-tier contributors ladder mapped to GitHub repository
roles:

| Tier | GitHub Role | Capabilities |
|------|-------------|--------------|
| Contributor | Read | File issues, submit PRs, participate in discussions |
| Reviewer | Write | All Contributor capabilities, plus: review and approve PRs, push to non-protected branches, triage issues |
| Maintainer | Maintain | All Reviewer capabilities, plus: merge PRs, manage releases, configure branch protection, maintain CI |
| Owner | Admin | All Maintainer capabilities, plus: manage repository settings, grant/revoke roles, make governance decisions |

## Current Contributors

| Name | Tier |
|------|------|
| mrizzi | Owner |
| ruromero | Maintainer |
| mrrajan | Contributor |

## Promotion Criteria

Promotions follow a hybrid model: approximately three months of sustained,
quality contributions combined with maintainer judgment. Mechanical tenure alone
is not sufficient — the quality, scope, and consistency of contributions matter
more than the calendar.

### Tier Transitions

| Transition | Who Nominates | Who Approves |
|------------|---------------|--------------|
| Contributor to Reviewer | Any Maintainer or Owner | One other Maintainer or Owner (not the nominator) |
| Reviewer to Maintainer | Any Owner | Another Owner (not the nominator) |
| Maintainer to Owner | Existing Owners | Consensus among all existing Owners |

Nominations are made by opening a discussion in the repository. The nominee
should be given the opportunity to accept or decline before any role change is
applied.

## Demotion Policy

Contributors who have been inactive for approximately one year may have their
role adjusted. Before any role change:

1. A Maintainer or Owner reaches out privately to the contributor to understand
   their situation and intentions.
2. The contributor is given a reasonable opportunity to respond.
3. Only after this private conversation may a role change be proposed.

Role changes due to inactivity are not punitive — contributors are welcome to
re-engage at any time and work toward re-promotion through the normal promotion
criteria.

## Reporting Issues

### External contributors

[GitHub Issues](../../issues) are the entry point for external contributors.
Use the available issue templates:

- **Bug report** — describe unexpected behavior with steps to reproduce
- **Feature request** — propose new functionality or improvements

### Internal team members

Internal team members are welcome to create issues directly in the project's
Jira board. Link the Jira issue to a GitHub Issue when external visibility is
needed.

## Submitting Pull Requests

This project uses a fork-and-PR model:

1. **Fork** the repository to your own GitHub account.
2. **Create a branch** in your fork for the change.
3. **Reference the GitHub Issue** in your PR description (e.g.,
   `Closes #42`). If no issue exists, consider creating one first.
4. **Follow Conventional Commits** for commit messages (e.g.,
   `feat(plan-feature): add validation step`). See
   [CONVENTIONS.md](CONVENTIONS.md) for the full commit message format.
5. **Open a pull request** against the `main` branch of this repository.
6. **Address review feedback** — at least one Reviewer (Write role or above)
   must approve the PR before it can be merged.
7. **Merging** — Maintainers or Owners merge approved PRs.

## Branch Protection

The `main` branch is protected with the following rules:

- **Pull request reviews required** — direct pushes to `main` are not allowed;
  all changes must go through a reviewed pull request.
- **Passing CI required** — the CI pipeline must pass before a PR can be merged.
- **At least one approval from a Write-level or above contributor** — a
  Reviewer, Maintainer, or Owner must approve the PR.

> **Note:** Applying and updating these rules in GitHub repository settings is a
> manual admin action performed by Owners.
