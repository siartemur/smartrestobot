# app/agents/menu_agent.py

from app.agents.chains.menu_chain import get_menu_chain

class MenuAgent:
    def __init__(self):
        self.chain = get_menu_chain()

    async def run(self, message: str, user_context: dict) -> str:
        response = await self.chain.ainvoke({"message": message})
        return response.content.strip()