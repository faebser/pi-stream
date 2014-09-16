#!/bin/bash

for pid in $(pidof -x python cloner.py); do
        if [ $pid != $$ ]; then
                echo "[$(date)] : Cloner : Process is already running with PID $pid"
                exit 1
        fi
done

echo "starting cloner"

cd /DIR/TO/CLONER

while true
do
sudo sh -c "python cloner.py"
sleep 3
done