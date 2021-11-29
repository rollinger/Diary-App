Worklog App
===========

- $> git clone git@github.com:rollinger/worklog-app.git
- $> python3 -m venv venv
- $> activate venv
- $> pip install -r requirements.txt
- $> cd worklog
- $> python manage.py migrate
- $> python manage.py createsuperuser
- $> python manage.py show_urls		# Endpoints Available
- $> python manage.py runserver

API ROOT under /api/

ADMIN under /admin/

Load fixtures:
$> python manage.py loaddata worklog/fixtures/dummy_data.json

Prefab User:
jimmy::JrS5S4hYrTiKjtx (normal user)
cian::jrS5S4hYrTiKjtx (admin)
georg::jrS5S4hYrTiKjtX (admin)


Run tests:
$> pytest