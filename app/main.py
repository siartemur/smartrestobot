from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.api import chat, auth, admin, ab_test

def create_app() -> FastAPI:
    app = FastAPI(
        title="SmartRestoBot API",
        version="1.0.0",
        description="Restoranlara özel LLM destekli akıllı sohbet ve rezervasyon sistemi."
    )

    # ✅ CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Geliştirme sürecinde geniş tutuldu, prod'da sınırla
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ✅ Router'lar
    app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
    app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
    app.include_router(chat.router, prefix="/api", tags=["Chat"])
    app.include_router(ab_test.router, prefix="/api", tags=["A/B Test"])

    # ✅ Sağlık kontrolü
    @app.get("/")
    def health_check():
        return {"message": "✅ SmartRestoBot API is running."}

    # ✅ JWT Bearer Token Swagger UI tanımı
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

# Uygulama başlatma noktası
app = create_app()
