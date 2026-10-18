# Keyless Cloud Operations

Updated: 2026-10-18

## Required Route

Use the executing host's X.509 operator wrappers for routine Firebase and Google Cloud work on CozDev and CozPlex. Each host has its own certificate and private key. No interactive Firebase login, copied user tokens, service-account JSON keys, or forwarded CozDev credentials are required by this route.

The existing wrappers are named `mg-cloud-*` because they were commissioned with Memory Genie. They support other projects through explicit project selection. Their default is `memory-genie-ai`, so every command for this repository must explicitly select `the-way-of-scripture`.

The source operating policy is in the sibling repository:

- `/home/cozwood/Documents/Dev/memory_genie/documentation/development/KEYLESS_CLOUD_OPERATIONS.md`
- `/home/cozwood/Documents/Dev/memory_genie/documentation/planning/active/engineering/2026-09-26-direct-local-cloud-credentials.md`

## Readiness

Before cloud work, run both checks on the host that will execute the work:

```bash
~/.local/bin/mg-cloud-gcloud projects describe the-way-of-scripture \
  --project the-way-of-scripture --format='value(projectId)'
~/.local/bin/mg-cloud-firebase apps:list --project the-way-of-scripture --json
```

The first check must return exactly `the-way-of-scripture`, and the second must succeed. Wrapper existence, CLI version, or a successful check against Memory Genie does not prove access to this project.

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
| Scripture project describe through operator certificate | Permission denied | Permission denied |
| Scripture Firebase app list through operator certificate | Failed | Failed |

Both host certificates work for Memory Genie. The shared effective operator is `local-cloud-operator@memory-genie-ai.iam.gserviceaccount.com`. Its visible project list does not include `the-way-of-scripture`. Scripture deployment readiness remains blocked on project access, not an expired interactive login. No IAM grants, new credentials, or deployments were made during these checks.

The [original account-separation record](../changes/2026-06-28-github-firebase-account-separation-and-domain-setup.md) deliberately places Scripture in a separate Firebase account. Do not assume Memory Genie's operator grants cover Scripture or extend those grants without establishing the intended project identity and authority.

Use an existing keyless administrator for this project to inspect its IAM and establish the approved certificate-backed operator access. If Scripture already has a separate operator, use that project's route rather than assuming the shared identity must be granted access. Do not create or copy service-account keys or refresh an old user login to pass readiness. Once the intended project route is established, repeat both project checks and the Hosting dry run on each host.

## Failure Handling

If a certificate exchange fails, inspect and repair that host's route and check the other host's independent certificate. If certificate checks succeed for Memory Genie but Scripture access is denied, investigate project identity and IAM rather than renewing user authentication. Do not substitute bare `firebase` or `gcloud` commands for the wrappers.

The Memory Genie GitHub cloud workflows are a separately gated last resort, not routine access or a Scripture readiness probe. Do not dispatch them for this project as a workaround.
