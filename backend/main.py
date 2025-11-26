from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import database

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

@app.get("/")
async def root():
    return {"message": "Database Copilot API", "version": "1.0.0"}