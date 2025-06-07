import asyncio
import csv
import os
from dotenv import load_dotenv
load_dotenv()  # ✅ Ortam değişkenlerini (.env) yükle

from app.agents.agent_router import AgentRouter

async def test_audit_logging():
    router = AgentRouter()

    message = "Yarın için 2 kişilik masa ayırtabilir miyim?"
    user_context = {"user_id": 999}

    log_file = "app/logs/audit_logs.csv"
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            initial_line_count = sum(1 for _ in f)
    else:
        initial_line_count = 0

    response = await router.handle_message(message, user_context)
    print("🧪 Yanıt:", response)

    with open(log_file, "r", encoding="utf-8") as f:
        final_line_count = sum(1 for _ in f)

    assert final_line_count > initial_line_count, "❌ Log kaydı başarısız!"
    print("✅ Log satırı eklendi:", final_line_count - initial_line_count)

if __name__ == "__main__":
    asyncio.run(test_audit_logging())
