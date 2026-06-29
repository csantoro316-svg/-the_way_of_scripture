# GitHub Firebase Account Separation And Domain Setup

Date: 2026-06-28
Scope: repo

## Summary

- Repointed this repository away from the mistakenly created `cozwoodiov` GitHub remote.
- Configured a dedicated SSH key and SSH host alias so this repo now pushes to `csantoro316-svg/-the_way_of_scripture` without affecting other repos on the machine.
- Repointed Firebase away from the wrong project and bound the repo to the new project `the-way-of-scripture`.
- Deployed the site successfully to `https://the-way-of-scripture.web.app`.
- Began custom-domain setup for `thewayofscripture.com` and updated DNS to the Firebase apex target and verification TXT record.

## Why

- This website needed to be isolated from the Memory Genie GitHub and Firebase accounts.
- Per-repo GitHub separation required SSH because the machine still needs to keep other repos on their existing identity.
- Firebase Hosting remains the correct deployment surface for the current static site.

## Notes

- The repo remote now uses the SSH alias `github-csantoro316-svg`.
- `.firebaserc` now maps the default project to `the-way-of-scripture`.
- Public DNS for `thewayofscripture.com` now resolves to Firebase Hosting, but Firebase custom-domain verification was still catching up at the end of the session.
