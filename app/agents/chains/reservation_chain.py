from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import Runnable

def get_reservation_chain() -> Runnable:
    prompt = ChatPromptTemplate.from_template(
        """
Aşağıda bir müşteriyle geçmiş konuşmalar ve şu anki mesajı verilmiştir.
Konuşmalar doğrultusunda, eksik bilgileri NAZİKÇE sor ya da tüm bilgiler tamamlandıysa rezervasyonu onayla.

[Geçmiş Konuşma]
{chat_history}

[Yeni Mesaj]
{message}

[Restoran Bilgisi]
{static_info}

[Güncel Durum]
{dynamic_info}

[Müşteri Bilgisi]
{user_context}

[Bugünün Tarihi]
{current_date}

Kurallar:
1. Müşteri rezervasyon yapmak istiyor mu, kontrol et.
2. Tarih, saat ve kişi sayısı belirtilmiş mi kontrol et.
3. Eksik varsa sadece eksik olanları sor.
4. Müşteri özel bir masa tercihi belirttiyse (örn. 'cam kenarı'), bunu "preferred_location" alanında belirt.
5. Eğer tüm bilgiler TAM ise rezervasyonu onayla. Aksi halde hiçbir rezervasyon işlemi başlatma.
6. "Bu akşam", "yarın", "2 gün sonra" gibi tarih ifadelerini 'current_date' verisine göre YYYY-MM-DD formatına dönüştür.
7. Cevabın doğal, kibar ve kısa olsun. Teknik detay verme.

Son olarak cevabı şu JSON formatında üret:
{{
  "reply": "<Kullanıcıya gösterilecek mesaj>",
  "reservation_details": {{
    "date": "YYYY-MM-DD",
    "time": "HH:MM",
    "guest_count": <int>,
    "preferred_location": "<optional - örn: Window>"
  }}
}}
        """
    )

    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.3,
        max_tokens=500
    )

    return prompt | llm
