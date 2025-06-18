from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import Runnable

def get_general_chain() -> Runnable:
    prompt = ChatPromptTemplate.from_template(
        """
        Kullanıcının restoran hakkında bilgi sorusu var:

        [Konuşma Geçmişi]
        {chat_history}

        [Yeni Mesaj]
        {message}

        [Restoran Statik Bilgisi]
        {static_info}

        Lütfen sadece yukarıdaki restoran bilgilerine dayanarak kısa, kibar ve yardımsever bir yanıt ver.
        - Açılış saatleri, konum, Wi-Fi, otopark, özel günler gibi konuları kapsayabilir.
        - Mesaj çok genel veya belirsizse, kullanıcıdan netleştirmesini iste.

        Cevabın sade ve doğal olsun.
        """
    )
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.3,
        max_tokens=150
    )
    return prompt | llm
