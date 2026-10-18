# Keyless Cloud Operations Correction

Date: 2026-10-18
Scope: operational documentation and cloud access verification

## Correction

The earlier CozPlex readiness assessment incorrectly treated an expired legacy Firebase user session as a deployment prerequisite. The owner's current operating model, documented in Memory Genie's `KEYLESS_CLOUD_OPERATIONS.md`, uses the executing host's independent X.509 operator certificate for routine Firebase and Google Cloud operations. Interactive login is not a readiness requirement.

## Changes

- Added `documentation/runbooks/CLOUD_OPERATIONS.md` with certificate-first operations, explicit Scripture project selection, both-host evidence, and failure handling.
- Added the cloud runbook to `SESSION_START.md` so subsequent sessions use the current route.
- Corrected `COZPLEX_HEADLESS.md`, `SESSION_RESUME.md`, and the earlier readiness record to remove the instruction to refresh Firebase login.
- Reused the existing shared host wrappers without copying credentials or modifying Memory Genie.

## Live Evidence

- CozDev and CozPlex: `mg-cloud-gcloud projects describe memory-genie-ai --project memory-genie-ai` succeeded.
- CozDev and CozPlex: `mg-cloud-firebase apps:list --project memory-genie-ai --json` succeeded.
- CozDev and CozPlex: the same certificate route returned permission denied for the `the-way-of-scripture` project describe, and the Firebase app list failed.
- The operator's visible project list does not include `the-way-of-scripture`.
- The effective identity is `local-cloud-operator@memory-genie-ai.iam.gserviceaccount.com`.

## Remaining Work

Use an existing keyless administrator for the Scripture project to inspect and establish the intended certificate-backed operator route, then repeat the two project checks and Hosting dry run on both hosts. The original setup deliberately separated Scripture's Firebase account from Memory Genie, so shared operator grants must not be assumed or expanded blindly. The Memory Genie host certificates already work; creating service-account keys or refreshing a legacy user session is not the required remedy.

No IAM changes, workflow dispatches, site regeneration, or Hosting deployments occurred. The Hosting dry run was not attempted because the project access checks failed.
