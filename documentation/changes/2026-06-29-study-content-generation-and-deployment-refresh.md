# Study Content Generation and Deployment Refresh

Date: 2026-06-29
Scope: website | content

## Summary

- Updated the study-generation workflow so study hero intros and library study-card copy stay aligned without duplicating the same intro again in the study body.
- Expanded generated passage coverage for newly added and newly linked references, including reciprocal study-to-passage relationships on public pages and in the library index.
- Added and integrated new study content for `worship` and `i_am_a_disciple`, and revised existing studies including `prayer_and_faith`, `seek_signs`, `true_church`, and `what_does_prayer_look_like`.
- Adjusted featured study-card layout styling so the main studies surface presents featured cards in a two-column desktop grid.
- Updated `documentation/architecture/CONTENT_EXECUTION_STANDARD.md` to reflect the durable workflow rules added during execution, including intro handling, associated-passage expectations, and deploy-on-completion requirements for public site changes.

## Why

- Study-card summaries had drifted from the actual study intros, and some study pages were duplicating the same introductory content in both the hero and the body.
- New and revised study material required broader passage-page generation so linked references remained navigable and kept study backlinks current.
- The content workflow changed in durable ways during implementation, so the architecture documentation needed to be brought in line with actual operating practice.
- Public site changes were being treated as complete only after regeneration, verification, and Firebase hosting deployment, which is now an explicit standard rather than an implicit habit.

## Notes

- Verification completed with `python3 -m py_compile tools/generate_study_pages.py` and `python3 tools/generate_study_pages.py`.
- Public site state was deployed to Firebase hosting at `https://the-way-of-scripture.web.app`.
- This change record covers the current uncommitted website/content batch visible in the working tree, including generated study and passage output.
