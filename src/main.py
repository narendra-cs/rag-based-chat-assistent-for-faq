from typing import Dict
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from src.api.chat import router as chat_router
from src.api.documents import router as documents_router

app = FastAPI(
    title="RAG-based Chat Assistant for FAQ API",
    description="RAG-based Chat Assistant for FAQ API",
    version="0.0.1",
    root_path="/api/v1",
    root_path_in_servers=False,
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


@app.get("/", status_code=status.HTTP_200_OK)
async def home() -> Dict[str, str]:
    return {"message": "Welcome to RAG-based Chat Assistant for FAQ API"}


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> Dict[str, str]:
    return {"message": "healthy"}


app.include_router(chat_router)
app.include_router(documents_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
