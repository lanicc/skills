---
name: git-branch-management
description: Manage Git branch creation and documentation with project-specific branch naming rules. Use when Codex needs to create, rename, suggest, or document branches for requirements, small optimizations, minor adjustments, or bug fixes, and when updating git-branchs.md with branch descriptions.
---

# Git Branch Management

## Overview

Use this skill to choose the correct Git branch prefix, generate a date-based English short name, create or rename the branch, and document the branch in `git-branchs.md`.

## Branch Type Rules

Classify the work before naming the branch:

- Use `feature/` for new requirements or larger user-facing capabilities.
- Use `develop/` for small optimizations, minor adjustments, cleanup, or low-risk refinements.
- Use `bugfix/` for defects, regressions, broken behavior, incorrect data, or failed workflows.

If the user's wording is ambiguous, infer conservatively from the requested work. Ask a short clarification only when the branch category would materially change the workflow or release expectations.

## Naming Format

Use the current local date in `yyyyMMdd` format unless the user explicitly provides another date.

Use lowercase English words for the short name. Keep it concise, descriptive, and hyphenated when it contains multiple words.

Formats:

- Requirement: `feature/yyyyMMdd_requirement-short-name`
- Small optimization or minor adjustment: `develop/yyyyMMdd_adjustment-short-name`
- Bug fix: `bugfix/yyyyMMdd_bug-short-name`

Examples:

- `feature/20260618_login`
- `develop/20260403_table-filter`
- `bugfix/20260203_payment-callback`

## Workflow

1. Inspect the current branch and worktree before creating or renaming a branch:
   - Run `git status --short --branch`.
   - Preserve user changes. Do not reset, checkout over, or discard changes unless the user explicitly requests it.
2. Choose the branch category from the work type.
3. Generate the branch name with the current date and English short name.
4. Check whether the branch already exists:
   - Run `git branch --list <branch-name>`.
   - If it exists, choose a slightly more specific short name or ask the user.
5. Create or rename the branch using the least disruptive command for the situation:
   - Use `git switch -c <branch-name>` for a new branch from the current HEAD.
   - Use `git branch -m <branch-name>` only when the user wants to rename the current branch.
6. Update `git-branchs.md` in the repository root with the branch name and detailed Chinese description.

## git-branchs.md

Keep branch documentation in `git-branchs.md` at the repository root.

Create the file if it does not exist. Append a new line for each branch unless an entry for the same branch already exists. If an entry exists, update it instead of duplicating it.

Entry format:

```markdown
branch-name: detailed Chinese description
```

Example:

```markdown
feature/20250902_login: 开发登录相关的功能
```

Descriptions should explain the business purpose or technical intent, not just repeat the short branch name.

## Output

When finished, report the created or selected branch name and the `git-branchs.md` entry that was added or updated.
