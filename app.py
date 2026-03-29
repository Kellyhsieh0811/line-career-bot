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
from replies import get_reply_and_type
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

    # Check if this is the user's first message
    message_count = db.get_user(user_id)
    is_first = message_count == 0
    last_reply_type = db.get_last_reply_type(user_id) or ""
    last_conversation_goal = db.get_conversation_goal(user_id) or ""

    # Store in DB
    db.save_message(user_id, display_name, text, result.intent, result.score)

    # Build reply
    reply_text, reply_type, goal = get_reply_and_type(
        text,
        is_first=is_first,
        last_reply_type=last_reply_type,
        message_count=message_count,
        last_conversation_goal=last_conversation_goal,
    )
    if reply_type:
        db.set_last_reply_type(user_id, reply_type)
    if goal:
        db.set_conversation_goal(user_id, goal)

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
