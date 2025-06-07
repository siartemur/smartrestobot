# app/tests/test_reservation_agent.py

import os
import sys
import asyncio
from dotenv import load_dotenv

# Ortam değişkenlerini yükle (.env'yi üst dizinden bul)
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.env"))
load_dotenv(dotenv_path=env_path)

# Import path ayarı
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.agents.reservation_agent import ReservationAgent

async def test_reservation_agent_response():
    agent = ReservationAgent()

    test_message_1 = "8 Haziran için 3 kişilik masa ayırtmak istiyorum"
    test_message_2 = "Rezervasyon yaptırmak istiyorum"

    print("🧪 Test 1 (tüm bilgiler mevcut):")
    response1 = await agent.run(test_message_1, user_context={})
    print(response1, "\n")

    print("🧪 Test 2 (eksik bilgi):")
    response2 = await agent.run(test_message_2, user_context={})
    print(response2)

if __name__ == "__main__":
    asyncio.run(test_reservation_agent_response())
