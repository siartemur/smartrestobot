from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import Runnable

def get_reservation_chain() -> Runnable:
    prompt = ChatPromptTemplate.from_template(
        """
        Müşteri rezervasyon yapmak istiyor:

        "{message}"

        Aşağıdaki bilgileri kontrol et:
        - Tarih belirtilmiş mi?
        - Saat belirtilmiş mi?
        - Kişi sayısı var mı?

        Eksikse iste, tamamsa onayla.
        """
    )
    llm = ChatOpenAI(model="gpt-4", temperature=0.3)
    return prompt | llm
