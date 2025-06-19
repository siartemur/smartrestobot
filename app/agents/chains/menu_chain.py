from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import Runnable

def get_menu_chain() -> Runnable:
    prompt = ChatPromptTemplate.from_template(
        """
Aşağıda bir müşteriyle geçmiş konuşmalar ve şu anki mesajı verilmiştir.
Müşterinin menüyle ilgili bilgi istediğini varsayarak eksik detayları NAZİKÇE iste veya tam bilgi varsa doğrudan açıkla.

[Geçmiş Konuşma]
{chat_history}

[Yeni Mesaj]
{message}

[Restoran Bilgisi]
{static_info}

[Menü ve Güncel Durum]
{menu}

[Müşteri Bilgisi]
{user_context}

[Bugünün Tarihi]
{current_date}

Kurallar:
1. Müşteri özel yemekler, içerikler, alerjenler veya vegan/glutensiz seçenekler hakkında bilgi istiyor olabilir.
2. Eğer eksik bilgi varsa müşteriden NAZİK bir dille detay iste.
3. Menü dışı bir şey sorarsa, kibarca sınırlarını belirt.
4. Bilgilendirici, akıcı ve nazik cevaplar ver. Menü bilgilerini zengin tut ama mesajı çok uzatma.
5. Teknik terim kullanma. Samimi ve anlaşılır bir dil kullan.
6. Cevap sonuna sipariş ya da rezervasyon yapabileceğini hatırlatabilirsin.

Son olarak cevabı şu JSON formatında üret:
{{
  "reply": "<Kullanıcıya gösterilecek mesaj>"
}}
        """
    )

    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.3,
        max_tokens=500
    )

    return prompt | llm
