# Bible Study Site Plan

**Date:** 2026-06-28

## Repository Approach

- Keep this project in a separate Git repository from `memory_genie`.
- A good local layout is:
  - `memory_genie/`
  - `bible-study-site/`
- It is fine to open work from a parent directory containing both repos so existing Memory Genie patterns can be referenced without mixing code or git history.

## Content Model Direction

- Use two primary content types:
  - Topic pages
  - Passage pages
- Topic pages should cover subjects like prayer, faith, and study questions.
- Passage pages should provide the standalone deep dive and context for any scripture referenced by a topic page.
- Cross-link both ways:
  - Topic pages list related passages.
  - Passage pages list related topics/studies.

## Platform Direction

- Preferred direction: static-site generator hosted on Firebase Hosting.
- Current recommendation is a static content architecture rather than a full app architecture.
- This keeps cost and complexity low while leaving room for future growth.

## Project Identity

- Project folder created at:
  - `/home/cozwood/Documents/Dev/the_way_of_scripture`
- Selected site and channel name:
  - `The Way of Scripture`
- Purchased primary domain:
  - `thewayofscripture.com`
- Domain wording intentionally keeps `Scripture` singular.
- The decision was to keep `the` in the primary domain so the website exactly matches the channel/brand name.

## Firebase Plan Decision

- `Spark` = no-cost plan with hard limits.
- `Blaze` = pay-as-you-go with a billing account attached.
- Based on the discussion, `Blaze` is the preferred default for this project.

Why `Blaze`:

- No flat monthly Firebase fee just for having the project.
- Small static-site usage may still cost effectively nothing.
- If usage grows past included no-cost limits, the site can continue instead of hard-stopping.
- It leaves room for future backend features without having to rethink the hosting plan first.

## Hosting Notes

- Firebase Hosting is a good fit for this project.
- For a mostly text static site, the included Hosting transfer allowance is substantial.
- A text-first site is unlikely to incur meaningful Hosting cost unless traffic becomes much larger.

## SSL / Certificate Notes

- If this site uses Firebase Hosting with a custom domain, Firebase automatically provisions and manages the SSL certificate.
- This means there is usually no need to separately buy an SSL certificate from a registrar like GoDaddy.
- Firebase documentation says custom domains are connected through Firebase Hosting and SSL is provisioned as part of that flow.
- DNS must be pointed correctly for provisioning to succeed, and Firebase notes certificate provisioning can take up to 24 hours, though it often completes sooner.

Practical implication:

- Buy the domain from the registrar you want.
- Point DNS to Firebase Hosting when ready.
- Let Firebase manage the certificate lifecycle.
- Avoid paying separately for a commercial SSL certificate unless a non-Firebase hosting scenario later requires it.

Registrar choice currently in use:

- Domain was purchased through `Squarespace`.
- Planned setup remains:
  - `Squarespace` for domain registration/DNS
  - `Firebase Hosting` for site hosting
  - Firebase-managed SSL for HTTPS

## Certificate Lifetime Context

- Let’s Encrypt currently issues default certificates valid for 90 days.
- Let’s Encrypt also announced that certificate lifetimes will decrease over time, aligning with broader CA/Browser Forum changes.
- Because of this industry direction, automated certificate management is preferable to manual certificate purchasing and renewal.
- Firebase-managed certificates fit that preference well because Firebase handles provisioning and renewal for the hosted custom domain.

## Next Step

- Domain has been purchased.
- Next working session should open from `/home/cozwood/Documents/Dev` so both repositories can be visible:
  - `memory_genie/`
  - `the_way_of_scripture/`
- Once resumed, continue with:
  - repo setup
  - stack choice
  - initial site structure
  - Firebase project + Hosting setup
  - domain connection

## Reference Sources

- Firebase custom domain setup: https://firebase.google.com/docs/hosting/custom-domain
- Firebase Hosting overview: https://firebase.google.com/docs/hosting
- Firebase pricing: https://firebase.google.com/pricing
- Firebase pricing plans: https://firebase.google.com/docs/projects/billing/firebase-pricing-plans
- Let’s Encrypt FAQ: https://letsencrypt.org/docs/faq/
- Let’s Encrypt certificate lifetime update: https://letsencrypt.org/2025/12/02/from-90-to-45
