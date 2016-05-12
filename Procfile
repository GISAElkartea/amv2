web: waitress-serve --expose-tracebacks --port=$PORT antxetamedia.heroku.wsgi:application
worker: celery -A antxetamedia worker -O fair --loglevel=info
clock: python manage.py collectstatic --no-input
