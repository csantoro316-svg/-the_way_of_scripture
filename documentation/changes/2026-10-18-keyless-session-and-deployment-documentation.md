# Keyless Session and Deployment Documentation

Date: 2026-10-18
Scope: repository operating instructions

## Changes

- Made the cloud runbook required startup reading and both active-host Scripture readiness checks part of `SESSION_START.md`.
- Made the certificate wrapper route, explicit Scripture project selection, alternate-host checks, and readiness reporting explicit in the startup instructions.
- Added operational entry points to `documentation/README.md` so the startup, cloud, headless, content, and Git workflows are discoverable.
- Updated `CONTENT_EXECUTION_STANDARD.md` with the exact keyless Hosting dry-run and live-release commands and clarified that documentation-only work does not require a site deployment.
- Aligned the cloud runbook and session resume checklist with the startup requirements.

## Verification

- Reviewed current startup, resume, content execution, and cloud operations instructions for consistent project and wrapper selection.
- Checked changed documentation links and ran `git diff --check`.
- Both-host cloud connectivity and Hosting dry-run evidence remains in `2026-10-18-scripture-keyless-hosting-access.md`; no new IAM changes or live release were needed for this documentation update.

## Current Route

Routine cloud work uses the executing host's independent `mg-cloud-*` certificate wrappers and explicitly targets `the-way-of-scripture`. The existing operator has project-level Firebase Hosting Admin access. Scripture's Firebase project and owning account remain separate from Memory Genie.
