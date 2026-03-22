"""
Keyword-based intent classifier for LINE messages.

Intent levels:
  HIGH   — ready to book or asking about price/services
  MEDIUM — curious about career topics, warming up
  LOW    — greeting, off-topic, or unclear
"""
import re
from dataclasses import dataclass
from typing import Literal

IntentLevel = Literal["HIGH", "MEDIUM", "LOW"]

# (pattern, score) — higher score = stronger signal
_HIGH: list[tuple[str, int]] = [
    (r"預約", 10),
    (r"費用|收費|多少錢|價格", 10),
    (r"想(諮詢|合作|請教|了解).*(履歷|轉職|面試|薪資|職涯)", 9),
    (r"(履歷|轉職|面試|薪資|職涯).*(諮詢|了解|請教)", 9),
    (r"怎麼(找你|聯絡|預約)", 8),
    (r"有(提供|開|什麼)(諮詢|課程|服務)", 8),
    (r"想(找人|請人)(幫|看|協助)", 7),
    (r"一對一", 7),
]

_MEDIUM: list[tuple[str, int]] = [
    (r"想了解", 5),
    (r"履歷", 4),
    (r"轉職", 4),
    (r"面試", 3),
    (r"薪資|薪水|加薪", 3),
    (r"職涯|職場|工作", 3),
    (r"求職|找工作", 4),
    (r"怎麼(寫|準備|提升)", 3),
    (r"有沒有(建議|方法|技巧)", 3),
]


@dataclass
class IntentResult:
    text: str
    intent: IntentLevel
    score: int
    matched: list[str]


def classify(text: str) -> IntentResult:
    text = text.strip()

    high_score, high_matched = _score(text, _HIGH)
    med_score, med_matched = _score(text, _MEDIUM)

    total = high_score * 2 + med_score

    if high_score >= 7:
        intent: IntentLevel = "HIGH"
        matched = high_matched
    elif high_score >= 4 or (high_score > 0 and med_score >= 3):
        intent = "HIGH"
        matched = high_matched + med_matched
    elif med_score >= 3:
        intent = "MEDIUM"
        matched = med_matched
    else:
        intent = "LOW"
        matched = []

    return IntentResult(text=text, intent=intent, score=total, matched=matched)


def _score(text: str, signals: list[tuple[str, int]]) -> tuple[int, list[str]]:
    total, matched = 0, []
    for pattern, weight in signals:
        if re.search(pattern, text, re.IGNORECASE):
            total += weight
            matched.append(pattern)
    return total, matched
