import os
#import pydevd_pycharm
import time
from datetime import datetime
from flask import Flask
from flask import request
from flask_basicauth import BasicAuth
import requests
import redis
import json
import re
import subprocess

file_path = '/usr/src/app/test'
#Init remove redis conn for publish
_host = os.getenv('REDIS_HOST')
_port = 12906
_user = 'outside'
_passwd = os.getenv('REDIS_PASSWD')

#new auth
redis_uri = "redis://" + _user + ":" + _passwd + "@" + _host + ":12906"
r = redis.from_url(redis_uri)
r.execute_command("AUTH " + _user +" " + _passwd)
aadToken = r.get('mail_access_token')
str_aadToken = aadToken.decode('utf-8')

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = os.getenv('FLASK_USER')
app.config['BASIC_AUTH_PASSWORD'] = os.getenv('FLASK_PASSWD')

print("user: " + os.getenv('FLASK_USER'))
print("passwd: " + os.getenv('FLASK_PASSWD'))
basiccauth = BasicAuth(app)
@app.route('/')
def hello_world():
    msg = 'this server is worked!'
    return msg

@app.route('/helo')
def check_run():
    if os.path.exists(file_path):
        stats_info = os.stat(file_path)
        st_mtime = stats_info.st_mtime
        last_update = datetime.fromtimestamp(st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        msg = 'last run in: ' + last_update
        return msg
    else:
        return 'check cron'
"""
@app.route('/start', methods=['GET'])
@basiccauth.required
def start():
    if not request.args.get("str"):
        return "no args"
    shell_str = request.args["str"]
    #import subprocess
    new_env = os.environ.copy()
    os.system(shell_str)
    #cmd_str = 'python notice.py &'
    chk_str = "ps -ef|grep notic|grep -v grep|awk '{print $2}'"
    pid = "no"
    #subprocess.Popen(cmd_str, env=new_env)
    #pid = os.popen(chk_str)
    #print(pid)
    return 'ok'

@app.route('/stop', methods=['GET'])
@basiccauth.required
def stop():
    chk_str = "ps -ef|grep notic|grep -v grep|awk '{print $2}'"
    pid = "11111"
    pid = os.popen(chk_str)
    cmd_str = 'kill -9 ' + pid
    os.system(cmd_str)
    return 'ok'
"""
@app.route('/check_mail', methods=['GET'])
@basiccauth.required
def check_mail():
    global aadToken
    page = 1

    if not request.args.get("s"):
        return "no args"
    search_str = request.args["s"]
    if search_str=='':
        return "no args"
    if request.args.get("p"):
        page = int(request.args["p"])
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': "Bearer " + str_aadToken
        }

    api_root = "https://graph.microsoft.com/v1.0/"
    tmp_sub = {}
    tmp_html = "no result"
    if aadToken == None:
            return "Access token acquired."
    query_url = api_root + "me/messages?$search=" + search_str
    res = requests.get(query_url, headers=headers)
    
    resp = json.loads(res.text)
    if res.status_code != 200:
        #update token
        aadToken = r.get('mail_access_token')
        str_aadToken = aadToken.decode('utf-8')
        return "retry, get outlook mail error code: "  +  resp["error"]["code"]

    result = resp["value"]
    count = len(result)
    
    for i in range(count):
        sender = result[i]["sender"]["emailAddress"]["address"]
        send_date = result[i]["createdDateTime"]
        subject = result[i]["subject"]
        print(str(i) + ": page: " + str(page-1) + ": " + send_date + " : " + sender + ": " + subject)
        #tmp_sub.append(resp[i]["subject"])
        
        if re.search(search_str, sender):
            tmp_sub[result[i]["subject"]]=result[i]["body"]["content"]  #["createdDateTime"]
            tmp_html = result[i]["body"]["content"]

            if int(page - 1) == i:
                break
        else:
            page = page + 1
        '''
        if result[i]["body"]["contentType"] == "html":
            tmp_html = result[i]["body"]["content"]
            break
        '''

    #return json.dumps(result)
    return str(count) + tmp_html

@app.route('/quit')
def app_quit():
    exit()
    
def attach():
  if os.environ.get('WERKZEUG_RUN_MAIN'):
    print('Connecting to debugger...')
    #pydevd_pycharm.settrace('0.0.0.0', port=9000, stdoutToServer=True, stderrToServer=True)

if __name__ == '__main__':
  print('Starting hello-world server...')
  # comment out to use Pycharm's remote debugger
  # attach()

  app.run(host='0.0.0.0', port=8080)
