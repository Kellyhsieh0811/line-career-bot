"""
Auto-reply templates in Traditional Chinese.
All replies are plain text to keep it human and conversational.
"""
import os
import random

BOOKING_LINK = os.getenv("BOOKING_LINK", "https://calendly.com/your-link")

# ── High intent: ready to convert ─────────────────────────────────────────────

_HIGH_REPLIES = [
    (
        "謝謝你的訊息！\n\n"
        "你可以直接用這個連結預約免費 15 分鐘的初步諮詢，"
        "我們先聊聊你的狀況，看看怎麼幫你最有效 👇\n\n"
        "{booking_link}\n\n"
        "預約後我會提前傳訊息確認，有問題也可以直接問我。"
    ),
    (
        "你好！很高興你找我諮詢 🙌\n\n"
        "先用這個連結預約時間，我們一對一談談你的情況：\n\n"
        "{booking_link}\n\n"
        "費用和服務內容我們通話時再詳細說，不用擔心。"
    ),
    (
        "收到！我們來約個時間聊聊。\n\n"
        "你可以從這裡選一個方便的時段 👇\n\n"
        "{booking_link}\n\n"
        "15 分鐘不收費，先了解你的狀況再決定要不要繼續也沒關係。"
    ),
]


def high_intent_reply() -> str:
    template = random.choice(_HIGH_REPLIES)
    return template.format(booking_link=BOOKING_LINK)


# ── Medium intent: engage and qualify ─────────────────────────────────────────

_MEDIUM_REPLIES = {
    "履歷": (
        "履歷是求職第一關，改對了面試機會差很多 💪\n\n"
        "你現在的狀況是？\n"
        "（1）履歷一直沒有面試\n"
        "（2）有面試但不多\n"
        "（3）想轉職，不確定怎麼寫\n\n"
        "跟我說你的情況，我給你更有針對性的建議。"
    ),
    "轉職": (
        "轉職是個大決定，方向對了才不會白費力氣 🎯\n\n"
        "你目前走到哪個階段了？\n"
        "（1）還在想要不要轉\n"
        "（2）已經決定轉，不知道怎麼開始\n"
        "（3）已經在投履歷，但沒什麼進展\n\n"
        "說說你的狀況，我們一起想辦法。"
    ),
    "想了解": (
        "當然可以聊聊 😊\n\n"
        "你目前最想了解的是哪個部分？\n"
        "（1）履歷怎麼寫\n"
        "（2）面試怎麼準備\n"
        "（3）薪資怎麼談\n"
        "（4）轉職方向怎麼規劃\n\n"
        "跟我說，我針對你的問題來回答。"
    ),
    "default": (
        "謝謝你的訊息！\n\n"
        "你目前遇到的最大困難是什麼？跟我說說，我看看怎麼幫你 🙌"
    ),
}


def medium_intent_reply(text: str) -> str:
    if "履歷" in text:
        return _MEDIUM_REPLIES["履歷"]
    if "轉職" in text:
        return _MEDIUM_REPLIES["轉職"]
    if "想了解" in text:
        return _MEDIUM_REPLIES["想了解"]
    return _MEDIUM_REPLIES["default"]


# ── Low intent: friendly welcome ──────────────────────────────────────────────

_LOW_REPLIES = [
    (
        "嗨！歡迎來找我 👋\n\n"
        "我是職涯諮詢師，專門幫助大家在求職、轉職、履歷、面試和薪資談判上少走冤枉路。\n\n"
        "你可以直接告訴我你現在遇到的職涯問題，我來幫你。"
    ),
    (
        "你好！很高興認識你 😊\n\n"
        "如果你正在煩惱求職、轉職或是不知道職涯下一步怎麼走，"
        "歡迎直接跟我說你的狀況，我們一起想辦法。"
    ),
]


def low_intent_reply() -> str:
    return random.choice(_LOW_REPLIES)


# ── Main dispatch ─────────────────────────────────────────────────────────────

def get_reply(intent: str, text: str) -> str:
    if intent == "HIGH":
        return high_intent_reply()
    if intent == "MEDIUM":
        return medium_intent_reply(text)
    return low_intent_reply()
