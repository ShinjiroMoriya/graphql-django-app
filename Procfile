release: python manage.py migrate && python manage.py createcachetable
web: gunicorn graphqlapp.wsgi --log-file -
