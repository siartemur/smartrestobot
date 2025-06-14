from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.api import chat, auth, admin, ab_test, reservation  # ✅ eklendi

# HTML template klasörü
templates = Jinja2Templates(directory="app/templates")

def create_app() -> FastAPI:
    app = FastAPI(
        title="SmartRestoBot API",
        version="1.0.0",
        description="Restoranlara özel LLM destekli akıllı sohbet ve rezervasyon sistemi."
    )

    # ✅ CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ✅ Statik dosyalar (CSS, JS, embed widget vs.)
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    # ✅ Router'lar
    app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
    app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
    app.include_router(chat.router, prefix="/api", tags=["Chat"])
    app.include_router(ab_test.router, prefix="/api", tags=["A/B Test"])
    app.include_router(reservation.router, prefix="/api", tags=["Reservation"])  # ✅ eklendi


    # ✅ Ana sayfa (chat widget test için)
    @app.get("/", response_class=HTMLResponse)
    async def serve_index(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})

    # ✅ Swagger UI için JWT Bearer token tanımı
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )

        openapi_schema["components"]["securitySchemes"] = {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            }
        }

        for path in openapi_schema["paths"].values():
            for method in path.values():
                method.setdefault("security", [{"BearerAuth": []}])

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi

    return app

# ✅ Uygulama başlatma noktası
app = create_app()
