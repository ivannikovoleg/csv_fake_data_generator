web: gunicorn csv_data_generator.wsgi --log-file -
celery: celery -A csv_data_generator worker -B --loglevel=info