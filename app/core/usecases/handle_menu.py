# app/usecases/handle_message.py

from app.agents.agent_router import AgentRouter
from app.services.core.sanitizer import sanitize_input

router = AgentRouter()

async def handle_message(message: str, user_context: dict) -> str:
    cleaned_message = sanitize_input(message)
    response = await router.handle_message(cleaned_message, user_context)
    return response