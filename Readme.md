DIARY APP
===========

- $> git clone git@github.com:rollinger/diary-app.git
- $> python3 -m venv venv
- $> activate venv
- $> pip install -r requirements.txt
- $> cd diary
- $> python manage.py migrate
- $> python manage.py createsuperuser
- $> python manage.py show_urls		# Endpoints Available
- $> python manage.py runserver

API ROOT under /api/

ADMIN under /admin/

Load fixtures:
$> python manage.py loaddata diary/fixtures/dummy_data.json

Run tests:
$> pytest