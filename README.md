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

## Casebook export

```powershell
.\.venv\Scripts\python.exe manage.py export_casebook --output casebook_export.json
.\.venv\Scripts\python.exe manage.py export_casebook --output casebook_export.json --include-sensitive
.\.venv\Scripts\python.exe manage.py export_casebook --output casebook_export.json --include-sensitive --include-private-notes
```

## AI extension notes

- Core app lives in `casebook/`.
- Snippet model and related objects are in `casebook/models.py`.
- Export pipeline is in `casebook/management/commands/export_casebook.py`.
- Frontend list/detail/create/edit views are in `casebook/views.py` and `templates/casebook/`.
- Progress and implementation checkpoints are tracked in `implementation.md`.
