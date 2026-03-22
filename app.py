"""
LINE Career Consulting Bot — Flask webhook server.

Endpoints:
  POST /webhook   — LINE Messaging API webhook
  GET  /health    — health check for Zeabur
"""
import os
import logging

from dotenv import load_dotenv
from flask import Flask, abort, request

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

# ── DB init (runs at import time so gunicorn workers also initialise it) ───────
import db as _db_module
_db_module.init_db()

# ── LINE SDK setup ─────────────────────────────────────────────────────────────

CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]

configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

from classifier import classify
from replies import get_reply
import db

# ── Flask app ──────────────────────────────────────────────────────────────────

app = Flask(__name__)


@app.route("/health")
def health():
    return {"status": "ok"}, 200


@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        log.warning("Invalid LINE signature")
        abort(400)

    return "OK", 200


@handler.add(MessageEvent, message=TextMessageContent)
def handle_text(event: MessageEvent):
    user_id = event.source.user_id
    text = event.message.text

    # Classify intent
    result = classify(text)
    log.info("user=%s intent=%s score=%d text=%r", user_id, result.intent, result.score, text)

    # Fetch display name (best-effort; fails gracefully without profile scope)
    display_name = _get_display_name(user_id)

    # Store in DB
    db.save_message(user_id, display_name, text, result.intent, result.score)

    # Build reply
    reply_text = get_reply(result.intent, text)

    with ApiClient(configuration) as api_client:
        api = MessagingApi(api_client)
        api.reply_message(ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text=reply_text)],
        ))


def _get_display_name(user_id: str) -> str:
    try:
        with ApiClient(configuration) as api_client:
            api = MessagingApi(api_client)
            profile = api.get_profile(user_id)
            return profile.display_name
    except Exception:
        return ""


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
