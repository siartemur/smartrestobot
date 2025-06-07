# app/agents/fallback_agent.py

from app.agents.chains.fallback_chain import get_fallback_chain

class FallbackAgent:
    def __init__(self):
        self.chain = get_fallback_chain()

    async def run(self, message: str, user_context: dict) -> str:
        response = await self.chain.ainvoke({"message": message})
        return response.content.strip()
