#!/bin/bash
export REDIS_HOST
export REDIS_PASSWD
export FLASK_USER
export FLASK_PASSWD

alias ll='ls -al'
ps -ef|grep cron
crontab -l
python app.py
