#!/bin/bash
cd ./server
redis-server &
rq worker --with-scheduler &
python main.py