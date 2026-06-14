import os
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "LINE Greeting Bot Running"

@app.route("/webhook", methods=["POST"])
def webhook():

    body = request.json

    print("Webhook received:")
    print(body)

    events = body.get("events", [])

    for event in events:

        if event.get("type") == "memberJoined":
            print("A new member joined!")

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
