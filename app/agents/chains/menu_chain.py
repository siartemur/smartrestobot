from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import Runnable

def get_menu_chain() -> Runnable:
    prompt = ChatPromptTemplate.from_template(
        """
        Aşağıdaki mesaj, bir müşteri tarafından restoran asistanına gönderildi:

        "{message}"

        Müşterinin talebine uygun, açıklayıcı, kibar ve bilgilendirici bir yanıt ver.
        Menü, içerikler, alerjen bilgileri ve özel seçenekler gibi detaylar içerebilir.
        """
    )
    llm = ChatOpenAI(model="gpt-4", temperature=0.3)
    return prompt | llm
