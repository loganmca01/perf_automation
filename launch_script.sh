#!/bin/bash

waitpid((($1)))

nohup python run_batch.py $2 &

