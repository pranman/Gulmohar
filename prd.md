# PRD: Portfolio Casebook (Wagtail)

## Product goal

Build a Wagtail app named `casebook` to capture detailed case studies with narrative fields, assets, spend, metrics, taxonomy, status controls, and one-command JSON export for LLM workflows.

## Core requirements

- Case study storage via Wagtail snippet model.
- Structured narrative fields and operational metadata.
- Related assets (images and uploaded videos), metrics, and optional channel spend records.
- Tagging and ordering support.
- Organization and industry are managed as reusable dropdown entities.
- Campaign status/confidentiality fields are removed in favor of portfolio-first public data capture.
- Admin-first editing with clean grouped UI and inline child editing.
- Localhost frontend experience with clear field guidance and portfolio-first usability.
- Flexible text dates are allowed across campaigns/assets (e.g. `2024`, `January 2024`).
- All campaign fields are optional for fast drafting.
- Management command export should include all campaigns by default in this public portfolio workflow.
- Export should include URLs only for media references (images/video documents), no binaries.

## Acceptance criteria

- `casebook` app exists with models, migrations, and snippet registration.
- Admin supports search/filter/list columns and inline editing.
- Frontend allows localhost interaction with records, including create/edit for case studies and related entities.
- Frontend case list supports per-row campaign deletion (including related records).
- Assets, metrics, and channel spend use tabular add/remove rows with explicit add and delete controls.
- `export_casebook` command emits valid JSON matching required schema.
- Export command supports optional note inclusion and media-aware asset payloads.
- Final automated test run creates test data, attaches images, and produces successful export without manual intervention.
