worker:
	celery -A taskapp --workdir=./pbb/ worker -l info -B

run:
	python pbb/manage.py runserver --settings=settings.development
