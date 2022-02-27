release: python manage.py migrate

web: daphne -b 0.0.0.0 -p $PORT chatAPI.asgi:application

python manage.py collectstatic --noinput
python manage.py runserver
