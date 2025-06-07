from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import Runnable

def get_fallback_chain() -> Runnable:
    prompt = ChatPromptTemplate.from_template(
        """
        Kullanıcının mesajı anlaşılamadı:

        "{message}"

        Empatik, kibar ve yardım etmek isteyen bir şekilde yanıt ver.
        Hangi konuda yardımcı olabileceğini sor.
        """
    )
    llm = ChatOpenAI(model="gpt-4", temperature=0.3)
    return prompt | llm
