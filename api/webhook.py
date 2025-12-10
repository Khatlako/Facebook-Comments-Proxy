
import requests

app = Flask(__name__)

VERIFY_TOKEN = "YOUR_VERIFY_TOKEN"
MAKE_WEBHOOK_URL = "https://hook.eu2.make.com/m47yrjmw2h0f4w8do4am6sgr6kzccmyy"

@app.route("/api/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Verification failed", 403

    elif request.method == "POST":
        data = request.json
        print("Received payload:", data)
        
        # Forward to Make.com
        try:
            requests.post(MAKE_WEBHOOK_URL, json=data)
        except Exception as e:
            print("Error sending to Make.com:", e)
        
        return "EVENT_RECEIVED", 200
