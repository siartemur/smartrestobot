import os
import openai
from app.interfaces.llm.llm_provider import LLMProvider

# .env dosyasından API anahtarını al
openai.api_key = os.getenv("OPENAI_API_KEY")

class OpenAIProvider(LLMProvider):
    def generate(self, prompt: str, context: dict = {}) -> str:
        """
        GPT-4 modelini kullanarak verilen prompt'a yanıt üretir.
        """
        messages = [{"role": "user", "content": prompt}]
        if context:
            messages = context.get("messages", messages)

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages
        )
        return response.choices[0].message.content.strip()

# 🔁 DI: LLM sağlayıcısını dışarıya ver
def get_llm() -> LLMProvider:
    return OpenAIProvider()
