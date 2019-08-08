#!/bin/bash

echo "Start Django."
cd /conf/webdaemon
nohup python3 manage.py runserver 0:7000 &

echo "Start AppDaemon."
cd /conf

appdaemon -c /conf

