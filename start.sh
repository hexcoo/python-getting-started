#!/bin/bash
alias ll='ls -al'
service cron start
cp root /var/spool/cron/crontabs/
crontab -l
python app.py >>/usr/src/app/web_status 2>&1 &
