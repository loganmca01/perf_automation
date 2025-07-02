#!/bin/bash

while true; do

	if kill -0 "$1" &> /dev/null; then
		sleep 120
	else
		break
	fi

done

nohup python run_batch.py $2 &

