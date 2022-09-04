#!/bin/bash
export REDIS_HOST
export REDIS_PASSWD
export FLASK_USER
export FLASK_PASSWD

alias ll='ls -al'
cp root /var/spool/cron/crontabs/
crontab -l
service cron start
python app.py
