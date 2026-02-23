# Implementation Tracker

## Status overview

- Phase 1 - Project bootstrap and hygiene: complete
- Phase 2 - Casebook data models: complete
- Phase 3 - Wagtail admin UX: complete
- Phase 4 - Local frontend UX: complete
- Phase 5 - Export command: complete
- Phase 6 - Migrations, validation, docs: complete

## Current step

All planned phases implemented. Finalizing last checkpoint commit/push.

## Validation results

- `manage.py check`: passed.
- `manage.py makemigrations casebook`: generated `casebook/migrations/0001_initial.py`.
- `manage.py migrate`: passed.
- Browser/local validation:
  - `/casebook/`, `/casebook/new/`, and case detail pages load successfully.
  - Create/edit flow verified (including one-liner update persistence).
  - Media-backed assets render from local `media/` URLs.
- Export validation:
  - `export_casebook` ran with default and policy flags.
  - JSON shape verified (`generated_at`, `count`, `cases`).
  - `notes_private` excluded by default and included only with `--include-private-notes`.
- Final automated acceptance:
  - `manage.py run_casebook_final_test` succeeded.
  - Output: `exports/final_casebook_export.json`.

## Git checkpoints

- Checkpoint 1 complete:
  - Commit: `b2a545f`
  - Scope: Wagtail scaffold + baseline docs/hygiene
  - Push: `main` updated on origin
- Checkpoint 2 complete:
  - Commit: `297e428`
  - Scope: casebook models/admin/frontend/export integration + migrations
  - Push: `main` updated on origin
- Checkpoint 3 pending:
  - Scope: automated final test, export verification outputs, docs finalization
