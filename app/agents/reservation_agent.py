# app/agents/reservation_agent.py

from app.agents.chains.reservation_chain import get_reservation_chain

class ReservationAgent:
    def __init__(self):
        self.chain = get_reservation_chain()

    async def run(self, message: str, user_context: dict) -> str:
        response = await self.chain.ainvoke({"message": message})
        return response.content.strip()