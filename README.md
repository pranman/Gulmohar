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
- Fill grouped tabs (Overview, Narrative, Delivery & Production, Results, Assets, Private)

2) Local frontend editor
- Go to `http://localhost:8000/casebook/new/`
- Fill form fields with inline related sections:
  - Assets
  - Metrics
  - Channel spend
- Save and review on the detail page

## Casebook export

```powershell
.\.venv\Scripts\python.exe manage.py export_casebook --output casebook_export.json
.\.venv\Scripts\python.exe manage.py export_casebook --output casebook_export.json --include-sensitive
.\.venv\Scripts\python.exe manage.py export_casebook --output casebook_export.json --include-sensitive --include-private
.\.venv\Scripts\python.exe manage.py export_casebook --output casebook_export.json --include-sensitive --include-private-notes
```

Default export behavior excludes:
- `status=sensitive`
- `confidentiality=private`
- `notes_private`

## Automated final acceptance test

```powershell
.\.venv\Scripts\python.exe manage.py run_casebook_final_test
```

What it does:
- Generates test images in `test_assets/`
- Seeds a fully populated lorem case with related metrics/channel spend/assets
- Runs `export_casebook`
- Verifies required JSON contract and private-note exclusion defaults
- Writes export to `exports/final_casebook_export.json`

## AI extension notes

- Core app lives in `casebook/`.
- Snippet model and related objects are in `casebook/models.py`.
- Export pipeline is in `casebook/management/commands/export_casebook.py`.
- Frontend list/detail/create/edit views are in `casebook/views.py` and `templates/casebook/`.
- Automated acceptance command is in `casebook/management/commands/run_casebook_final_test.py`.
- Progress and implementation checkpoints are tracked in `implementation.md`.
