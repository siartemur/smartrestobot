# app/api/admin.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.database import models
from app.api.dependencies import get_admin_user
from app.dashboard.admin_panel import generate_metrics_dashboard , generate_bad_response_dashboard
from app.core.usecases.generate_metrics_report import generate_ab_test_report

router = APIRouter()

@router.get("/restaurants")
def list_all_restaurants(
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_admin_user)
):
    return db.query(models.Restaurant).all()


@router.get("/ab-test-report")
def ab_test_report():
    return {"results": generate_ab_test_report()}


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    charts = generate_metrics_dashboard()
    if "error" in charts:
        return f"<h1>{charts['error']}</h1>"

    html = f"""
    <html>
        <head><title>SmartRestoBot Dashboard</title></head>
        <body>
            <h2>LLM Yanıt Süresi Zaman Grafiği</h2>
            <img src="data:image/png;base64,{charts['latency_chart']}" />

            <h2>Prompt vs Yanıt Uzunluğu</h2>
            <img src="data:image/png;base64,{charts['length_chart']}" />

            <h2>Model Dağılımı</h2>
            <img src="data:image/png;base64,{charts['model_chart']}" />

            <h2>Restoranlara Göre Chat Sayısı</h2>
            <img src="data:image/png;base64,{charts['restaurant_chart']}" />
        </body>
    </html>
    """
    return html

@router.get("/bad-responses", response_class=HTMLResponse)
def bad_responses_dashboard():
    charts = generate_bad_response_dashboard()
    if "error" in charts:
        return f"<h1>{charts['error']}</h1>"

    html = f"""
    <html>
        <head><title>Kötü Yanıt Dashboard</title></head>
        <body>
            <h2>📉 Günlük Kötü Yanıt Sayısı</h2>
            <img src="data:image/png;base64,{charts['daily_bad_responses']}" />

            <h2>🧪 Kötü Yanıt Nedenleri</h2>
            <img src="data:image/png;base64,{charts['reason_distribution']}" />

            <h2>🏢 Restoranlara Göre Kötü Yanıt Dağılımı</h2>
            <img src="data:image/png;base64,{charts['restaurant_bad_responses']}" />
        </body>
    </html>
    """
    return html

