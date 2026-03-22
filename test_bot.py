"""
Local test — no LINE credentials needed.
Simulates incoming messages and prints intent + auto-reply.
"""
import os
os.environ.setdefault("BOOKING_LINK", "https://calendly.com/your-link")

from classifier import classify
from replies import get_reply

SAMPLE_MESSAGES = [
    # HIGH
    "想預約諮詢",
    "費用是多少？",
    "怎麼找你諮詢？",
    "想了解履歷諮詢的費用",
    "有提供一對一服務嗎",
    # MEDIUM
    "想了解怎麼準備面試",
    "我在考慮轉職，不知道從哪裡開始",
    "履歷要怎麼寫比較好",
    "想了解職涯規劃",
    # LOW
    "你好",
    "嗨",
    "謝謝",
]

COLORS = {"HIGH": "\033[92m", "MEDIUM": "\033[93m", "LOW": "\033[90m", "RESET": "\033[0m"}

print("\n" + "="*60)
print("  LINE Bot 本地測試")
print("="*60)

for msg in SAMPLE_MESSAGES:
    result = classify(msg)
    reply = get_reply(result.intent, msg)
    color = COLORS[result.intent]
    reset = COLORS["RESET"]

    print(f"\n{color}[{result.intent}]{reset} 用戶：{msg}")
    print(f"  分數：{result.score}  匹配：{result.matched or '—'}")
    print(f"  Bot 回覆：\n    " + reply.replace("\n", "\n    "))
    print("-"*60)
