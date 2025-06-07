# app/tests/test_menu_agent.py

import os
import sys
import asyncio
from dotenv import load_dotenv

# Ortam değişkenlerini yükle (.env dosyasını üst dizinden al)
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.env"))
load_dotenv(dotenv_path=env_path)

# Projenin kök yolunu Python path'e ekle (import hatalarını önler)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.agents.menu_agent import MenuAgent

async def test_menu_agent_response():
    agent = MenuAgent()
    response = await agent.run("Vegan seçenekleriniz var mı?", user_context={})
    print("✅ Agent yanıtı:")
    print(response)

if __name__ == "__main__":
    asyncio.run(test_menu_agent_response())
