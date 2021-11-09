#! /bin/sh


sleep 5


rm -r static/*


python3 manage.py migrate


python3 manage.py loaddata fixtures/initial_data.json


python3 manage.py collectstatic --no-input


gunicorn solution_factory_project.wsgi:application -b 0.0.0.0:8000 --reload
