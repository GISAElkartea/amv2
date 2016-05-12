web: waitress-serve --expose-tracebacks --port=$PORT antxetamedia.heroku.wsgi:application
worker: celery -A antxetamedia worker -O fair --loglevel=info
worker: python manage.py collectstatic --no-input
