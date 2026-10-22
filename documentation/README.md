# Repository Documentation

This is the single documentation tree for the repository.

## Structure

- `changes/`: repo change records.
- `planning/`: active and queued repo plans.
- `architecture/`: stable repo architecture and workflow docs.
- `runbooks/`: operational runbooks and resume entrypoints.
- `testing/`: verification notes and test evidence.

## Current Canonical Resume

- `documentation/runbooks/SESSION_RESUME.md`

Use this as the default handoff/start file for sessions.

## Operational Entry Points

- [Session start](../SESSION_START.md): required startup reading and active-host keyless readiness checks.
- [Keyless cloud operations](runbooks/CLOUD_OPERATIONS.md): canonical Firebase/Google Cloud route, explicit Scripture project selection, verification commands, and failure handling.
- [CozPlex headless work](runbooks/COZPLEX_HEADLESS.md): independent host checkout, access, and machine handoff.
- [Content execution standard](architecture/CONTENT_EXECUTION_STANDARD.md): source generation, verification, and certificate-backed Hosting deployment.
- [Passage editorial standard](architecture/PASSAGE_EDITORIAL_STANDARD.md): source hierarchy, fair interpretation comparisons, optional plan connections, and position authority.
- [Git workflow](../SESSION_GIT.md): repository sync, commit, and push.

## Scope Boundary

- Planning and workflow docs stay under `documentation/...`.
- Content source material stays under `content/...`.
- Site implementation files stay under `apps/web/...`.
