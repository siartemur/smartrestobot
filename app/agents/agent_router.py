# app/agents/agent_router.py

from app.agents.menu_agent import MenuAgent
from app.agents.reservation_agent import ReservationAgent
from app.agents.general_agent import GeneralAgent
from app.agents.fallback_agent import FallbackAgent
from app.interfaces.agents.agent import Agent
from langchain_openai import ChatOpenAI
from app.services.infrastructure.audit_logger import log_interaction


class AgentRouter:
    def __init__(self):
        self.menu_agent = MenuAgent()
        self.reservation_agent = ReservationAgent()
        self.general_agent = GeneralAgent()
        self.fallback_agent = FallbackAgent()
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)

    async def classify_agent_type(self, message: str) -> str:
        """LLM ile agent türünü belirle"""
        system_prompt = (
            "Aşağıdaki kullanıcı mesajının hangi amaca ait olduğunu belirle.\n"
            "Sadece şu dört cevaptan birini döndür: menu, reservation, general, fallback\n"
            "Ek açıklama yapma."
        )
        chat = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]
        response = await self.llm.ainvoke(chat)
        return response.content.strip().lower()

    async def handle_message(self, message: str, user_context: dict) -> str:
        agent_type = await self.classify_agent_type(message)

        if agent_type == "menu":
            agent = self.menu_agent
        elif agent_type == "reservation":
            agent = self.reservation_agent
        elif agent_type == "general":
            agent = self.general_agent
        else:
            agent = self.fallback_agent

        response = await agent.run(message, user_context)

        # ✅ Loglama
        log_interaction(
            user_id=user_context.get("user_id", 0),
            message=message,
            response=response,
            agent_type=agent_type
        )

        return response
