# CozPlex Headless Readiness

Date: 2026-10-18
Scope: repository operations

## Findings and Actions

- Found an existing clean checkout on CozPlex at `/home/cozwood/Documents/Dev/the_way_of_scripture`, four commits behind GitHub.
- Fetched and fast-forwarded `main` to preserve all existing history and bring the checkout current.
- Verified CozPlex's dedicated GitHub SSH identity authenticates as `csantoro316-svg`; `git push --dry-run origin main` succeeded.
- Confirmed the checkout resides on local ext4 storage and does not depend on CozDev.
- Confirmed Codex is installed and signed in, with an existing running managed app server whose PATH includes Node 22.23.2.
- Added `documentation/runbooks/COZPLEX_HEADLESS.md` with repository access, handoff, verification, and runtime instructions.

## Validation

- CozPlex: `python3 tools/check_repo.py` passed with 0 errors and the same 401 existing passage warnings observed on CozDev.
- CozPlex: Firebase CLI 15.9.0 runs under the installed Node 22.23.2 runtime.
- The initial bare Firebase project listing failed, but that command used an obsolete interactive-user path. The reauthentication diagnosis was incorrect; see `2026-10-18-keyless-cloud-operations-correction.md` for certificate checks and the actual project-access blocker.
- No site generation or deployment was performed.

## Follow-up

Use the existing certificate wrappers and resolve Scripture project IAM access before deployment work, as described in `../runbooks/CLOUD_OPERATIONS.md`. Editing, local checks, and Git synchronization are available independently of CozDev.
