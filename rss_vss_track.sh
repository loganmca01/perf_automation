#!/bin/bash

rss=0
vsz=0

while true; do

	if kill -0 "$1" &> /dev/null; then
		tmp = ps -o rss,vsz -p "$1"
		i=0
		for x in $tmp
		do
			if 
	else
		break
	fi

done

