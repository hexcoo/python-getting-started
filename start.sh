#!/bin/bash
export REDIS_HOST
export REDIS_PASSWD
export FLASK_USER
export FLASK_PASSWD

alias ll='ls -al'
service cron start
crontab -l
ps -ef|grep cron
python app.py
