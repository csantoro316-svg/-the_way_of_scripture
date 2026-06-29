# Repo Git And Firebase Setup

Date: 2026-06-28
Scope: repo

## Summary

- Initialized the repository as a local git repo on the `main` branch.
- Created the GitHub remote repository `cozwoodiov/the_way_of_scripture` and connected it as `origin`.
- Added `.gitignore` for Firebase local artifacts and common OS noise.
- Added Firebase Hosting configuration with `apps/web/` as the publish directory.
- Created and linked the Firebase project `the-way-of-scripture-site`.
- Verified a successful initial Hosting deploy.

## Why

- The project needed source control and a deploy target before continued website work.
- The current website is a static site, so Firebase Hosting is the simplest matching first deployment surface.

## Notes

- Hosting is currently deployed from `apps/web/`.
- Live site URL: `https://the-way-of-scripture-site.web.app`
