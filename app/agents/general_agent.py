# app/agents/general_agent.py

from app.agents.chains.general_chain import get_general_chain

class GeneralAgent:
    def __init__(self):
        self.chain = get_general_chain()

    async def run(self, message: str, user_context: dict) -> str:
        response = await self.chain.ainvoke({"message": message})
        return response.content.strip()