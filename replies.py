"""
Auto-reply templates in Traditional Chinese.
All replies are plain text to keep it human and conversational.
"""
import os
import random

from classifier import classify

FORM_LINK = os.getenv("FORM_LINK", "https://reurl.cc/dQKd5M")

# ── First visit ────────────────────────────────────────────────────────────────

_FIRST_VISIT_REPLY = (
    "嗨！歡迎來找我 👋\n\n"
    "我是職涯諮詢師，專注在金融業的中年轉職和職涯規劃。\n\n"
    "你可以直接跟我說你現在的狀況，我來幫你釐清方向。"
)

# ── Specific intent replies ────────────────────────────────────────────────────

_INTERVIEW_URGENT = (
    "聽起來你這次面試時間有點近，應該會有點壓力。\n\n"
    "這種情況其實不用準備很多，抓對幾個重點就會差很多。\n\n"
    "你這次大概是面試什麼職缺？"
)

_RESUME_HELP = (
    "看起來你已經投了一段時間，但沒有太多回音，對嗎？\n\n"
    "這種情況通常不是你不夠好，而是履歷呈現方式卡住了。\n\n"
    "你大概投了多久了？"
)

_TRANSITION_CONFUSION = (
    "這種卡住方向的感覺，其實蠻常見的，不是只有你一個人會這樣。\n\n"
    "通常不是沒有選項，而是還沒把自己整理清楚。\n\n"
    "你目前大概是在什麼產業？"
)

_SERVICE_QUESTION = (
    "我懂，你會想先確認看看是不是適合再決定，這很正常。\n\n"
    "我這邊主要是透過一對一的方式，\n"
    "幫你把目前的狀況跟下一步方向整理清楚。\n\n"
    "如果你願意，可以先跟我說一下你現在的背景或卡關點，\n"
    "我可以幫你看這樣的方式對你有沒有幫助。"
)

_PRICE_QUESTION = (
    "目前一對一職涯諮詢是 3000 元 / 1 小時，\n"
    "會根據你的背景幫你把方向、履歷定位或面試策略一起整理清楚。\n\n"
    "多數人會在這個階段，把原本卡住的方向或履歷問題釐清很多。\n\n"
    "如果後續有進一步服務，這次費用也可以折抵。\n\n"
    "如果你願意，也可以先跟我說一下你的狀況，\n"
    "我可以幫你看這樣的方式對你有沒有幫助。"
)

_HIGH_MAINTENANCE = (
    "我懂你想先多了解一些，這其實很正常。\n\n"
    "我這邊的方式會比較偏「一起把整體方向整理清楚」，\n"
    "比較不是零散的一題一題回答。\n\n"
    "如果你現在只是想先看看資訊，其實也很好，\n"
    "只是可能還不一定需要到這一步。\n\n"
    "如果你希望有人直接幫你判斷方向，我再幫你一起看。"
)

# ── High intent (service/form) ─────────────────────────────────────────────────

_HIGH_REPLY = (
    "你好！很高興認識你 😊\n\n"
    "如果你正在煩惱求職、轉職，或不知道職涯下一步怎麼走，\n"
    "可以先跟我說你的狀況，我會先幫你一起釐清方向。\n\n"
    "如果你希望更完整深入地討論，\n"
    "我目前有提供 1 對 1 職涯諮詢，時間是 1 小時，費用為 3000 元。\n"
    "若你後續有進一步報名陪跑方案，這 3000 元也可以折抵。\n\n"
    "如果你想先讓我更了解你的背景，\n"
    "可以先填這份表單 👉 {form_link}\n\n"
    "我會再根據你的狀況，跟你說明下一步怎麼安排比較適合。"
)


def high_intent_reply() -> str:
    return _HIGH_REPLY.format(form_link=FORM_LINK)


# ── Medium intent ──────────────────────────────────────────────────────────────

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


# ── Returning low intent ───────────────────────────────────────────────────────

_RETURNING_REPLIES = [
    "你好～可以直接跟我說你目前的狀況（轉職 / 履歷 / 面試都可以）\n\n我可以幫你一起看下一步怎麼走。",
]


# ── Specific intent detection (keyword-based) ──────────────────────────────────

def _detect_specific_intent(text: str) -> str | None:
    # 1. price_question — checked first (clearest signal)
    if any(k in text for k in ["多少", "價格", "收費", "費用"]):
        return "price_question"

    # 2. interview_urgent — "面試" + any time word
    if "面試" in text and any(k in text for k in ["今天", "明天", "後天", "下週", "這週", "快", "即將"]):
        return "interview_urgent"

    # 3. resume_help — resume or application with no response
    if any(k in text for k in ["履歷", "石沉大海", "沒回音", "沒有回音", "面試少"]) or \
       ("投" in text and any(k in text for k in ["沒回", "沒有回", "沒反應", "石沉"])):
        return "resume_help"

    # 4. transition_confusion — uncertainty + career context
    if any(k in text for k in ["不知道", "不確定", "迷茫"]) and \
       any(k in text for k in ["工作", "產業", "銀行", "保險", "券商", "做", "待", "年"]):
        return "transition_confusion"

    # 5. service_question — asking about what help is available
    if any(k in text for k in ["服務", "怎麼幫", "你做什麼", "可以幫我", "有案例", "先幫我看", "先給我看"]):
        return "service_question"

    # 6. high_maintenance — strong negative or resistant signals only
    if any(k in text for k in ["太貴", "不值得", "沒用", "騙", "不需要"]):
        return "high_maintenance"

    return None


_SPECIFIC_REPLIES = {
    "interview_urgent":    _INTERVIEW_URGENT,
    "resume_help":         _RESUME_HELP,
    "transition_confusion": _TRANSITION_CONFUSION,
    "service_question":    _SERVICE_QUESTION,
    "price_question":      _PRICE_QUESTION,
    "high_maintenance":    _HIGH_MAINTENANCE,
}


# ── Main dispatch ──────────────────────────────────────────────────────────────

def get_reply(text: str, is_first: bool = False) -> str:
    if is_first:
        return _FIRST_VISIT_REPLY

    specific = _detect_specific_intent(text)
    if specific:
        return _SPECIFIC_REPLIES[specific]

    intent = classify(text).intent
    if intent == "HIGH":
        return high_intent_reply()
    if intent == "MEDIUM":
        return medium_intent_reply(text)
    return random.choice(_RETURNING_REPLIES)
