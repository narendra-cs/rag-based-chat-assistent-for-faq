from typing import Dict

from fastapi import APIRouter, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from src.api.chat import router as chat_router
from src.api.documents import router as documents_router
from src.config import API_PREFIX, MODE

app = FastAPI(
    title="RAG-based Chat Assistant for FAQ API",
    description="RAG-based Chat Assistant for FAQ API",
    version="0.0.1",
    docs_url=f"{API_PREFIX}/docs",
    redoc_url=None,
    openapi_url=f"{API_PREFIX}/openapi.json",
)

# Add CORS middleware to allow requests from the UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "Accept",
        "X-Requested-With",
        "X-HTTP-Method-Override",
    ],
)

# Create a base router for all API routes
api_router = APIRouter(prefix=API_PREFIX)

# Include all API routes under the base router
api_router.include_router(chat_router)
api_router.include_router(documents_router)


# Include the base router with all API routes
app.include_router(api_router)


# Root endpoint
@app.get("/", status_code=status.HTTP_200_OK)
async def home() -> Dict[str, str]:
    return {"message": "Welcome to RAG-based Chat Assistant for FAQ API"}


# Health check endpoint
@app.get(f"{API_PREFIX}/health", status_code=status.HTTP_200_OK)
async def health_check() -> Dict[str, str]:
    return {"message": "healthy"}


if __name__ == "__main__":
    import uvicorn

    if MODE == "DEVELOPMENT":
        uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
    else:
        uvicorn.run("src.main:app", host="0.0.0.0", port=8000)
