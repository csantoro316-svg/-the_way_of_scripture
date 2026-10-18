# Scripture Keyless Hosting Access

Date: 2026-10-18
Scope: project access verification and operational documentation

## Access Setup

The owner saved a project-level Firebase Hosting Admin (`roles/firebasehosting.admin`) grant on `the-way-of-scripture` for the existing operator, `local-cloud-operator@memory-genie-ai.iam.gserviceaccount.com`, using the account that owns Scripture's Firebase project.

The hosts reuse their existing independent X.509 certificates and `mg-cloud-*` wrappers. Scripture remains in its separate Firebase project/account. No service-account keys were created or copied, and no interactive Firebase CLI login was needed.

## Verification

These commands passed from both CozDev and CozPlex, with the Hosting command run from each host's Scripture checkout:

```bash
~/.local/bin/mg-cloud-gcloud projects describe the-way-of-scripture \
  --project the-way-of-scripture --format='value(projectId)'
~/.local/bin/mg-cloud-firebase apps:list --project the-way-of-scripture --json
~/.local/bin/mg-cloud-firebase deploy --only hosting \
  --project the-way-of-scripture --dry-run
```

Both project descriptions returned exactly `the-way-of-scripture`. Both Firebase app-list responses returned `status: success` with empty result lists. Both Hosting checks exited successfully with `Dry run complete!`.

This supersedes the project-access blocker recorded earlier in `2026-10-18-keyless-cloud-operations-correction.md`. The verified scope is Hosting and the project/app reads above, not all Firebase products or project IAM administration.

## Documentation

Updated `CLOUD_OPERATIONS.md`, `COZPLEX_HEADLESS.md`, and `SESSION_RESUME.md` with the working route and verification results. CozPlex can perform repository work and authorized Hosting deployments while CozDev is offline.

No site regeneration or live Hosting release was performed. The existing Prayer and Faith HTML/source mismatch remains documented separately and must be reconciled before regeneration.
