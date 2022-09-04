import redis
import requests
import logging
import logging.handlers
import signal
import sys

#Init remove redis conn for publish
_host = os.getenv('REDIS_HOST')
_port = 12906
_user = 'outline'
_passwd = os.getenv('REDIS_PASSWD')

#日志文件
LOG_FILENAME = 'rebalancing.log'

#telegram
_tghost = 'api.telegram.org'
_tgbot_token = '2038956431:AAGIpP3DSy3q1EM58lDlHwvcgSzbcZMu7fw'
_tg_chat_id = '-1001710535265'

_slack_host = os.getenv('SLACK_HOOK')
_slack_channel = "#notice_cube"

# Telegram Bot Push https://core.telegram.org/bots/api#authorizing-your-bot
def telegram(msg):
    data = (
        ('chat_id', _tg_chat_id),
        ('text','msg from okteto\n' + msg + '\n\n' + '')
    )
    print('https://' + _tghost + '/bot' + _tgbot_token + '/sendMessage')
    response = requests.get('https://' + _tghost + '/bot' + _tgbot_token + '/sendMessage', params=data)
    if response.status_code != 200:
        print('Telegram Bot 推送失败')
    else:
        print('Telegram Bot success')

def slack_send(channel, msg):
    data = {
        "channel": channel,
        "username":"okteto-test",
        "text": msg + "\n\n" ,
        "icon_emoji": ":moneybag:"
    }
    print(_slack_host)
    response = requests.post(_slack_host, json=data)
    if response.status_code != 200:
        print(response.text)
        print('Slack failure')
    else:
        print('Slack  success')

def set_logger():
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILENAME, maxBytes=10485760, backupCount=2, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

def term_sig_handler(signum, frame):
    term_str = "listener is offline"
    if signum == 2:
        telegram(term_str)
        sys.exit()

logger = logging.getLogger()
set_logger()

online_str = "listener is online"
telegram(online_str)

signal.signal(signal.SIGINT, term_sig_handler)     #ctrl +c  use kill -2

rc = redis.StrictRedis(host=_host, port=_port, charset="utf-8", decode_responses=True)
rc.auth(_passwd, _user)
sub = rc.pubsub()
sub.subscribe('xq_cube')
try:
    for msg in sub.listen():
        if msg is not None and isinstance(msg, dict) and msg["type"]=="message":
            telegram(msg["data"])
            slack_send(_slack_channel, msg["data"])
            logger.info(msg["data"])
except Exception as e:
    import traceback
    print(traceback.format_exc())
    telegram(traceback.format_exc())
