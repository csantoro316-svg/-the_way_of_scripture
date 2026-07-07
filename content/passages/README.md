# Passage Sources

This directory is the canonical source of truth for generated passage pages.

## Format

- One JSON file per passage reference, named by passage slug.
- Each file stores:
  - reference metadata
  - optional section title for navigation
  - version text blocks
  - context lines
  - common interpretation lines
  - optional deeper-study links

## Rule

- Passage pages should be generated from these files.
- Study pages may still reference the same passages, but study prose is not the authoritative source for passage-page verse text.
- Standalone passage source files are also included in the library even if no study has linked to them yet.
- `_audit.json` records current translation coverage across generated passage sources.
