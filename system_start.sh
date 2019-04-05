nohup python3 origin_capture.py > origin.log 2>&1 &

sleep 10

nohup python3 system_init.py > system.log 2>&1 &

