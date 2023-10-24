#!/bin/bash
cd ./server
redis-server &
redis-cli flushall &
rq worker --with-scheduler &
python main.py