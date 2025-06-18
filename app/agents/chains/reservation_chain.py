from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import Runnable

def get_reservation_chain() -> Runnable:
    prompt = ChatPromptTemplate.from_template(
        """
Aşağıda bir müşteriyle önceki konuşmalar ve şu anki mesajı verilmiştir.
Konuşmalar doğrultusunda, eksik bilgileri isteyin ya da rezervasyon işlemini tamamlayın.

[Geçmiş Konuşma]
{chat_history}

[Yeni Mesaj]
{message}

[Restoran Bilgisi]
{static_info}

[Güncel Durum]
{dynamic_info}

**Kurallar:**
1. Müşteri hangi tarih ve saatte gelmek istediğini belirtmiş mi kontrol et.
2. Kişi sayısı belirtilmiş mi kontrol et.
3. Eğer bu bilgiler eksikse sadece eksik olanı NAZİKÇE iste.
4. Eğer tüm bilgiler varsa ve uygun masa varsa rezervasyonu ONAYLA.
5. Uygun masa yoksa alternatif öner.
6. Cevap KISA, NET ve DOĞAL OLMALI. Teknik analiz yapma.

Son olarak cevabı şu JSON formatında üret:
{{
  "reply": "<Kullanıcıya gösterilecek mesaj>",
  "reservation_details": {{
    "date": "YYYY-MM-DD",
    "time": "HH:MM",
    "guest_count": <int>
  }}
}}
        """
    )

    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.3,
        max_tokens=300
    )

    return prompt | llm
