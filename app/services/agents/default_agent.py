from app.interfaces.agents.agent import Agent

class DefaultAgent(Agent):
    async def run(self, message: str, user_context: dict) -> str:
        # Örnek bir davranış (dummy agent)
        return f"[DefaultAgent yanıtı]: '{message}' içeriği işlendi."
