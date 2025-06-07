# app/cli/manage.py

import typer
from app.services.llm.faiss_index import reset_index
from app.services.data.seed_data import seed_initial_data
from app.services.core.metrics_reader import show_metrics_summary
from app.agents.agent_router import AgentRouter

app = typer.Typer()

@app.command()
def reset_faiss():
    """FAISS vektör verisini sıfırlar"""
    reset_index()
    typer.echo("✅ FAISS index sıfırlandı.")

@app.command()
def seed_data():
    """Başlangıç veri setini yükler"""
    seed_initial_data()
    typer.echo("✅ Örnek veriler başarıyla yüklendi.")

@app.command()
def test_agents():
    """Agent'ları CLI'dan test eder"""
    router = AgentRouter()
    test_messages = [
        "Vegan menünüzde ne var?",
        "Yarın saat 20:00 için 2 kişilik yer ayırtabilir miyim?",
        "Pazar günleri açık mısınız?",
        "Ne dediğimi anlamadın mı?"
    ]

    for msg in test_messages:
        response = router.route(msg)
        print(f"[Input]: {msg}")
        print(f"[Response]: {response}\n")

@app.command()
def show_metrics():
    """Kayıtlı metrikleri gösterir"""
    show_metrics_summary()

if __name__ == "__main__":
    app()
