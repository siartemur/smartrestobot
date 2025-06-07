import pytest
from dotenv import load_dotenv
import asyncio

from app.agents.agent_router import AgentRouter

# ✅ .env dosyasını yükle
load_dotenv()


@pytest.mark.asyncio
async def test_menu_agent():
    router = AgentRouter()
    response = await router.handle_message("Menüde vegan seçenekler var mı?", {"user_id": 1})
    print("\n[Menu Agent Response]:", response)
    assert isinstance(response, str) and len(response) > 0


@pytest.mark.asyncio
async def test_reservation_agent():
    router = AgentRouter()
    response = await router.handle_message("Yarın saat 20:00'de 4 kişilik rezervasyon yapmak istiyorum.", {"user_id": 2})
    print("\n[Reservation Agent Response]:", response)
    assert isinstance(response, str) and len(response) > 0


@pytest.mark.asyncio
async def test_general_agent():
    router = AgentRouter()
    response = await router.handle_message("Restoranınız pazar günü açık mı?", {"user_id": 3})
    print("\n[General Agent Response]:", response)
    assert isinstance(response, str) and len(response) > 0


@pytest.mark.asyncio
async def test_fallback_agent():
    router = AgentRouter()
    response = await router.handle_message("Ajdklfjasldkf?", {"user_id": 4})
    print("\n[Fallback Agent Response]:", response)
    assert isinstance(response, str) and len(response) > 0
