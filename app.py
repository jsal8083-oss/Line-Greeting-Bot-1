import os

from flask import Flask, request, abort

from linebot.v3 import WebhookHandler
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    TextMessage,
    ReplyMessageRequest
)

from linebot.v3.webhooks import MemberJoinedEvent

app = Flask(__name__)

CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")
CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")

configuration = Configuration(
    access_token=CHANNEL_ACCESS_TOKEN
)

handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/")
def home():
    return "LINE Greeting Bot Running"

@app.route("/webhook", methods=["POST"])
def webhook():

    signature = request.headers.get("X-Line-Signature")

    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except Exception as e:
        print(e)
        abort(400)

    return "OK"

@handler.add(MemberJoinedEvent)
def handle_member_join(event):

    with ApiClient(configuration) as api_client:

        line_bot_api = MessagingApi(api_client)

        welcome_text = (
            "🎉 Welcome to the INFOCHAT bulletin for MCOC related information and infographs!\n\n"
            "This chat is READ ONLY! DO NOT post in this chat unless you have been given permission!."
        )

        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[
                    TextMessage(text=welcome_text)
                ]
            )
        )

if __name__ == "__main__":
    app.run()
