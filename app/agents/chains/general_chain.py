from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import Runnable

def get_general_chain() -> Runnable:
    prompt = ChatPromptTemplate.from_template(
        """
        Kullanıcının mesajı genel bilgi içindir:

        "{message}"

        Eğer mesaj şu konulardaysa:
        - Açılış saatleri
        - Lokasyon
        - Wi-Fi veya otopark durumu
        - Bayram/özel gün çalışma durumu

        Bilgilendirici ve kibar şekilde cevapla. Eğer mesaj belirsizse, hangi konuda bilgi istediğini sor.
        """
    )
    llm = ChatOpenAI(model="gpt-4", temperature=0.3)
    return prompt | llm
