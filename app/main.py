from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat, users

app = FastAPI(title="Relaii API", version="1.0.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["35.183.222.241", "ec2-35-183-222-241.ca-central-1.compute.amazonaws.com", "http://35.183.222.241", "http://ec2-35-183-222-241.ca-central-1.compute.amazonaws.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(users.router, prefix="/api/users", tags=["users"])

@app.get("/")
async def root():
    return {"message": "Welcome to Relaii API"}