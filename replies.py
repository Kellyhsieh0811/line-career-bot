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
    "我是職涯諮詢師 凱莉，專注在金融業的中年轉職和職涯規劃。\n\n"
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
    "目前一對一職涯諮詢是 3000 / 1 小時，\n"
    "會依你的背景幫你把方向、履歷定位或面試策略整理清楚。\n\n"
    "多數人會在這個階段，把卡住的點釐清很多。\n\n"
    "如果後續有加入陪跑服務，這次費用也可以折抵。\n\n"
    "如果你願意，可以先跟我說一下你的狀況，\n"
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
    "你好！我是凱莉，做職涯諮詢的 😊\n\n"
    "如果你正在煩惱求職、轉職，或不知道職涯下一步怎麼走，\n"
    "可以先跟我說你的狀況，我會先幫你一起釐清方向。\n\n"
    "如果你希望更完整深入地討論，\n"
    "我目前有提供 1 對 1 職涯諮詢，時間是 1 小時，費用為 3000 元。\n"
    "若你後續有加入陪跑服務，這 3000 元也可以折抵。\n\n"
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
        "了解，你現在在思考職涯下一步。\n\n"
        "你目前最卡的是方向選擇、履歷，還是面試準備？"
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


# ── Reusable form CTA ──────────────────────────────────────────────────────────

_FORM_CTA = (
    "諮詢前請先填寫以下表單，讓我更了解你的背景與需求：\n"
    "👉 {form_link}"
)


def _form_cta() -> str:
    return _FORM_CTA.format(form_link=FORM_LINK)


# ── Conversation goal templates ────────────────────────────────────────────────

_GUIDE_TO_CONSULT = (
    "聽起來你現在卡的地方其實蠻關鍵的。\n\n"
    "這種情況我通常會幫你把方向、履歷或面試策略一起整理清楚，\n"
    "讓你知道現在最值得先動的是哪一步。\n\n"
    "如果你想讓討論更有效率，可以先填這份表單，\n"
    "我可以更快了解你的背景，後面也能給你更精準的建議。\n\n"
    "👉 {form_link}"
)


def guide_to_consult_reply() -> str:
    return _GUIDE_TO_CONSULT.format(form_link=FORM_LINK)

_FOLLOW_UP_NUDGE = (
    "我想幫你把這個問題想清楚，但我需要更具體的資訊。\n\n"
    "你現在最想先搞清楚的是哪一件事？\n"
    "（例如：我的履歷為什麼沒回音、我不知道要轉去哪、我不確定要不要諮詢）"
)


# ── Follow-up replies (sent when same specific intent repeats) ─────────────────

_FOLLOWUP_REPLIES = {
    "interview_urgent": (
        "你剛才提到快要面試了。\n\n"
        "現在準備到哪個階段了？還是說有特定的環節想先確認？"
    ),
    "resume_help": (
        "你剛才說履歷沒什麼回音。\n\n"
        "你現在投的是什麼樣的職缺？我可以幫你判斷是方向問題還是呈現問題。"
    ),
    "transition_confusion": (
        "你剛才說不確定方向。\n\n"
        "你現在是完全沒想法，還是有幾個選項但不確定怎麼選？"
    ),
    "service_question": (
        "你之前問過我的服務。\n\n"
        "你現在最想先釐清的是哪一塊？我可以直接針對你的狀況說明。"
    ),
    "price_question": (
        "你之前已經看過費用了。\n\n"
        "如果你願意，可以先跟我說一下你目前的背景，\n"
        "我幫你看這個方式對你有沒有幫助。"
    ),
    "high_maintenance": (
        "你之前有些顧慮，這很正常。\n\n"
        "有什麼具體的部分想先釐清嗎？"
    ),
}


# ── Conversation goal determination ───────────────────────────────────────────

def determine_goal(
    specific: str | None,
    intent: str,
    message_count: int,
    last_reply_type: str,
    last_conversation_goal: str,
) -> str:
    # follow_up_nudge: no specific topic detected, conversation has gone on too long
    if not specific and message_count >= 4:
        return "follow_up_nudge"

    # guide_to_consult: classifier HIGH + enough exchanges
    if intent == "HIGH" and message_count >= 3:
        return "guide_to_consult"
    if intent == "HIGH" and specific in ("resume_help", "transition_confusion", "interview_urgent") \
            and message_count >= 2:
        return "guide_to_consult"

    # guide_to_consult: conversation history shows enough context even without HIGH signal
    # — already discussed price or service and still engaging
    if last_reply_type in ("price_question", "service_question") and message_count >= 3:
        return "guide_to_consult"
    # — topic established (resume/direction/interview) and had back-and-forth
    if last_reply_type in ("resume_help", "transition_confusion", "interview_urgent") \
            and message_count >= 2:
        return "guide_to_consult"

    # default: collect_context — use existing specific/intent templates
    return "collect_context"


# ── Main dispatch ──────────────────────────────────────────────────────────────

def get_reply_and_type(
    text: str,
    is_first: bool = False,
    last_reply_type: str = "",
    message_count: int = 0,
    last_conversation_goal: str = "",
) -> tuple[str, str, str]:
    if is_first:
        return _FIRST_VISIT_REPLY, "first_visit", "collect_context"

    specific = _detect_specific_intent(text)
    intent = classify(text).intent
    goal = determine_goal(specific, intent, message_count, last_reply_type, last_conversation_goal)

    # guide_to_consult overrides all specific routing — always includes form link
    if goal == "guide_to_consult":
        return guide_to_consult_reply(), "guide_to_consult", goal

    # specific intent routing (with follow-up deduplication)
    if specific:
        if specific == last_reply_type and specific in _FOLLOWUP_REPLIES:
            return _FOLLOWUP_REPLIES[specific], specific, goal
        return _SPECIFIC_REPLIES[specific], specific, goal

    # generic follow_up_nudge (no specific, conversation stuck)
    if goal == "follow_up_nudge":
        return _FOLLOW_UP_NUDGE, "follow_up_nudge", goal

    # standard intent routing
    if intent == "HIGH":
        return high_intent_reply(), "high", goal
    if intent == "MEDIUM":
        return medium_intent_reply(text), "medium", goal
    return random.choice(_RETURNING_REPLIES), "low", goal


def get_reply(text: str, is_first: bool = False) -> str:
    reply, _, __ = get_reply_and_type(text, is_first=is_first)
    return reply
