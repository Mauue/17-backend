git pull
cat uwsgi.pid|xargs kill -9
uwsgi uwsgi.ini