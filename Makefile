worker:
	celery -A taskapp --workdir=./pbb/ worker -l info -B

run:
	python manage.py runserver --settings=config.settings.development
