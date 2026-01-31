from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import database, auth_routes, chat
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Database Copilot API", version="1.0.0")

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(database.router)
app.include_router(auth_routes.router)
app.include_router(chat.router)

@app.get("/")
async def root():
    return {"message": "Database Copilot API", "version": "1.0.0"}