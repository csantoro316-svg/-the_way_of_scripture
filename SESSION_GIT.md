# Git Sync + Commit Prompt

Use this prompt when git actions are needed for repo-scoped work.

## Scope Rule

- Assess the full visible working tree first.
- Include valid local changes that match the intended scope.
- If scope is narrowed, state what is excluded and why before committing.

## Instructions

1. Run a sync safety check before commit/push.
2. Review local work to commit and flag unexpected changes.
3. Confirm required documentation exists for the changed scope.
4. Create a concise commit message with a short title and useful body bullets.
5. Stage intended files, commit, and push.

## Output

Provide:

1. Sync assessment result
2. Final commit message
3. Git actions taken or blocked reason
4. Post-push status summary

## Notes

- This repository is website-rooted, so normal site work still uses this root git workflow.
