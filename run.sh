git pull
ps -A|grep flask|xargs kill -9
nohup flask run --host 0.0.0.0 --port 9999 &