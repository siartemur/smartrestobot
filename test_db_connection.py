from app.database.db import engine

def test_connection():
    try:
        conn = engine.connect()
        print("✅ PostgreSQL bağlantısı başarılı!")
        conn.close()
    except Exception as e:
        print("❌ Bağlantı hatası:", e)

test_connection()
