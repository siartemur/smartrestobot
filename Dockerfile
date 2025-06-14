# Dockerfile

FROM python:3.11-slim

# Çalışma dizini
WORKDIR /app

# Gereksinimler
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyaları
COPY . .

# Statik klasör varsa (embed_script.js gibi), şimdiden kopyalanmış olacak
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
