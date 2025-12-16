# Ward-Based Waste Management (Django)

This repository contains a starter scaffold for the Ward-Based Waste Management System described in the master prompt.

## Quickstart

1. Create a virtualenv and install requirements

   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

2. Run migrations and create a superuser

   python manage.py migrate
   python manage.py createsuperuser

3. Run server

   python manage.py runserver

## Next steps

- Finish polishing views, forms, templates for `accounts`, `users`, `workers`, `waste` and `payments` apps
- Use management command to generate bills: `python manage.py generate_monthly_bills --year 2025 --month 12`
- Invoice generation (HTML + optional PDF) available at `/payments/invoice/<id>/?pdf=1` if `xhtml2pdf` is installed
- Run `python manage.py generate_monthly_bills --year 2025 --month 12` to generate invoices (emails sent if email backend is configured)
- Tests: run `python manage.py test` to execute unit tests for billing, pickup, worker verification, and payments
- Configure production settings (DEBUG=False) and a robust DB (Postgres)
