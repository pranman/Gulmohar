# Implementation Tracker

## Status overview

- Public UX Refresh Phase A (schema optional + text dates + video assets): complete
- Public UX Refresh Phase B (admin/forms flow): complete
- Public UX Refresh Phase C (Bulma template redesign): complete
- Public UX Refresh Phase D (export contract update): complete
- Public UX Refresh Phase E (validation + automation): complete
- Public UX Refresh Phase F (docs + checkpoints): complete

## Current step

Implementing requested v2 workflow changes: organization/industry dropdowns, sector field, campaign delete actions, and addable table UX for related rows.

## Validation results (refresh run)

- `manage.py makemigrations casebook`: generated `0002_remove_casestudy_notes_private_caseasset_video_and_more.py`.
- `manage.py migrate`: passed.
- `manage.py check`: passed.
- `manage.py export_casebook --output exports/casebook_export_public_refresh.json --include-notes`: passed.
- `manage.py run_casebook_final_test --output exports/final_casebook_export.json`: passed.
- Browser validation (localhost):
  - index/create/detail pages load.
  - flexible text dates accepted.
  - image + video asset fields present.
  - lightweight campaign submit/edit flow passes.
- v2 delta validation:
  - `manage.py makemigrations casebook`: generated `0003_industry_organization_remove_casestudy_client_or_org_and_more.py`.
  - `manage.py migrate`: passed.
  - `manage.py check`: passed.

## Git checkpoints (refresh run)

- Checkpoint R1 complete:
  - Commit: `07d5fff`
  - Scope: schema + migration + core export/media model alignment
  - Push: `main` updated on origin
- Checkpoint R2 complete:
  - Commit: `cd2d28a`
  - Scope: admin/frontend flow improvements + Bulma redesign
  - Push: `main` updated on origin
- Checkpoint R3 complete:
  - Commit: `c0a0eb9`
  - Scope: validation outputs + docs completion for public UX refresh
  - Push: `main` updated on origin
- Checkpoint V2-R1 pending:
  - Scope: organization/industry models, sector field, campaign delete route, and related UI/filter updates
