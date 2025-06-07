from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# 1. Model yükle
model = SentenceTransformer("all-MiniLM-L6-v2")

# 2. Örnek metinler ve embedding oluştur
texts = ["Menüde pizza var", "Masa saat 8’de hazır", "Alerjen içeriğimiz var mı?"]
vectors = model.encode(texts)

# 3. FAISS index oluştur (L2 mesafe)
index = faiss.IndexFlatL2(vectors.shape[1])
index.add(np.array(vectors).astype('float32'))

# 4. Sorgu metni → vektörleştir → en yakınları ara
query = "Pizza seçenekleri nelerdir?"
query_vector = model.encode([query])
distances, indices = index.search(np.array(query_vector).astype('float32'), k=2)

# 5. Sonuçları yazdır
print("🔍 Sorgu:", query)
print("📌 En ilgili sonuçlar:")
for i in indices[0]:
    print("-", texts[i])
