# PRD: Portfolio Casebook (Wagtail)

## Product goal

Build a Wagtail app named `casebook` to capture detailed case studies with narrative fields, assets, spend, metrics, taxonomy, status controls, and one-command JSON export for LLM workflows.

## Core requirements

- Case study storage via Wagtail snippet model.
- Structured narrative fields and operational metadata.
- Related assets (image-backed), metrics, and optional channel spend records.
- Tagging and ordering support.
- Admin-first editing with clean grouped UI and inline child editing.
- Localhost frontend experience (v1 private/local use) with clear field guidance.
- Management command export with policy-aware filtering:
  - Exclude `status=sensitive` by default.
  - Exclude `confidentiality=private` by default.
  - Exclude private notes unless explicitly requested.
- Export should include URLs only for images (original + key renditions), no binaries.

## Acceptance criteria

- `casebook` app exists with models, migrations, and snippet registration.
- Admin supports search/filter/list columns and inline editing.
- Frontend allows localhost interaction with records.
- `export_casebook` command emits valid JSON matching required schema.
- Final automated test run creates test data, attaches images, and produces successful export without manual intervention.
