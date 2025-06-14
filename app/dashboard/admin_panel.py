import matplotlib
matplotlib.use("Agg")  # Headless backend
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import matplotlib.dates as mdates

METRICS_CSV = "app/logs/metrics.csv"
BAD_RESPONSES_CSV = "app/logs/bad_responses.csv"

def generate_base64_image(fig):
    buf = BytesIO()
    plt.tight_layout()
    fig.savefig(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()
    plt.close(fig)
    return img_base64

def generate_metrics_dashboard():
    try:
        df = pd.read_csv(METRICS_CSV)

        expected_columns = [
            "timestamp", "restaurant_id", "agent_type", "prompt_version",
            "prompt_name", "model", "prompt_length", "response_length",
            "token_usage", "latency_ms", "bad"
        ]
        if list(df.columns) != expected_columns:
            return {"error": f"metrics.csv sütunları beklenen yapıda değil. Beklenen: {expected_columns}"}

        # Tip dönüşümü ve eksik veri kontrolü
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df.dropna(subset=["timestamp", "prompt_length", "response_length", "latency_ms"])

        df[["prompt_length", "response_length", "latency_ms"]] = df[["prompt_length", "response_length", "latency_ms"]].astype(float)

        charts = {}

        # 🎯 Grafik 1: Yanıt Süresi Zaman Çizelgesi
        fig1, ax1 = plt.subplots()
        df_sorted = df.sort_values("timestamp")
        ax1.plot(df_sorted["timestamp"], df_sorted["latency_ms"], marker='o')
        ax1.set_title("Yanıt Süresi (ms) Zaman Çizelgesi")
        ax1.set_xlabel("Zaman")
        ax1.set_ylabel("Latency (ms)")
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        fig1.autofmt_xdate()
        charts["latency_chart"] = generate_base64_image(fig1)

        # 🎯 Grafik 2: Prompt vs Yanıt Uzunluğu
        fig2, ax2 = plt.subplots()
        ax2.scatter(df["prompt_length"], df["response_length"], alpha=0.6)
        ax2.set_title("Prompt vs Yanıt Uzunluğu")
        ax2.set_xlabel("Prompt Uzunluğu (char)")
        ax2.set_ylabel("Yanıt Uzunluğu (char)")
        charts["length_chart"] = generate_base64_image(fig2)

        # 🎯 Grafik 3: Model Dağılımı
        fig3, ax3 = plt.subplots()
        df["model"].value_counts().plot(kind="pie", autopct='%1.1f%%', startangle=140, ax=ax3)
        ax3.set_ylabel("")
        ax3.set_title("Kullanılan Model Dağılımı")
        charts["model_chart"] = generate_base64_image(fig3)

        # 🎯 Grafik 4: Restoranlara Göre Chat Sayısı
        fig4, ax4 = plt.subplots()
        df["restaurant_id"].value_counts().plot(kind="bar", ax=ax4)
        ax4.set_title("Restoranlara Göre Chat Sayısı")
        ax4.set_xlabel("Restoran ID")
        ax4.set_ylabel("Chat Sayısı")
        charts["restaurant_chart"] = generate_base64_image(fig4)

        return charts

    except Exception as e:
        return {"error": str(e)}


def generate_bad_response_dashboard():
    try:
        df = pd.read_csv(BAD_RESPONSES_CSV)

        expected_columns = ["timestamp", "restaurant_id", "prompt", "response", "reason"]
        if list(df.columns) != expected_columns:
            return {"error": f"bad_responses.csv sütunları beklenen yapıda değil. Beklenen: {expected_columns}"}

        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df.dropna(subset=["timestamp", "restaurant_id", "reason"])

        charts = {}

        # 🎯 Grafik 1: Günlük kötü yanıt sayısı
        df_daily = df.groupby(df["timestamp"].dt.date).size()
        fig1, ax1 = plt.subplots()
        df_daily.plot(kind="line", marker="o", ax=ax1)
        ax1.set_title("Günlük Kötü Yanıt Sayısı")
        ax1.set_xlabel("Tarih")
        ax1.set_ylabel("Kötü Yanıt")
        charts["daily_bad_responses"] = generate_base64_image(fig1)

        # 🎯 Grafik 2: Kötü yanıt nedenleri
        fig2, ax2 = plt.subplots()
        df["reason"].value_counts().plot(kind="bar", ax=ax2)
        ax2.set_title("Kötü Yanıt Nedenleri")
        ax2.set_xlabel("Neden")
        ax2.set_ylabel("Adet")
        charts["reason_distribution"] = generate_base64_image(fig2)

        # 🎯 Grafik 3: Restoran bazlı kötü yanıtlar
        fig3, ax3 = plt.subplots()
        df["restaurant_id"].value_counts().plot(kind="bar", ax=ax3)
        ax3.set_title("Restoranlara Göre Kötü Yanıt Sayısı")
        ax3.set_xlabel("Restoran ID")
        ax3.set_ylabel("Adet")
        charts["restaurant_bad_responses"] = generate_base64_image(fig3)

        return charts

    except Exception as e:
        return {"error": str(e)}
