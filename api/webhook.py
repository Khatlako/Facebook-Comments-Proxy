import json
import requests

VERIFY_TOKEN = "YOUR_VERIFY_TOKEN"
MAKE_WEBHOOK_URL = "YOUR_MAKE_WEBHOOK_URL"

def handler(request, response):
    method = request.method

    if method == "GET":
        # Meta verification
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode and token == VERIFY_TOKEN:
            response.status_code = 200
            response.send(challenge)
        else:
            response.status_code = 403
            response.send("Verification failed")

    elif method == "POST":
        data = request.json
        print("Received payload:", data)

        # Forward to Make.com
        try:
            requests.post(MAKE_WEBHOOK_URL, json=data)
        except Exception as e:
            print("Error sending to Make.com:", e)

        response.status_code = 200
        response.send("EVENT_RECEIVED")
