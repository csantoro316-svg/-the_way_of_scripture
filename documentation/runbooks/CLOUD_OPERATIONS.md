# Keyless Cloud Operations

Updated: 2026-10-18

## Required Route

Use the executing host's X.509 operator wrappers for routine Firebase and Google Cloud work on CozDev and CozPlex. Each host has its own certificate and private key. No interactive Firebase login, copied user tokens, service-account JSON keys, or forwarded CozDev credentials are required by this route.

The existing wrappers are named `mg-cloud-*` because they were commissioned with Memory Genie. They support other projects through explicit project selection. Their default is `memory-genie-ai`, so every command for this repository must explicitly select `the-way-of-scripture`.

The source operating policy is in the sibling repository:

- `/home/cozwood/Documents/Dev/memory_genie/documentation/development/KEYLESS_CLOUD_OPERATIONS.md`
- `/home/cozwood/Documents/Dev/memory_genie/documentation/planning/active/engineering/2026-09-26-direct-local-cloud-credentials.md`

## Readiness

At session start, run both read-only checks on the active host. Repeat them on another host before its first cloud operation when switching hosts:

```bash
~/.local/bin/mg-cloud-gcloud projects describe the-way-of-scripture \
  --project the-way-of-scripture --format='value(projectId)'
~/.local/bin/mg-cloud-firebase apps:list --project the-way-of-scripture --json
```

The first check must return exactly `the-way-of-scripture`, and the second must succeed. Wrapper existence, CLI version, or a successful check against Memory Genie does not prove access to this project.

Record the executing host, target project, and both outcomes in the session assessment. A failed check is a readiness issue to investigate through the failure-handling section below, not a reason to refresh an obsolete user login. These checks do not publish a release.

After project access passes, validate a deployment from this repository without publishing:

```bash
~/.local/bin/mg-cloud-firebase deploy --only hosting \
  --project the-way-of-scripture --dry-run
```

An authorized Hosting deployment uses the same command without `--dry-run`, after the ordinary content, verification, and release checks.

For a reviewed SDK script, select the project before the process-scoped wrapper:

```bash
MG_CLOUD_PROJECT=the-way-of-scripture ~/.local/bin/mg-cloud-run node path/to/reviewed-script.js
```

The script must use the supplied certificate-backed ADC rather than reading a Firebase user-token store or overriding credentials internally. Never print tokens, private keys, or credential-file contents.

## Current Verification

Observed on 2026-10-18:

| Check | CozDev | CozPlex |
| --- | --- | --- |
| Memory Genie project describe through operator certificate | Passed | Passed |
| Memory Genie Firebase app list through operator certificate | Passed | Passed |
| Scripture project describe through operator certificate | Passed | Passed |
| Scripture Firebase app list through operator certificate | Passed | Passed |
| Scripture Hosting deployment dry run | Passed | Passed |

The owner granted `local-cloud-operator@memory-genie-ai.iam.gserviceaccount.com` the `roles/firebasehosting.admin` role on `the-way-of-scripture`. Both hosts subsequently returned the exact Scripture project ID and successful Firebase app-list responses. Both app-list requests returned empty lists successfully. Hosting dry runs passed on both hosts. No live Hosting release was published during verification.

The [original account-separation record](../changes/2026-06-28-github-firebase-account-separation-and-domain-setup.md) deliberately places Scripture in a separate Firebase account. That project and its ownership remain separate. The approved project-level Hosting role lets the existing operator certificates manage this site's Hosting resources. It does not grant this operator project Owner or IAM administration in Scripture.

Reuse the existing host-local certificate wrappers with explicit Scripture project selection. No new certificate setup, copied credentials, or interactive Firebase login is needed for the verified route. Other Firebase products or project administration require their own task-specific access assessment.

## Failure Handling

If a certificate exchange fails, inspect and repair that host's route and check the other host's independent certificate. If certificate checks succeed for Memory Genie but Scripture access is denied, investigate project identity and IAM rather than renewing user authentication. Do not substitute bare `firebase` or `gcloud` commands for the wrappers.

The Memory Genie GitHub cloud workflows are a separately gated last resort, not routine access or a Scripture readiness probe. Do not dispatch them for this project as a workaround.
