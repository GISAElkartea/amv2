web: waitress-serve --expose-tracebacks --port=$PORT antxetamedia.heroku.wsgi:application
worker: python manage.py collectstatic --no-input ; celery -A antxetamedia worker -O fair --loglevel=info
