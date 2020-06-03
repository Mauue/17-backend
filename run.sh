git pull
cat uwsgi.pid|xargs kill -9
sleep 5
uwsgi uwsgi.ini