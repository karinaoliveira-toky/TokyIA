from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router as api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Motor de Inteligência Estratégica — Grupo Toky (Tok&Stok, Mobly e Guldi).",
    version=settings.PROJECT_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusão das rotas modularizadas
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    import os
    
    ambiente_host = os.getenv("HOST", "127.0.0.1")
    uvicorn.run("main:app", host=ambiente_host, port=8000, reload=True)