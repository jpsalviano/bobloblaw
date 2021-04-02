install:
	pip install -r requirements.dev

run:
	python manage.py runserver

test:
	python manage.py test