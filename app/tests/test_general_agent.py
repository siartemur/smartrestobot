# app/tests/test_general_agent.py

import os
import sys
import asyncio
from dotenv import load_dotenv

# Ortam değişkenlerini yükle
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.env"))
load_dotenv(dotenv_path=env_path)

# Import path düzeltmesi
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.agents.general_agent import GeneralAgent

async def test_general_agent_response():
    agent = GeneralAgent()

    test_message_1 = "Wi-Fi hizmetiniz var mı?"
    test_message_2 = "Açılış saatleriniz nedir?"
    test_message_3 = "Bir şey sormak istiyorum"

    print("🧪 Test 1 (Wi-Fi):")
    print(await agent.run(test_message_1, user_context={}), "\n")

    print("🧪 Test 2 (Saat):")
    print(await agent.run(test_message_2, user_context={}), "\n")

    print("🧪 Test 3 (Belirsiz mesaj):")
    print(await agent.run(test_message_3, user_context={}))

if __name__ == "__main__":
    asyncio.run(test_general_agent_response())
