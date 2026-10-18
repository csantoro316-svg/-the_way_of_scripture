> **Session Start**
>
> Use this file to begin work in `the_way_of_scripture`.

# Session Start

Purpose: stable startup protocol for this repository.

This file is a starting guide and should remain mostly stable.
Session continuity should come from change docs in:

- `documentation/changes/`

## Startup Sequence

1. Read `documentation/README.md` for repo documentation boundaries.
2. Read `documentation/architecture/PROJECT_DOCTRINE_AND_STANDARDS.md` for the master content, translation, and project standards.
3. Read `documentation/runbooks/SESSION_RESUME.md` for baseline repo context.
4. Read `documentation/runbooks/CLOUD_OPERATIONS.md` for the required keyless cloud route, then read the newest relevant change docs to recover the latest state.
5. Verify local status before changing implementation behavior.
6. Run both read-only readiness checks from `documentation/runbooks/CLOUD_OPERATIONS.md` on the active host. Record the host, `the-way-of-scripture` project, and both results in the session assessment.

## Keyless Cloud Operating Rule

- All routine Firebase and Google Cloud commands use the executing host's `~/.local/bin/mg-cloud-firebase`, `mg-cloud-gcloud`, or `mg-cloud-run` certificate wrapper.
- Always select `the-way-of-scripture` explicitly; the shared wrappers default to Memory Genie. The projects have separate owning accounts.
- CozDev and CozPlex each have independent host certificates. When cloud work moves to the other host, run the readiness checks there before its first cloud operation.
- Use the runbook's certificate repair and alternate-host route if a check fails. Do not ask for interactive Firebase login because an old user session expired, run a bare cloud CLI, copy credentials, or dispatch a Memory Genie workflow as a workaround.
- Report readiness only after the Scripture project read and Firebase app-list checks succeed. Wrapper existence, an old successful check, or Memory Genie access alone is insufficient.
- A successful check or Hosting dry run does not publish the site. Follow the content execution standard and the user's deployment scope for live releases.

## Documentation Rules

- Stable repo docs live under `documentation/`.
- Repo change history lives under `documentation/changes/`.
- Use `SESSION_DOCUMENTATION_UPDATE.md` for repo-scoped documentation updates.
- Use `SESSION_GIT.md` for repo-scoped sync/commit/push workflow.
