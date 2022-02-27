release: python manage.py migrate

web: daphne -b 0.0.0.0 -p $PORT chatAPI.asgi:application
worker: celery -A chatAPI worker -l INFO
beat: celery -A chatAPI beat -l INFO
chatworker: python manage.py runworker --settings=chatAPI.settings

python manage.py collectstatic --noinput
python manage.py runserver
