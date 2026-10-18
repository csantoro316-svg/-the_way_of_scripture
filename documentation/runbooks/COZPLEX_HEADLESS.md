# CozPlex Headless Work

Verified: 2026-10-18

## Repository

- Host: `CozPlex` (`192.168.160.147`)
- User: `cozwood`
- Checkout: `/home/cozwood/Documents/Dev/the_way_of_scripture`
- Branch: `main`
- Remote: `git@github-the-way-of-scripture:csantoro316-svg/-the_way_of_scripture.git`

The checkout is on CozPlex's local disk. Its dedicated GitHub SSH identity is stored on CozPlex, so Git access does not depend on CozDev or forwarded credentials.

## Start Work

From a client with SSH access configured for CozPlex:

```bash
ssh CozPlex
cd /home/cozwood/Documents/Dev/the_way_of_scripture
git status --short --branch
git fetch --prune origin
git pull --ff-only
```

Run the pull only when local work is safely committed or otherwise preserved. Follow `SESSION_START.md` before implementation work and `SESSION_GIT.md` for commits and pushes. Push work before switching between CozPlex and CozDev, then fetch and inspect status on the receiving machine.

For Codex work, use CozPlex as the execution host and the checkout path above as the project directory. Codex is already installed, signed in, and has a running managed app server on CozPlex. An interactive SSH session can start the CLI with:

```bash
~/.local/bin/codex -C /home/cozwood/Documents/Dev/the_way_of_scripture
```

## Verification and Runtime

```bash
python3 tools/check_repo.py
```

The current baseline passes with 0 errors and 401 existing passage warnings.

The managed Codex server already includes Node `22.23.2` in its PATH. Routine cloud commands use the existing host-local certificate wrappers, which select the isolated Firebase toolchain and compatible runtime:

```bash
~/.local/bin/mg-cloud-firebase apps:list --project the-way-of-scripture --json
```

Always pass the Scripture project explicitly: these shared wrappers default to Memory Genie. See [Keyless Cloud Operations](CLOUD_OPERATIONS.md) for the required route and checks. Bare Firebase CLI or interactive user authentication is not the routine deployment path.

## Deployment Follow-up

Both hosts' existing operator certificates passed Memory Genie project and Firebase checks on 2026-10-18. The same operator, `local-cloud-operator@memory-genie-ai.iam.gserviceaccount.com`, was denied Scripture project access on both hosts. The remaining deployment prerequisite is establishing the intended certificate-backed operator route for Scripture's separate project, followed by the Scripture-specific checks and Hosting dry run in the cloud operations runbook. An expired legacy Firebase user session does not establish a need to sign in again.

The Prayer and Faith HTML revision currently differs from its Markdown source. Follow `documentation/changes/2026-10-18-prayer-and-faith-git-backup.md` before regenerating pages.
