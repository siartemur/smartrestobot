# app/adapters/openai_provider.py

import openai
from app.interfaces.llm_provider import LLMProvider
from app.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

class OpenAIProvider(LLMProvider):
    async def generate_response(self, prompt: str, user_context: dict) -> str:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful restaurant assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message["content"]
