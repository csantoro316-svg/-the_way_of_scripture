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

The managed Codex server already includes Node `22.23.2` in its PATH. Plain noninteractive SSH commands instead select system Node 18, which cannot run the installed Firebase CLI. For Firebase commands in such a shell, select the existing compatible runtime explicitly:

```bash
export PATH="$HOME/.nvm/versions/node/v22.23.2/bin:$PATH"
firebase --version
```

This runtime is installed locally on CozPlex; no runtime installation or global shell change was needed.

## Deployment Follow-up

Firebase CLI `15.9.0` runs with Node 22, but the saved Firebase authentication requires reauthentication. Deployment access to `the-way-of-scripture` is not yet verified. Refresh the Firebase login on CozPlex using the intended project account before deploying. Do not copy credentials from CozDev or use another project's service account as a workaround.

The Prayer and Faith HTML revision currently differs from its Markdown source. Follow `documentation/changes/2026-10-18-prayer-and-faith-git-backup.md` before regenerating pages.
