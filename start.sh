nohup python3 delete_log.py >> delete_log.out &
nohup /usr/local/bin/gunicorn -w 12 -b 0.0.0.0:8888 web:app >> web.out &
