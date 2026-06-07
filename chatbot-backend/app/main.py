from app.routers.chat import router as chat_router
from app.routers.admin import router as admin_router

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import validate_settings

app = FastAPI(
    title="Finnet IT Support Chatbot API",
    description="Backend API untuk chatbot IT Support berbasis RAG",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    validate_settings()
    print("Backend Finnet IT Support Chatbot berjalan.")


@app.get("/")
def root():
    return {"message": "Finnet IT Support Chatbot API"}


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "Backend aktif",
    }

app.include_router(chat_router)
app.include_router(admin_router)