# Gulmohar - Portfolio Casebook

Local-first Wagtail project for authoring and exporting portfolio case studies.

## PowerShell + venv setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run locally

```powershell
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py runserver
```

Admin URLs:
- Wagtail admin: `http://localhost:8000/admin/`
- Django admin: `http://localhost:8000/django-admin/`

Frontend URLs:
- Casebook index: `http://localhost:8000/casebook/`
- Case create: `http://localhost:8000/casebook/new/`
- Case detail/edit: from index links

## Add a case study

Two supported paths:

1) Snippet admin
- Go to `http://localhost:8000/admin/`
- Open **Snippets -> Case Studies**
- Fill grouped tabs (Overview, Narrative, Delivery & Production, Results, Assets, Notes)

2) Local frontend editor
- Go to `http://localhost:8000/casebook/new/`
- Fill form fields with inline related sections:
  - Assets (image or uploaded video per asset row)
  - Metrics
  - Channel spend
- Save and review on the detail page

Entry notes:
- All fields are optional for faster drafting.
- Date fields are flexible text (examples: `2024`, `January 2024`, `Q1 2025`).
- Multiple assets can be attached to the same campaign.

## Casebook export

```powershell
.\.venv\Scripts\python.exe manage.py export_casebook --output casebook_export.json
.\.venv\Scripts\python.exe manage.py export_casebook --output casebook_export.json --include-notes
```

Default export behavior:
- Includes all campaigns.
- Excludes `notes` unless `--include-notes` is provided.
- Emits image rendition URLs and uploaded-video document URLs (no binary embedding).

## Automated final acceptance test

```powershell
.\.venv\Scripts\python.exe manage.py run_casebook_final_test
```

What it does:
- Generates test images in `test_assets/`
- Seeds a fully populated lorem case with related metrics/channel spend/assets (including a video document)
- Runs `export_casebook`
- Verifies required JSON contract and notes inclusion behavior
- Writes export to `exports/final_casebook_export.json`

## AI extension notes

- Core app lives in `casebook/`.
- Snippet model and related objects are in `casebook/models.py`.
- Export pipeline is in `casebook/management/commands/export_casebook.py`.
- Frontend list/detail/create/edit views are in `casebook/views.py` and `templates/casebook/`.
- Automated acceptance command is in `casebook/management/commands/run_casebook_final_test.py`.
- Progress and implementation checkpoints are tracked in `implementation.md`.
