from __future__ import print_function
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage)
from googleapiclient.discovery import build
from message import get_time_range, get_reply, get_message
import pickle
import os
import os.path
import json
import configs

app = Flask(__name__)


# 環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
creds = None

config_file = os.path.basename("configs/configs.py".split('.')[0])
config_def = eval('configs.' + config_file + '.Config')
config = config_def()


@app.route('/morning', methods=['POST'])
def morning():
    user_id = config.USERID
    try:
        if request.method == 'POST':
            data = request.data.decode('utf-8')
            data = json.loads(data)
            message = get_message(data)
            line_bot_api.push_message(user_id, TextSendMessage(text=message))
            return "OK"
    except Exception as e:
        print(e)
        return str(e)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(e):
    # for line connection test
    if e.reply_token == "00000000000000000000000000000000":
        return

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    service = build('calendar', 'v3', credentials=creds)

    text = e.message.text
    t_start, t_end, d = get_time_range(text)

    if (t_start is None) or (t_end is None):
        reply = "無効な操作です"
    else:
        events_result = service.events().list(calendarId='primary',
                                              timeMin=t_start,
                                              timeMax=t_end,
                                              singleEvents=True,
                                              orderBy='startTime').execute()

        events = events_result.get('items', [])
        reply = get_reply(events, d)

    line_bot_api.reply_message(
        e.reply_token,
        TextSendMessage(text=reply))


if __name__ == "__main__":
    # app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
