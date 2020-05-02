export FLASK_APP=app
old_pid=$(ps ax|grep flask|grep -v grep|awk '{print $1}')
echo "old_pid=${old_pid}"
if [ -z $old_pid ];then
    echo "Process Non-existent !"
else
    kill -9 ${old_pid}
    mid_pid=$(ps ax|grep flask|grep -v grep|awk '{print $1}')
    if [ -z ${mid_pid} ];then
        echo "Process Close Success !"
    else
        echo "Process Close Fail !"
        exit 1
    fi
fi
echo "Starting Process...."
nohup python -m flask run --port 9999
new_pid=$(ps ax|grep flask|grep -v grep|awk '{print $1}')
if [ -z ${new_pid} ];then
    echo "Restart Fail !"
else
    echo "Restart Success !"
    echo "new_pid=${new_pid}"
fi